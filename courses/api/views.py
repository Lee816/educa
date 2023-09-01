from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from ..models import Subject, Course
from .serializers import SubjectSerializer

class SubjectListView(generics.ListAPIView):
    # 객체를 검색하기 위해 사용할 기본 QuerySet
    queryset = Subject.objects.all()
    # 객체를 직렬화 하기 위한 클래스
    serializer_class = SubjectSerializer

class SubjectDetailView(generics.RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    
class CourseEnrollView(APIView):
    # POST 동작에 대한 메서드이며 다른 HTTP 메서드를 허용하지 않는다.
    def post(self, request, pk, format=None):
        # pk URL 변수를 사용하여 강좌를 가져온다.
        course = get_object_or_404(Course, pk=pk)
        # Course 객체의 학생 등록
        course.students.add(request.user)
        return Response({'enrolled':True})