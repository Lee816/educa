# 프로덕션 환경을 위한 사용자 지정 설정

import os
from .base import *

DEBUG = False

# 예외가 발생하면 모든 정보가 관리 설정에 나열된 사람들에게 이메일로 전송
ADMINS = [
    ('Lee', 'asddsa124@naver.com'),
]

ALLOWED_HOSTS = ['educaproject.com','www.educaproject.com']

DATABASES = {
    'default' : {
        'ENGINE' : 'django.db.backends.postgresql',
        'NAME' : os.environ.get('POSTGRES_DB'),
        'USER' : os.environ.get('POSTGRES_USER'),
        'PASSWORD' : os.environ.get('POSTGRES_PASSWORD'),
        'HOST' : 'db',
        'PORT' : 5432,
    }
}

REDIS_URL = 'redis://cache:6379'
CACHED['default']['LOCATION'] = REDIS_URL
CHANNEL_LAYERS['default']['CONFIG']['hosts'] = [REDIS_URL]