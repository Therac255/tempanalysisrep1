from app.conf.environ import env

DEFAULT_FILE_STORAGE = env('DEFAULT_FILE_STORAGE', cast=str, default='django.core.files.storage.FileSystemStorage')
MEDIA_URL = env('MEDIA_URL', cast=str, default='/api/media/')
MEDIA_ROOT = env('MEDIA_ROOT', cast=str, default='media')
