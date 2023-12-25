from datetime import timedelta

from app.conf.environ import env
from app.settings import SECRET_KEY

# Django REST Framework
# https://www.django-rest-framework.org/api-guide/settings/

DISABLE_THROTTLING = env('DISABLE_THROTTLING', cast=bool, default=False)
MAX_PAGE_SIZE = env('MAX_PAGE_SIZE', cast=int, default=1000)

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': env('PAGE_SIZE', cast=int, default=100),
    'DEFAULT_THROTTLE_RATES': {
        'anon-auth': '10/min',
    },
    'EXCEPTION_HANDLER': 'app.api.exception_handler.custom_exception_handler'
}

SPECTACULAR_DEFAULTS = {
    'SERVE_PERMISSIONS': ['rest_framework.permissions.IsAuthenticatedOrReadOnly']
}
# ---------------------------------------------
# SIMPLE JWT settings
# ---------------------------------------------
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(days=1),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=7),
}

# Adding session auth and browsable API at the developer machine
if env('DEBUG', cast=bool, default=False):
    REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'].append('rest_framework.authentication.SessionAuthentication')
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'].append(
        'djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer')
