# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

from app.conf.environ import env

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('POSTGRES_HOST', default='127.0.0.1'),
        'PORT': env('POSTGRES_PORT', default='5432'),
        'CONN_MAX_AGE': env('POSTGRES_CONN_MAX_AGE', cast=int, default=0),
    }
}
# https://docs.djangoproject.com/en/4.1/releases/3.2/#customizing-type-of-auto-created-primary-keys
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
