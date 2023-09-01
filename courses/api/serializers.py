from rest_framework import serializers

from ..models import Subject

# 시리얼 라이저는 Django의 Form 및 ModelForm클래스와 유사한 방식으로 정의
# fields 속성을 설정하지 않으면 모든 필드가 포함된다.
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id','title','slug']