import os
from os import path

from .base import *

SECRET_KEY = '*piusv42ywk&=dy$xc$qmk$vch17zo2-kzxi0+d4o($yvy4wv-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(ROOT_DIR, 'db.sqlite3'),
    }
}

# EMAIL

EMAIL_HOST = "localhost"
EMAIL_PORT = 1025

# MEDIA
MEDIA_ROOT = path.join(ROOT_DIR, "development_media_storage")
MEDIA_URL = "/media/"
