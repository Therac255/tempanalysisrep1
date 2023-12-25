from app.conf.environ import env

AUTH_USER_MODEL = 'users.User'
AXES_ENABLED = env('AXES_ENABLED', cast=bool, default=False)

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesBackend',
    'users.backends.phone_backend.PhoneNumberAuthBackend',
    'users.backends.email_backend.EmailAuthBackend',
]

# Security notice: we use plain bcrypt to store passwords.
#
# We avoid django default pre-hashing algorithm
# from contrib.auth.hashers.BCryptSHA256PasswordHasher.
#
# The reason is compatibility with other hashing libraries, like
# Ruby Devise or Laravel default hashing algorithm.
#
# This means we can't store passwords longer then 72 symbols.
#
OTP_EXPIRATION_TIME = env('OTP_EXPIRATION_TIME', cast=int, default=60 * 5)
OTP_LENGTH = env('OTP_LENGTH', cast=int, default=6)

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]
