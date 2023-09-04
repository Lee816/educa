from rest_framework import generics, viewsets
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from ..models import Subject, Course
from .serializers import SubjectSerializer, CourseSerializer

class SubjectListView(generics.ListAPIView):
    # 객체를 검색하기 위해 사용할 기본 QuerySet
    queryset = Subject.objects.all()
    # 객체를 직렬화 하기 위한 클래스
    serializer_class = SubjectSerializer

class SubjectDetailView(generics.RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    

# class CourseEnrollView(APIView):
#     # 인증클래스 - 사용자는 HTTP 요청의 인증 헤더에 설정된 자격 증명으로 식별
#     authentication_classes = [BasicAuthentication]
#     # 익명의 사용자가 뷰에 액세스 할 수 없다.
#     permission_classes = [IsAuthenticated]
#     # POST 동작에 대한 메서드이며 다른 HTTP 메서드를 허용하지 않는다.
#     def post(self, request, pk, format=None):
#         # pk URL 변수를 사용하여 강좌를 가져온다.
#         course = get_object_or_404(Course, pk=pk)
#         # Course 객체의 학생 등록
#         course.students.add(request.user)
#         return Response({'enrolled':True})
    
# ReadOnlyModelViewSet 는 list() 와 retrieve()를 통해 객체 목록을 가져오거나 단일 객체를 검색하는 읽기 전용 동작
class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    
    # 데코레이터를 사용하여 추가 동작을 정의 detail=True 매개변수를 사용하여 이 동작을 단일 객체에 대해 수행되는 동작임을 지정
    # 이 동작에는 post() 메서드만 허용되며 인증 및 권한 클래스를 설정
    @action(detail=True, methods=['post'], authentication_classes=[BasicAuthentication], permission_classes=[IsAuthenticated])
    def enroll(self, request, *args, **kwargs):
        # self.get_object()를 사용하여 Course 객체를 가져온다.
        course = self.get_object()
        course.students.add(request.user)
        return Response({'enrolled':True})