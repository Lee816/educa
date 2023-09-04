from rest_framework.permissions import BasePermission

class IsEnrolled(BasePermission):
    # 요청을 수행하는 사용자가 Course 객체의 students 관계에 있는지 확인
    def has_object_permission(self, request, view, obj):
        return obj.students.filter(id=request.user.id).exists()