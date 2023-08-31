from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms.models import modelform_factory
from django.apps import apps
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.db.models import Count

from .models import Course, Module, Content, Subject
from .forms import ModuleFormSet
from students.forms import CourseEnrollForm

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

    # dispatch 메서드는 url에서 클래스 기반 뷰를 호출할때 실행된다
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
    
class ContentCreateUpdateView(generic.base.TemplateResponseMixin, generic.base.View):
    module = None
    model = None
    obj = None
    template_name = 'courses/manage/content/form.html'

    def get_model(self,model_name):
        # 주어진 모델 이름이 네가지 콘텐츠 모델 중 하나인지 확인
        if model_name in ['text','video','image','file']:
            # Django의 apps 모듈을 사용하여 주어진 모델 이름에 해당하는 실제 클래스를 가져옴
            return apps.get_model(app_label='courses',model_name=model_name)
        # 모델이름이 유효하지 않은 경우 None 을 반환
        return None
    
    def get_form(self, model, *args, **kwargs):
        # modelform_factory() 함수를 사용하여 동적으로 폼을 생성 
        # exclude 매개변수를 사용하여 폼에서 제외할 공통 필드를 지정
        form_class = modelform_factory(model, exclude=['owner','order','created','updated'])
        return form_class(*args, **kwargs)
    
    # URL 매개변수를 받아 해당 모듈,모델 및 콘텐츠 객체를 클래스 속성으로 저장
    # module_id - 콘텐츠가 될 모듈의 ID
    # model_name - 생성, 업데이트할 콘텐츠의 모델 이름
    # id - 업데이트 중인 객체의 ID
    def dispatch(self, request, module_id, model_name, id=None):
        self.module = get_object_or_404(Module, id=module_id, course__owner=request.user)
        self.model = self.get_model(model_name)
        
        if id:
            self.obj = get_object_or_404(self.model, id=id, owner = request.user)
        return super().dispatch(request, module_id, model_name, id)
    
    # get 요청이 수신되었을 때 실행
    # 업데이트되는 인스턴스의 모델폼을 생성
    # 그렇지 않으면 새로운 객체를 생성하기 때문에 인스턴스를 지정하지 않고 빈폼을 생성(self.obj 가 None이기 때문)
    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form':form, 'object': self.obj})
    
    # post 요청이 수신되었들때 실행
    def post(self, request, module_id, model_name, id=None):
        # Text,Video, Image, File 모델에 대한 모델폼을 생성하고, 제출된 데이터와 파일을 폼에 전달하여 폼을검증
        form = self.get_form(self.model, instance=self.obj, data=request.POST, files=request.FILES)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()

            # id 매개변수를 확인하여 id가 제공되지 않은 경우 사용자가 기존 객체를 업데이트하는 대신 새로운 객체를 생성
            # 주어진 모듈에 대해 Content 객체를 생성하고 새 콘텐츠를 연결
            if not id:
                # new content
                Content.objects.create(module=self.module, item=obj)
                
            return redirect('module_content_list', self.module.id)
            
        return self.render_to_response({'form':form, 'object': self.obj})
    
class ContentDeleteView(generic.base.View):
    def post(self, request, id):
        content = get_object_or_404(Content, id=id, module__course__owner = request.user)
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('module_content_list', module.id)
    
class ModuleContentListView(generic.base.TemplateResponseMixin, generic.base.View):
    template_name = 'courses/manage/module/content_list.html'

    def get(self, request, module_id):
        module = get_object_or_404(Module, id=module_id, course__owner = request.user)

        return self.render_to_response({'module':module})
    
# 모듈의 순서를 업데이트하는 클래스뷰
class ModuleOrderView(CsrfExemptMixin,JsonRequestResponseMixin, generic.base.View):
    def post(self,request):
        for id, order in self.request_json.items():
            Module.objects.filter(id=id, course__owner=request.user).update(order=order)
        return self.render_json_response({'saved':'OK'})
    
# 모듈의 콘텐츠의 순서를 업데이트하는 클래스 뷰
class ContentOrderView(CsrfExemptMixin,JsonRequestResponseMixin,generic.base.View):
    def post(self,request):
        for id, order in self.request_json.items():
            Content.objects.filter(id=id, module__course__owner=request.user).update(order=order)
        return self.render_json_response({'saved':'OK'})
    
class CourseListView(generic.base.TemplateResponseMixin,generic.base.View):
    model = Course
    template_name = 'courses/course/list.html'

    def get(self, request, subject=None):
        subjects = Subject.objects.annotate(total_courses=Count('courses'))
        courses = Course.objects.annotate(total_modules=Count('modules'))

        if subject:
            subject  = get_object_or_404(Subject, slug=subject)
            courses = courses.filter(subject=subject)

        return self.render_to_response({'subjects':subjects, 'subject':subject, 'courses':courses})

class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'courses/course/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enroll_form'] = CourseEnrollForm(initial={'course':self.object})

        return context