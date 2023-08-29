from django import forms
from django.forms.models import inlineformset_factory

from .models import Course, Module

# Django 에서 제공하는 inlineformset_factory()함수를 사용하여 생성
# 인라인 폼셋은 관련된 객체와 함께 작업하는 폼셋 위에 있는 작은 추상화 계틍이다.
# Course 객체와 관련된 Module 객체에 대한 모델 폼셋을 동적으로 생성
# fields - 폼셋의 각 폼에 포함될 필드들
# extra - 폼셋에 표시될 빈 추가 폼의 수를 설정
# can_delete - True로 설정하면 폼마다 체크박스 입력으로 렌더링되는 부울 필드를 포함
ModuleFormSet = inlineformset_factory(Course,Module, fields=['title','description'],extra=2,can_delete=True)
