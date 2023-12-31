from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.template.loader import render_to_string

from .fields import OrderField

# Create your models here.

class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['title']

    def __str__(self) -> str:
        return self.title

class Course(models.Model):
    # 이 강좌를 생성한 강사
    owner = models.ForeignKey(User, related_name='courses_created', on_delete=models.CASCADE)
    # 이 강좌가 속한 주제
    subject = models.ForeignKey(Subject, related_name='courses',on_delete=models.CASCADE)
    # 강좌의 제목
    title = models.CharField(max_length=200)
    # 강좌의 슬러그 ( URL 에서 사용 )
    slug = models.SlugField(max_length=200, unique=True)
    # 강좌에 대한 개요
    overview = models.TextField()
    # 강좌가 생성된 날짜와 시간
    created = models.DateTimeField(auto_now_add=True)
    
    students = models.ManyToManyField(User, related_name='courses_joined', blank=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title
    

class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules',on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # course를 사용해 코스에 따른 정렬을 계산한다고 명시
    # 이렇게 하면 새 모듈의 정렬은 동일한 코스 객체의 마지막 모듈에 1을 더하여 할당
    order = OrderField(blank=True,for_fields=['course'])

    def __str__(self) -> str:
        return f'{self.order}. {self.title}'
    
    # 기본 정렬 추가
    class Meta :
        ordering = ['order']
    
class Content(models.Model):
    module = models.ForeignKey(Module, related_name='contents',on_delete=models.CASCADE)
    # ContentType 모델을 가리키는 필드
    # limit_choices_to 를 이용해 content_type 개체를 제한
    # model__in 필드 조회를 사용하여 다음 네가지 속성을 가진 ContentType 개체의 쿼리를 필터링
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE,limit_choices_to={'model__in':('text','video','image','file')})
    # 관련 개체의 기본 키를 저장하는 필드
    object_id = models.PositiveIntegerField()
    # 두개의 필드를 결합하여 개체를 직접 검색하거나 설정할 수 있는 필드
    item = GenericForeignKey('content_type','object_id')
    
    order = OrderField(blank=True, for_fields=['module'])
    
    class Meta:
        ordering = ['order']
    
class ItemBase(models.Model):
    # 콘텐츠를 생성한 사용자
    owner = models.ForeignKey(User,related_name='%(class)s_related',on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        # 추상모델로 정의
        abstract = True

    def __str__(self) -> str:
        return self.title
    
    def render(self):
        # render_to_string 함수는 템플릿을 렌더링하고 렌더링된 내용을 문자열로 반환
        # self._mata.model_name을 사용하여 동적으로 각 콘텐츠 모델에 대한 템플릿 이름을 생성
        return render_to_string(f'courses/content/{self._meta.model_name}.html',{'item':self})

# 텍스트 콘텐츠를 저장하기 위한 모델
class Text(ItemBase):
    content = models.TextField()

# PDF와 같은 파일을 저장하기 위한 모델
class File(ItemBase):
    file = models.FileField(upload_to='files')

# 이미지 파일을 저장하기 위한 모델
class Image(ItemBase):
    file = models.FileField(upload_to='images')

# 비디오를 저장하기 위해 URLField 필드를 사용하여 비디오 URL을 임베드하기 위한 모델
class Video(ItemBase):
    url = models.URLField()