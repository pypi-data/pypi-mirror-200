# Copyright 2020 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os

from flask import current_app
from flask import send_file
from flask_login import current_user
from flask_login import login_required

import kadi.lib.constants as const
from kadi.ext.db import db
from kadi.lib.api.blueprint import bp
from kadi.lib.api.core import internal
from kadi.lib.api.core import json_error_response
from kadi.lib.api.core import json_response
from kadi.lib.config.core import get_sys_config
from kadi.lib.conversion import normalize
from kadi.lib.conversion import strip
from kadi.lib.db import escape_like
from kadi.lib.notifications.models import Notification
from kadi.lib.notifications.schemas import NotificationSchema
from kadi.lib.permissions.core import get_permitted_objects
from kadi.lib.resources.schemas import BasicResourceSchema
from kadi.lib.search.models import SavedSearch
from kadi.lib.search.schemas import SavedSearchSchema
from kadi.lib.storage.misc import create_misc_storage
from kadi.lib.utils import get_class_by_name
from kadi.lib.web import qparam
from kadi.modules.main.utils import get_licenses
from kadi.modules.main.utils import get_tags


@bp.get("/notifications", v=None)
@login_required
@internal
def get_notifications():
    """Get all notifications of the current user."""
    notifications = current_user.notifications.order_by(Notification.created_at.desc())
    return json_response(200, NotificationSchema(many=True).dump(notifications))


@bp.get("/saved-searches/<int:id>", v=None)
@login_required
@internal
def get_saved_search(id):
    """Get a saved search of the current user."""
    saved_search = current_user.saved_searches.filter(
        SavedSearch.id == id
    ).first_or_404()

    return json_response(200, SavedSearchSchema().dump(saved_search))


@bp.get("/index-image", v=None)
@internal
def preview_index_image():
    """Preview the configured index image directly in the browser."""
    image_identifier = get_sys_config(const.SYS_CONFIG_INDEX_IMAGE, use_fallback=False)
    filepath = None

    # Check whether an image that was uploaded via the GUI should be used or try to use
    # the path specified directly in the config file as fallback, if applicable.
    if image_identifier:
        storage = create_misc_storage()
        filepath = storage.create_filepath(image_identifier)

        if not storage.exists(filepath):
            filepath = None
    else:
        filepath = current_app.config[const.SYS_CONFIG_INDEX_IMAGE]

        if filepath is not None and not os.path.isfile(filepath):
            filepath = None

    if filepath is not None:
        return send_file(
            filepath, mimetype=const.MIMETYPE_JPEG, download_name="index.jpg"
        )

    return json_error_response(404)


@bp.get("/quick-search", v=None)
@login_required
@internal
@qparam("query", parse=normalize)
def quick_search(qparams):
    """Search for different resources using a simple query.

    Currently used in the base navigation quick search. Supports resources of type
    :class:`.Record`, :class:`.Collection`, :class:`.Template` and :class:`.Group`.
    """
    query = escape_like(qparams["query"])
    resource_queries = []

    for resource_type, resource_type_meta in const.RESOURCE_TYPES.items():
        model = get_class_by_name(resource_type_meta["model"])

        resources_query = (
            get_permitted_objects(current_user, "read", resource_type)
            .filter(
                model.state == const.MODEL_STATE_ACTIVE,
                db.or_(
                    model.title.ilike(f"%{query}%"),
                    model.identifier.ilike(f"%{query}%"),
                ),
            )
            .with_entities(
                model.id,
                model.title,
                model.identifier,
                model.last_modified.label("last_modified"),
                db.literal(resource_type).label("type"),
                db.literal(str(resource_type_meta["title"])).label("pretty_type"),
            )
        )

        resource_queries.append(resources_query)

    resources = (
        resource_queries[0]
        .union(*resource_queries[1:])
        .order_by(db.desc("last_modified"))
        .limit(5)
    )

    return json_response(200, BasicResourceSchema(many=True).dump(resources))


@bp.get("/check-identifier/<resource_type>", v=None)
@login_required
@internal
@qparam("identifier")
@qparam("exclude", default=None, parse=int)
def check_identifier(resource_type, qparams):
    """Check whether an identifier of a specific resource type already exists."""
    if resource_type not in const.RESOURCE_TYPES:
        return json_error_response(404)

    data = {"duplicate": False}

    model = get_class_by_name(const.RESOURCE_TYPES[resource_type]["model"])
    resource = (
        model.query.filter_by(identifier=qparams["identifier"])
        .with_entities(model.id)
        .first()
    )

    if resource is not None and resource.id != qparams["exclude"]:
        data["duplicate"] = True

    return json_response(200, data)


@bp.get("/saved-searches/select", v=None)
@login_required
@internal
@qparam("page", default=1, parse=int)
@qparam("term", parse=normalize)
@qparam("object")
def select_saved_searches(qparams):
    """Search saved searches in dynamic selections.

    Similar to :func:`kadi.lib.resources.api.get_selected_resources`. Only the saved
    searches of the current user are returned.
    """
    searches_query = current_user.saved_searches.filter(
        SavedSearch.name.ilike(f"%{escape_like(qparams['term'])}%"),
    )

    if qparams["object"]:
        searches_query = searches_query.filter(SavedSearch.object == qparams["object"])

    paginated_searches = searches_query.order_by(SavedSearch.name).paginate(
        page=qparams["page"], per_page=10, error_out=False
    )

    data = {
        "results": [],
        "pagination": {"more": paginated_searches.has_next},
    }
    for saved_search in paginated_searches:
        data["results"].append({"id": saved_search.id, "text": saved_search.name})

    return json_response(200, data)


@bp.get("/tags/select", v=None)
@login_required
@internal
@qparam("page", default=1, parse=int)
@qparam("term", parse=normalize)
@qparam("type", default=None)
def select_tags(qparams):
    """Search tags in dynamic selections.

    Similar to :func:`kadi.lib.resources.api.get_selected_resources`. Only the tags of
    resources the current user has read permission for are returned.
    """
    paginated_tags = get_tags(
        filter_term=qparams["term"], resource_type=qparams["type"]
    ).paginate(page=qparams["page"], per_page=10, error_out=False)

    data = {
        "results": [],
        "pagination": {"more": paginated_tags.has_next},
    }
    for tag in paginated_tags:
        data["results"].append({"id": tag.name, "text": tag.name})

    return json_response(200, data)


@bp.get("/licenses/select", v=None)
@login_required
@internal
@qparam("page", default=1, parse=int)
@qparam("term", parse=strip)
def select_licenses(qparams):
    """Search licenses in dynamic selections.

    Similar to :func:`kadi.lib.resources.api.get_selected_resources`.
    """
    paginated_licenses = get_licenses(filter_term=qparams["term"]).paginate(
        page=qparams["page"], per_page=10, error_out=False
    )

    data = {
        "results": [],
        "pagination": {"more": paginated_licenses.has_next},
    }
    for license in paginated_licenses:
        data["results"].append({"id": license.name, "text": license.title})

    return json_response(200, data)
