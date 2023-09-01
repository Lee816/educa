from rest_framework import generics

from ..models import Subject
from .serializers import SubjectSerializer

class SubjectListView(generics.ListAPIView):
    # 객체를 검색하기 위해 사용할 기본 QuerySet
    queryset = Subject.objects.all()
    # 객체를 직렬화 하기 위한 클래스
    serializer_class = SubjectSerializer

class SubjectDetailView(generics.RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer