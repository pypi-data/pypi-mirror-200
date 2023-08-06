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
from collections import OrderedDict

from flask_babel import lazy_gettext as _l


# All additional access token scopes that are not tied to any resource permissions.
ACCESS_TOKEN_SCOPES = {
    "user": ["read"],
    "misc": ["manage_trash"],
}


# All available prefixes to distinguish different types of access tokens.
ACCESS_TOKEN_PREFIX_OAUTH = "oat_"
ACCESS_TOKEN_PREFIX_PAT = "pat_"


# All API versions that are currently available.
API_VERSIONS = ["v1"]


# Name of the attribute to store the API documentation meta dictionary in view functions
# for use in the API documentation.
APIDOC_META_ATTR = "__apidoc__"

# Keys to store various information in the API documentation meta dictionary.
APIDOC_EXPERIMENTAL_KEY = "experimental"
APIDOC_INTERNAL_KEY = "internal"
APIDOC_PAGINATION_KEY = "pagination"
APIDOC_QPARAMS_KEY = "qparams"
APIDOC_REQ_FORM_KEY = "reqform"
APIDOC_REQ_SCHEMA_KEY = "reqschema"
APIDOC_SCOPES_KEY = "scopes"
APIDOC_STATUS_CODES_KEY = "status_codes"
APIDOC_VERSIONS_KEY = "versions"


# Type values for all built-in authentication providers and identities.
AUTH_PROVIDER_TYPE_LDAP = "ldap"
AUTH_PROVIDER_TYPE_LOCAL = "local"
AUTH_PROVIDER_TYPE_SHIB = "shib"


# All currently available built-in authentication providers and their corresponding
# provider, identity and form classes.
AUTH_PROVIDER_TYPES = {
    AUTH_PROVIDER_TYPE_LOCAL: {
        "provider": "kadi.modules.accounts.providers.LocalProvider",
        "identity": "kadi.modules.accounts.models.LocalIdentity",
        "form": "kadi.modules.accounts.forms.CredentialsLoginForm",
    },
    AUTH_PROVIDER_TYPE_LDAP: {
        "provider": "kadi.modules.accounts.providers.LDAPProvider",
        "identity": "kadi.modules.accounts.models.LDAPIdentity",
        "form": "kadi.modules.accounts.forms.CredentialsLoginForm",
    },
    AUTH_PROVIDER_TYPE_SHIB: {
        "provider": "kadi.modules.accounts.providers.ShibProvider",
        "identity": "kadi.modules.accounts.models.ShibIdentity",
        "form": "kadi.modules.accounts.forms.ShibLoginForm",
    },
}


# Values for the possible Kadi environments.
ENV_DEVELOPMENT = "development"
ENV_PRODUCTION = "production"
ENV_TESTING = "testing"


# Currently supported export types with corresponding titles and file extensions for
# different resource types.
EXPORT_TYPES = {
    "record": OrderedDict(
        [
            ("json", {"title": "JSON", "ext": "json"}),
            ("pdf", {"title": "PDF", "ext": "pdf"}),
            ("qr", {"title": "QR Code", "ext": "png"}),
            ("rdf", {"title": "RDF (Turtle)", "ext": "ttl"}),
            ("ro-crate", {"title": "RO-Crate", "ext": "eln"}),
        ]
    ),
    "extras": OrderedDict(
        [
            ("json", {"title": "JSON", "ext": "json"}),
        ]
    ),
    "collection": OrderedDict(
        [
            ("json", {"title": "JSON", "ext": "json"}),
            ("qr", {"title": "QR Code", "ext": "png"}),
            ("rdf", {"title": "RDF (Turtle)", "ext": "ttl"}),
            ("ro-crate", {"title": "RO-Crate", "ext": "eln"}),
        ]
    ),
    "template": OrderedDict(
        [
            ("json", {"title": "JSON", "ext": "json"}),
            ("json-schema", {"title": "JSON Schema", "ext": "json"}),
        ]
    ),
}


