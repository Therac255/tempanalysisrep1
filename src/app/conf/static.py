from app.conf.environ import env

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATICFILES_STORAGE = env('STATICFILES_STORAGE', cast=str, default='django.contrib.staticfiles.storage.StaticFilesStorage')
STATIC_URL = env('STATIC_URL', cast=str, default='/api/static/')
STATIC_ROOT = env('STATIC_ROOT', cast=str, default='static')
