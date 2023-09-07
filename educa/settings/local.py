# 로컬 환경에 대한 사용자 지정 설정

import os, json

from .base import *

with open(os.path.join(BASE_DIR, "secret.json")) as f:
    secret = json.loads(f.read())


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": secret['DB_NAME'],
        "USER": secret['DB_USER'],
        "PASSWORD": secret['DB_PASSWORD'],
    }
}

if DEBUG:
    import mimetypes
    mimetypes.add_type('application/javascript','.js',True)
    mimetypes.add_type('text/css','.css',True)