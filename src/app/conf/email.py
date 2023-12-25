from app.conf.environ import env

EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = env('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_USE_TLS = env('EMAIL_USE_TLS', cast=bool, default=True)
EMAIL_PORT = env('EMAIL_PORT', default='587')
EMAIL_USE_SSL = env('EMAIL_USE_SSL', cast=bool, default=False)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