# Maximum and minimum values for integers in the extra metadata. This way, the values
# are always safe for using them in JS contexts, where all numbers are 64 bit floating
# point numbers. This should probably be enough for most use cases, and as a positive
# side effect, all integer values are indexable by Elasticsearch.
EXTRAS_MAX_INTEGER = 2**53 - 1
EXTRAS_MIN_INTEGER = -EXTRAS_MAX_INTEGER


# All locales that are currently available with corresponding titles.
LOCALES = OrderedDict(
    [
        ("en", "English"),
        ("de", "Deutsch"),
    ]
)

# The default locale.
LOCALE_DEFAULT = "en"

# The name of the query parameter for selecting the current locale.
LOCALE_PARAM_NAME = "locale"


# Default MIME type for unspecified binary files.
MIMETYPE_BINARY = "application/octet-stream"

# Preferred MIME type for CSV files.
MIMETYPE_CSV = "text/csv"
# Preferred MIME type for JSON files.
MIMETYPE_JSON = "application/json"
# Preferred MIME type for XML files.
MIMETYPE_XML = "application/xml"

# Custom MIME type for dashboard files.
MIMETYPE_DASHBOARD = "application/x-dashboard+json"
# Custom MIME type for flow files to define workflows.
MIMETYPE_FLOW = "application/x-flow+json"
# Custom MIME type for tool files to be used within workflows.
MIMETYPE_TOOL = "application/x-tool+xml"

# Various other commonly used MIME types.
MIMETYPE_FORMDATA = "multipart/form-data"
MIMETYPE_HTML = "text/html"
MIMETYPE_JPEG = "image/jpeg"
MIMETYPE_JSONLD = "application/ld+json"
MIMETYPE_MD = "text/markdown"
MIMETYPE_PDF = "application/pdf"
MIMETYPE_PNG = "image/png"
MIMETYPE_TEXT = "text/plain"
MIMETYPE_TTL = "text/turtle"
MIMETYPE_ZIP = "application/zip"


# Supported MIME types for image uploads and direct image previews.
IMAGE_MIMETYPES = [MIMETYPE_JPEG, MIMETYPE_PNG]


# Active state value for all stateful models.
MODEL_STATE_ACTIVE = "active"
# Deleted state value for all stateful models. For the main resource types, this is used
# to represent soft deletion, but may have different semantics in other cases.
MODEL_STATE_DELETED = "deleted"

# Private visibility value for all supporting models.
MODEL_VISIBILITY_PRIVATE = "private"
# Public visibility value for all supporting models, usually used to grant default read
# permission.
MODEL_VISIBILITY_PUBLIC = "public"


# All currently registered OAuth2 grant types.
OAUTH_GRANT_AUTH_CODE = "authorization_code"
OAUTH_GRANT_REFRESH_TOKEN = "refresh_token"

# The single response type to allow for OAuth2 clients to request.
OAUTH_RESPONSE_TYPE = "code"

# The single method to allow for OAuth2 client authentication when requesting a token.
OAUTH_TOKEN_ENDPOINT_AUTH_METHOD = "client_secret_post"

# The single OAuth2 token type that is currently used.
OAUTH_TOKEN_TYPE = "Bearer"


# Amount of bytes (decimal interpretation).
ONE_KB = 1_000
ONE_MB = 1_000 * ONE_KB
ONE_GB = 1_000 * ONE_MB
ONE_TB = 1_000 * ONE_GB

# Amount of bytes (binary interpretation).
ONE_KIB = 1_024
ONE_MIB = 1_024 * ONE_KIB
ONE_GIB = 1_024 * ONE_MIB
ONE_TIB = 1_024 * ONE_GIB

# Amount of seconds.
ONE_MINUTE = 60
ONE_HOUR = 60 * ONE_MINUTE
ONE_DAY = 24 * ONE_HOUR
ONE_WEEK = 7 * ONE_DAY


