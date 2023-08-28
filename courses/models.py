from django.db import models
from django.contrib.auth.models import User

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

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title
    

class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules',on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.title