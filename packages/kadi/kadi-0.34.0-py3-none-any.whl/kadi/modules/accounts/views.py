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
from flask import current_app
from flask import redirect
from flask import render_template
from flask import request
from flask_babel import format_number
from flask_babel import gettext as _
from flask_login import current_user
from flask_login import login_required

import kadi.lib.constants as const
from .blueprint import bp
from .forms import EmailConfirmationForm
from .forms import get_login_form
from .forms import LegalsAcceptanceForm
from .forms import RegistrationForm
from .forms import RequestPasswordResetForm
from .forms import ResetPasswordForm
from .models import LocalIdentity
from .models import User
from .models import UserState
from .providers import LDAPProvider
from .providers import LocalProvider
from .providers import ShibProvider
from .utils import login_user
from .utils import logout_user
from kadi.ext.db import db
from kadi.ext.limiter import limiter
from kadi.lib.db import update_object
from kadi.lib.format import filesize
from kadi.lib.mails.utils import send_email_confirmation_mail
from kadi.lib.mails.utils import send_password_reset_mail
from kadi.lib.utils import utcnow
from kadi.lib.web import flash_danger
from kadi.lib.web import flash_success
from kadi.lib.web import get_next_url
from kadi.lib.web import html_error_response
from kadi.lib.web import url_for
from kadi.modules.collections.models import Collection
from kadi.modules.collections.models import CollectionState
from kadi.modules.groups.models import Group
from kadi.modules.groups.models import GroupState
from kadi.modules.records.models import File
from kadi.modules.records.models import FileState
from kadi.modules.records.models import Record
from kadi.modules.records.models import RecordState
from kadi.modules.sysadmin.utils import legals_acceptance_required
from kadi.modules.templates.models import Template
from kadi.modules.templates.models import TemplateState