# All currently available main resource types and their corresponding model class,
# schema class and other attributes.
RESOURCE_TYPES = OrderedDict(
    [
        (
            "record",
            {
                "model": "kadi.modules.records.models.Record",
                "schema": "kadi.modules.records.schemas.RecordSchema",
                "title": _l("Record"),
                "title_plural": _l("Records"),
                "endpoint": "records.records",
            },
        ),
        (
            "collection",
            {
                "model": "kadi.modules.collections.models.Collection",
                "schema": "kadi.modules.collections.schemas.CollectionSchema",
                "title": _l("Collection"),
                "title_plural": _l("Collections"),
                "endpoint": "collections.collections",
            },
        ),
        (
            "template",
            {
                "model": "kadi.modules.templates.models.Template",
                "schema": "kadi.modules.templates.schemas.TemplateSchema",
                "title": _l("Template"),
                "title_plural": _l("Templates"),
                "endpoint": "templates.templates",
            },
        ),
        (
            "group",
            {
                "model": "kadi.modules.groups.models.Group",
                "schema": "kadi.modules.groups.schemas.GroupSchema",
                "title": _l("Group"),
                "title_plural": _l("Groups"),
                "endpoint": "groups.groups",
            },
        ),
    ]
)


# Type values for all built-in storage providers.
STORAGE_TYPE_LOCAL = "local"


# Keys for global config items.
SYS_CONFIG_BROADCAST_MESSAGE = "BROADCAST_MESSAGE"
SYS_CONFIG_NAV_FOOTER_ITEMS = "NAV_FOOTER_ITEMS"
SYS_CONFIG_INDEX_IMAGE = "INDEX_IMAGE"
SYS_CONFIG_INDEX_TEXT = "INDEX_TEXT"

SYS_CONFIG_TERMS_OF_USE = "TERMS_OF_USE"
SYS_CONFIG_PRIVACY_POLICY = "PRIVACY_POLICY"
SYS_CONFIG_ENFORCE_LEGALS = "ENFORCE_LEGALS"
SYS_CONFIG_LEGAL_NOTICE = "LEGAL_NOTICE"

SYS_CONFIG_ROBOTS_NOINDEX = "ROBOTS_NOINDEX"


# All currently available system roles that group global actions of different resources.
SYSTEM_ROLES = {
    "admin": {
        "record": ["create", "read", "update", "link", "permissions", "delete"],
        "collection": ["create", "read", "update", "link", "permissions", "delete"],
        "template": ["create", "read", "update", "permissions", "delete"],
        "group": ["create", "read", "update", "members", "delete"],
    },
    "member": {
        "record": ["create"],
        "collection": ["create"],
        "template": ["create"],
        "group": ["create"],
    },
    "guest": {},
}


# Names of all currently available Celery tasks.
TASK_APPLY_ROLE_RULES = "kadi.permissions.apply_role_rules"
TASK_CLEAN_RESOURCES = "kadi.main.clean_resources"
TASK_MERGE_CHUNKS = "kadi.records.merge_chunks"
TASK_PUBLISH_RESOURCE = "kadi.resources.publish_resource"
TASK_PURGE_RECORD = "kadi.records.purge_record"
TASK_SEND_MAIL = "kadi.notifications.send_mail"


# URL of the ELN file format specification.
URL_ELN_SPEC = (
    "https://github.com/TheELNConsortium/TheELNFileFormat/blob/master/SPECIFICATION.md"
)

# URL from which the latest released Kadi version is retrieved.
URL_PYPI = "https://pypi.org/pypi/kadi/json"

# URLs where the documentation is hosted.
URL_RTD_STABLE = "https://kadi4mat.readthedocs.io/en/stable"
URL_RTD_LATEST = "https://kadi4mat.readthedocs.io/en/latest"


# Keys for user-specific config items.
USER_CONFIG_HIDE_INTRODUCTION = "HIDE_INTRODUCTION"
USER_CONFIG_HOME_LAYOUT = "HOME_LAYOUT"

# Default values for user-specific config items.
USER_CONFIG_HOME_LAYOUT_DEFAULT = [
    {"resource": "record", "visibility": "all", "creator": "any", "max_items": 6},
    {"resource": "collection", "visibility": "all", "creator": "any", "max_items": 4},
]


# Environment variables defined and used within Kadi.
VAR_API_BP = "KADI_IGNORE_API_BP_SETUP_CHECK"
VAR_CLI = "KADI_APP_FROM_CLI"
VAR_CONFIG = "KADI_CONFIG_FILE"
VAR_ENV = "KADI_ENV"
