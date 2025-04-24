import os

from .base import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-@==x%vz4gjnv2&4pn@@*_r&o2o4c&0+r*l0+#0tm_zm@!ybc2c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CORS_ALLOW_ALL_ORIGINS = True

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8080",
]

ALLOWED_HOSTS = [
    'localhost',
]

# INSTALLED_APPS += [
#     'debug_toolbar',
# ]

# DEBUG_TOOLBAR_CONFIG = {
#     "SHOW_TOOLBAR_CALLBACK": lambda request: True,
# }
# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('MYSQL_DATABASE'),
        'USER': os.environ.get('MYSQL_ROOT_USER'),
        'PASSWORD': os.environ.get('MYSQL_ROOT_PASSWORD'),
        'HOST': 'db',
        'PORT': 3306
    }
}

# email backend para desarrollo
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'].append('rest_framework.authentication.SessionAuthentication')

DJOSER.update({
    'EMAIL_FRONTEND_DOMAIN': 'localhost:8080',
    'EMAIL_FRONTEND_PROTOCOL': 'http'
})