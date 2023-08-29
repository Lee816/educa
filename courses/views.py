from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Course
from .forms import ModuleFormSet

# Create your views here.

# 여러 클래스 기반 뷰에 특정 동작을 제공해야 할 때는 믹스인을 사용

# request.user에 해당하는 owner 속성을 기준으로 객체를 필터링
class OwnerMixin:
    # get_queryset() 메서드를 오버라이드하여 현재 사용자가 생성한 강좌만 검색하도록 설정
    # 사용자가 생성하지 않은 강좌를 편집, 업데이트, 삭제하는 것을 방지하기위해 
    # 생성,업데이트,삭제 뷰에도 get_queryset()메서드를 오버라이드 해야한다.
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)

# 폼 또는 모델폼을 사용하는 뷰에서 사용하는 form_valid()메서드를 구현
# 제출된 폼이 유효할 때 실행
class OwnerEditMixin:
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

# LoginRequiredMixin - login_required 데코레이터와 동일한 기능
# PermissionRequiredMixin - 특정 권한을 가진 사용자에게 뷰에 대한 접근 권한을 부여 ( permission_required 속성에 지정된 권한을 가진 사용자만 해당 뷰에 액세스)
class OwnerCourseMixin(OwnerMixin,LoginRequiredMixin, PermissionRequiredMixin):
    # QuerySet에 사용되는 모델, 모든 뷰에서 사용
    model = Course
    # CreateView 및 UpdateView 뷰의 모델 폼을 구성하는 모델의 필드
    fields = ['subject','title','slug','overview']
    # 폼이 성공적으로 제출되거나 객체가 삭제도니 후에 사용자를 리디렉션하기위해 사용
    success_url = reverse_lazy('manage_course_list')

class OwnerCourseEditMixin(OwnerCourseMixin,OwnerEditMixin):
    # CreateView 와 UpdateView 에 사용할 템플릿
    template_name = 'courses/manage/course/form.html'

class ManageCourseListView(OwnerCourseMixin, generic.ListView):
    template_name = 'courses/manage/course/list.html'
    permission_required = 'courses.view_course'

class CourseCreateView(OwnerCourseEditMixin, generic.CreateView):
    permission_required = 'courses.add_course'

class CourseUpdateView(OwnerCourseEditMixin, generic.UpdateView):
    permission_required = 'courses.change_course'

class CourseDeleteView(OwnerCourseMixin, generic.DeleteView):
    template_name = 'courses/manage/course/delete.html'
    permission_required = 'courses.delete_course'

# 특정 코스에 대한 모듈 추가, 업데이트, 삭제하기 위해 폼셋을 처리
# TemplateResponseMixin - 템플릿을 렌더링하고 HTTP 응답을 반환 render_to_response()메서드를 제공하고 이 메서드를 사용하여 컨텍스트를 전달하고 템플릿을 렌더링
# View - 기본 클래스 기반 뷰
class CourseModuleUpdateView(generic.base.TemplateResponseMixin, generic.base.View):
    template_name = 'courses/manage/module/formset.html'
    course = None

    # 폼셋을 구축하는 코드를 중복하지 않기 위한 메서드 주어진 코스 객체에 대한 ModuleFormSet객체를 생성하고 선택적으로 데이터를 전달
    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course, data=data)

    # View클래스에서 제공되는 메서드
    # HTTP 요청과 매개변수를 가져와서 사용된 HTTP 메서드와 일치하는 소문자 메서드에 위임 ex) GET -> get(), POST -> post()
    def dispatch(self, request, pk):
        # get 및 post 요청 모두에서 코스를 검색
        self.course = get_object_or_404(Course, id=pk, owner=request.user)
        return super().dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course':self.course, 'formset':formset})
    
    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response({'course':self.course, 'formset':formset})