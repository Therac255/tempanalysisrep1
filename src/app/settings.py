# This file was generated using http://github.com/f213/django starter template.
#
# Settings are split into multiple files using http://github.com/sobolevn/django-split-settings

from split_settings.tools import include

from app.conf.environ import env

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG', cast=bool, default=False)
CI = env('CI', cast=bool, default=False)

ORDER_EXPIRE_STATUS_COUNTDOWN = env('ORDER_STATUS_EXPIRE_COUNTDOWN', default=1800)

include(
    'conf/api.py',
    'conf/auth.py',
    'conf/boilerplate.py',
    'conf/db.py',
    'conf/healthchecks.py',
    'conf/http.py',
    'conf/i18n.py',
    'conf/installed_apps.py',
    'conf/middleware.py',
    'conf/static.py',
    'conf/media.py',
    'conf/storage-aws.py',
    'conf/sentry.py',
    'conf/templates.py',
    'conf/timezone.py',
    'conf/ckeditor.py',
    'conf/email.py',
    'conf/payments.py',
    'conf/export-import.py',
    'conf/celery_conf.py',
    "conf/logging.py"
)


try:
    from app.settings_local import *
except ImportError:
    pass