@bp.get("/login")
def login():
    """Page to select an authentication provider to log in with.

    See :func:`login_with_provider`.
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    providers = list(current_app.config["AUTH_PROVIDERS"])
    forms = []

    for provider in providers:
        form = get_login_form(provider)
        forms.append(form)

    return render_template(
        "accounts/login.html",
        title=_("Login"),
        forms=forms,
        next_url=get_next_url(),
        js_context={"providers": providers},
    )


@bp.route("/login/<provider>", methods=["GET", "POST"])
@limiter.limit("5/minute")
@limiter.limit("50/minute", key_func=lambda: "login_global")
def login_with_provider(provider):
    """Page to log in with a specific authentication provider."""
    if (
        current_user.is_authenticated
        or provider not in current_app.config["AUTH_PROVIDERS"]
    ):
        return redirect(url_for("main.index"))

    form = get_login_form(provider)
    next_url = get_next_url()

    if provider == const.AUTH_PROVIDER_TYPE_LOCAL:
        return _login_local(provider, form, next_url)

    if provider == const.AUTH_PROVIDER_TYPE_LDAP:
        return _login_ldap(provider, form, next_url)

    if provider == const.AUTH_PROVIDER_TYPE_SHIB:
        return _login_shib(provider, form, next_url)

    return html_error_response(404)


def _login_local(provider, form, next_url):
    if request.method == "GET":
        return redirect(url_for("accounts.login", tab=provider))

    if form.validate():
        user_info = LocalProvider.authenticate(
            username=form.username.data, password=form.password.data
        )

        if user_info.is_authenticated:
            identity = user_info.data

            login_user(identity)
            db.session.commit()

            return redirect(next_url)

    flash_danger(_("Invalid credentials."))
    return redirect(url_for("accounts.login", next=next_url, tab=provider))


def _login_ldap(provider, form, next_url):
    if request.method == "GET":
        return redirect(url_for("accounts.login", tab=provider))

    if form.validate():
        user_info = LDAPProvider.authenticate(
            username=form.username.data, password=form.password.data
        )

        if user_info.is_authenticated:
            ldap_info = user_info.data
            identity = LDAPProvider.register(
                username=ldap_info.username,
                email=ldap_info.email,
                displayname=ldap_info.displayname,
            )

            if identity:
                login_user(identity)
                db.session.commit()

                return redirect(next_url)

            flash_danger(_("Error registering user."))
            return redirect(url_for("accounts.login", next=next_url, tab=provider))

    flash_danger(_("Invalid credentials."))
    return redirect(url_for("accounts.login", next=next_url, tab=provider))


def _login_shib(provider, form, next_url):
    if request.method == "POST":
        if form.validate():
            target = url_for(
                "accounts.login_with_provider",
                provider=const.AUTH_PROVIDER_TYPE_SHIB,
                next=next_url,
            )
            url = ShibProvider.get_session_initiator(form.idp.data, target)
            return redirect(url)

        flash_danger(_("Invalid identity provider."))

    elif request.method == "GET":
        if ShibProvider.contains_valid_idp():
            user_info = ShibProvider.authenticate()

            if user_info.is_authenticated:
                shib_info = user_info.data
                identity = ShibProvider.register(
                    username=shib_info.username,
                    email=shib_info.email,
                    displayname=shib_info.displayname,
                )

                if identity:
                    login_user(identity)
                    db.session.commit()

                    return redirect(next_url)

                flash_danger(_("Error registering user."))

            else:
                shib_meta = ShibProvider.get_metadata()
                required_attrs = ShibProvider.get_required_attributes()

                return render_template(
                    "accounts/shib_missing_attributes.html",
                    title=_("Login failed"),
                    sp_entity_id=shib_meta.sp_entity_id,
                    idp_entity_id=shib_meta.idp_entity_id,
                    idp_displayname=shib_meta.idp_displayname,
                    idp_support_contact=shib_meta.idp_support_contact,
                    required_attrs=required_attrs,
                    timestamp=utcnow().isoformat(),
                )

        else:
            flash_danger(_("Invalid identity provider."))
            url = ShibProvider.get_logout_initiator(url_for("accounts.login"))
            return redirect(url)

    return redirect(url_for("accounts.login", next=next_url, tab=provider))


def _send_email_confirmation_mail(identity, email=None):
    if send_email_confirmation_mail(identity, email=email):
        flash_success(_("A confirmation email has been sent."))
    else:
        flash_danger(_("Could not send confirmation email."))


@bp.get("/logout")
def logout():
    """Endpoint to log a user out of the application."""
    redirect_url = logout_user()
    return redirect(redirect_url)


@bp.route("/register", methods=["GET", "POST"])
def register():
    """Page to register a new local user."""
    if not LocalProvider.registration_allowed() or current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = RegistrationForm()
    enforce_legals = legals_acceptance_required()

    if not enforce_legals:
        del form.accept_legals

    if request.method == "POST":
        if form.validate():
            identity = LocalProvider.register(
                username=form.username.data,
                displayname=form.displayname.data,
                email=form.email.data,
                password=form.password.data,
            )

            if identity:
                if LocalProvider.email_confirmation_required():
                    _send_email_confirmation_mail(identity)

                if enforce_legals:
                    identity.user.accept_legals()
                    db.session.commit()

                flash_success(_("Registration completed successfully."))
                return redirect(
                    url_for("accounts.login", tab=const.AUTH_PROVIDER_TYPE_LOCAL)
                )

        flash_danger(_("Error registering user."))

    return render_template(
        "accounts/register.html",
        title=_("Register"),
        form=form,
        enforce_legals=enforce_legals,
    )


@bp.route("/reset-password", methods=["GET", "POST"])
def request_password_reset():
    """Page to request a reset for a local user's password."""
    if not LocalProvider.is_registered() or current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = RequestPasswordResetForm()

    if form.validate_on_submit():
        identity = LocalIdentity.query.filter_by(username=form.username.data).first()

        if identity:
            send_password_reset_mail(identity)

        # Always indicate success, so anonymous users cannot use this functionality to
        # easily determine existing usernames.
        flash_success(_("A password reset email has been sent."))
        return redirect(url_for("accounts.login", tab=const.AUTH_PROVIDER_TYPE_LOCAL))

    return render_template(
        "accounts/request_password_reset.html", title=_("Password reset"), form=form
    )


@bp.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    """Page to reset a local user's password.

    The token to reset the password must be a JSON web token obtained from
    :func:`request_password_reset`.
    """
    if not LocalProvider.is_registered() or current_user.is_authenticated:
        return redirect(url_for("main.index"))

    payload = LocalIdentity.decode_password_reset_token(token)

    if not payload:
        flash_danger(_("Token invalid or expired."))
        return redirect(url_for("main.index"))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        identity = LocalIdentity.query.get(payload["id"])
        identity.set_password(form.password.data)
        db.session.commit()

        flash_success(_("Password changed successfully."))
        return redirect(url_for("accounts.login", tab=const.AUTH_PROVIDER_TYPE_LOCAL))

    return render_template(
        "accounts/reset_password.html", title=_("Password reset"), form=form
    )


