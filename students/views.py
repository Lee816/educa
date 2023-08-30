from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms  import UserCreationForm
from django.contrib.auth import authenticate, login

# Create your views here.

class StudentRegistrationsView(generic.CreateView):
    template_name = 'students/student/registrations.html'
    # 객체를 생성하는데 사용되는 폼
    form_class = UserCreationForm
    # 폼이 성공적으로 제출된 후 연결될 url
    success_url = reverse_lazy('student_course_list')

    def form_valid(self,form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(usernae=cd['username'],password=cd['password'])
        login(self.request, user)
        return result