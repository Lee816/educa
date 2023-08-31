from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms  import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CourseEnrollForm
from courses.models import Course

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
    
class StudentEnrollCourseView(LoginRequiredMixin, generic.FormView):
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('student_course_detail', args=[self.course.id])
    
class StudentCourseListView(LoginRequiredMixin, generic.ListView):
    model = Course
    template_name = 'students/course/list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in = [self.request.user])
    
class StudentCourseDetailView(generic.DetailView):
    model = Course
    template_name = 'students/course/detail.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in = [self.request.user])

    # module_id URL 매개변수가 주어지면 코스 모듈을 context에 설정
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        
        if 'module_id' in self.kwargs:
            context['module'] = course.modules.get(id=self.kwargs['module_id'])
        else:
            context['module'] = course.modules.all()[0]
        return context