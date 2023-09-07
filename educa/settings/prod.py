# 프로덕션 환경을 위한 사용자 지정 설정

from .base import *

DEBUG = False

# 예외가 발생하면 모든 정보가 관리 설정에 나열된 사람들에게 이메일로 전송
ADMINS = [
    ('Lee', 'asddsa124@naver.com'),
]

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default' : {
        
    }
}