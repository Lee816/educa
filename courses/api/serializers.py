from rest_framework import serializers

from ..models import Subject, Course, Module, Content

# 시리얼 라이저는 Django의 Form 및 ModelForm클래스와 유사한 방식으로 정의
# fields 속성을 설정하지 않으면 모든 필드가 포함된다.
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id','title','slug']

# 모듈 모델에 대한 직렬화
class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['order','title','description']
        
class CourseSerializer(serializers.ModelSerializer):
    # 모듈 시리얼라이저를 중첩
    # many =True 는 여러 객체를 직렬화하는 것을 나타낸다
    # read_only = True 는 이 필드는 읽기 전용이며 객체를 생성하거나 업데이트하는데 사용되지 않아야함을 나타낸다.
    modules = ModuleSerializer(many=True, read_only=True)
    class Meta:
        model = Course
        fields = ['id','subject','title','slug','overview','created','owner','modules']
        
class ItemRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return value.render()

class ContentSerializer(serializers.ModelSerializer):
    item = ItemRelatedField(read_only=True)

    class Meta:
        model = Content
        fields = ['order','item']
        
class ModuleWithContentsSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True)

    class Meta:
        model = Module
        fields = ['order','title','description','contents']

class CourseWithContentsSerializer(serializers.ModelSerializer):
    modules = ModuleWithContentsSerializer(many=True)

    class Meta:
        model = Course
        fields = ['id','subject','title','slug','overview','created','owner','modules']