@bp.route("/confirm-email", methods=["GET", "POST"])
@login_required
def request_email_confirmation():
    """Page to request confirmation for a local user's email address."""
    if (
        not LocalProvider.is_registered()
        or current_user.identity.type != const.AUTH_PROVIDER_TYPE_LOCAL
        or not current_user.identity.needs_email_confirmation
    ):
        return redirect(url_for("main.index"))

    identity = current_user.identity
    email = identity.email

    form = EmailConfirmationForm()

    if form.validate_on_submit():
        _send_email_confirmation_mail(identity, email=form.email.data or email)
        return redirect(url_for("accounts.request_email_confirmation"))

    return render_template(
        "accounts/request_email_confirmation.html",
        title=_("Email confirmation"),
        form=form,
        email=email,
    )


@bp.get("/confirm-email/<token>")
def confirm_email(token):
    """Page to confirm a local user's email address.

    The token to confirm the email address must be a JSON web token obtained from
    :func:`request_email_confirmation`.
    """
    if not LocalProvider.is_registered() or (
        current_user.is_authenticated and current_user.identity.email_confirmed
    ):
        return redirect(url_for("main.index"))

    payload = LocalIdentity.decode_email_confirmation_token(token)

    if not payload:
        flash_danger(_("Token invalid or expired."))
        return redirect(url_for("main.index"))

    identity = LocalIdentity.query.get(payload["id"])

    if identity is not None and not identity.email_confirmed:
        update_object(identity, email=payload["email"], email_confirmed=True)
        db.session.commit()

        flash_success(_("Email confirmed successfully."))

    return redirect(url_for("main.index"))


@bp.route("/accept-legals", methods=["GET", "POST"])
@login_required
def request_legals_acceptance():
    """Page to request acceptance of all legal notices."""
    if not current_user.needs_legals_acceptance:
        return redirect(url_for("main.index"))

    form = LegalsAcceptanceForm()

    if form.validate_on_submit():
        current_user.accept_legals()
        db.session.commit()

        return redirect(url_for("main.index"))

    return render_template(
        "accounts/request_legals_acceptance.html",
        title=_("Accept legal notices"),
        form=form,
    )


@bp.get("/inactive-user")
@login_required
def inactive_user():
    """Page to redirect inactive users to."""
    if current_user.state == UserState.ACTIVE:
        return redirect(url_for("main.index"))

    return render_template("accounts/inactive_user.html", title=_("Account inactive"))


@bp.get("/users")
@login_required
def users():
    """User overview page.

    Allows users to filter for users.
    """
    return render_template("accounts/users.html", title=_("Users"))


@bp.get("/users/<int:id>")
@login_required
def view_user(id):
    """Page to view the profile of a user."""
    user = User.query.get_or_404(id)

    if user.is_merged:
        return redirect(url_for("accounts.view_user", id=user.new_user_id), code=301)

    return render_template("accounts/view_user.html", user=user, UserState=UserState)


@bp.get("/users/<int:id>/resources")
@login_required
def view_resources(id):
    """Page to view the created and shared resources of a user."""
    user = User.query.get_or_404(id)

    if user.is_merged:
        return redirect(
            url_for("accounts.view_resources", id=user.new_user_id), code=301
        )

    stats = None

    if user == current_user:
        files_query = user.files.filter(File.state == FileState.ACTIVE)
        local_file_size = (
            files_query.filter(File.storage_type == const.STORAGE_TYPE_LOCAL)
            .with_entities(db.func.sum(File.size))
            .scalar()
            or 0
        )
        local_file_size = filesize(local_file_size)

        # Add the user quota information to the formatted file size, if applicable.
        upload_user_quota = current_app.config["UPLOAD_USER_QUOTA"]

        if upload_user_quota is not None:
            local_file_size += f" / {filesize(upload_user_quota)}"

        num_records = user.records.filter(
            Record.state == RecordState.ACTIVE,
        ).count()
        num_collections = user.collections.filter(
            Collection.state == CollectionState.ACTIVE,
        ).count()
        num_templates = user.templates.filter(
            Template.state == TemplateState.ACTIVE,
        ).count()
        num_groups = user.groups.filter(
            Group.state == GroupState.ACTIVE,
        ).count()
        num_files = files_query.count()

        stats = {
            "num_records": format_number(num_records),
            "num_collections": format_number(num_collections),
            "num_templates": format_number(num_templates),
            "num_groups": format_number(num_groups),
            "num_files": format_number(num_files),
            "local_file_size": local_file_size,
        }

    return render_template(
        "accounts/view_resources.html",
        title=_("Resources"),
        user=user,
        stats=stats,
    )


@bp.get("/users/trash")
@login_required
def manage_trash():
    """Page for the current user to manage their deleted resources."""
    return render_template(
        "accounts/manage_trash.html", title=_("Trash"), user=current_user
    )
