from .base import *

import os

from .base import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-@==x%vz4gjnv2&4pn@@*_r&o2o4c&0+r*l0+#0kdjflm@!ybc2c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CORS_ALLOW_ALL_ORIGINS = True

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8080",
    "https://fup-env.eba-ijpp3mdu.us-east-1.elasticbeanstalk.com",
]

ALLOWED_HOSTS = [
    '*',
    'fup-env.eba-ijpp3mdu.us-east-1.elasticbeanstalk.com'
]

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fup',
        'USER': 'fup_admin',
        'PASSWORD': 'Inkcmh29lh0METFfaFB',
        'HOST': 'fup-database.c0l2au4w2p33.us-east-1.rds.amazonaws.com',
        'PORT': 3306
    }
}
