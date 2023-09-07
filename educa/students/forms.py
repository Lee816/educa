from django import forms
from courses.models import Course

# 학생들이 코스에 등록하기 위해 사용
class CourseEnrollForm(forms.Form):
    # course 필드는 사용자가 등록될 코스이므로 ModelChoiceField
    # 이 폼은 CourseDetailView 뷰에서 등록버튼을 표시하는데 사용
    course = forms.ModelChoiceField(queryset=Course.objects.all(), widget=forms.HiddenInput)