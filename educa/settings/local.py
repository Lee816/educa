# 로컬 환경에 대한 사용자 지정 설정
# 로컬 환경 서버 실행 환경변수 설정
# linux, macOS - export DJANGO_SETTINGS_MODULE = educa.settings.local
# window - set DJANGO_SETTINGS_MODULE = educa.settings.local

# 환경 변수 설정 전 실행 방법 - python manage.py runserver --settings=educa.settings.local
# 환경 변수 설정 후 실행 방법 - python manage.py runserver

import os, json

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / 'db.sqlite3',
    }
}

if DEBUG:
    import mimetypes
    mimetypes.add_type('application/javascript','.js',True)
    mimetypes.add_type('text/css','.css',True)