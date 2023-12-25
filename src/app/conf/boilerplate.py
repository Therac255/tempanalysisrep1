import os.path

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ROOT_URLCONF = 'app.urls'

# Disable built-in ./manage.py test command in favor of pytest
TEST_RUNNER = 'app.test.disable_test_command_runner.DisableTestCommandRunner'

WSGI_APPLICATION = 'app.wsgi.application'

PHONENUMBER_DEFAULT_FORMAT = 'INTERNATIONAL'

SPECTACULAR_SETTINGS = {
    # available SwaggerUI versions: https://github.com/swagger-api/swagger-ui/releases
    "SWAGGER_UI_DIST": "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.3"  # latest version is broken
}
