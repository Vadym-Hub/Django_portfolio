from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from django.views import generic

from ..forms import CourseEnrollForm, CourseModelForm
from ..mixins import LoginEndIsOwnerCourseMixin
from ..models import Course, Subject


class CourseListView(generic.ListView):
    """
    Обработчик отображения курсов.
    """
    template_name = 'lms/course/course_list.html'
    context_object_name = 'courses'
    paginate_by = 12

    def get_queryset(self):
        subject_slug = self.kwargs.get('subject_slug', None)
        queryset = Course.objects.all()
        if subject_slug:
            subject = get_object_or_404(Subject, slug=subject_slug)
            queryset = queryset.filter(subject=subject)
        return queryset


class PreviewCourseDetailView(generic.DetailView):
    """
    Обработчик, который выводит страницу курса.
    """
    model = Course
    template_name = 'lms/course/course_detail.html'

    def get_context_data(self, **kwargs):
        """
        Добавляем форму в контекст шаблона. Для записи пользователя на данный курс
        Объект формы содержит скрытое поле с ID курса, поэтому при нажатии кнопки
        на сервер будут отправлены данные курса и пользователя.
        """
        context = super().get_context_data(**kwargs)
        context['enroll_form'] = CourseEnrollForm(initial={'course': self.object})
        return context


class ManageCourseListView(LoginEndIsOwnerCourseMixin, generic.ListView):
    """
    Обработчик вывода курсов владельцем курса.
    """
    model = Course
    template_name = 'lms/manage/course/manage_course_list.html'
    permission_required = 'lms.view_course'
    success_url = reverse_lazy('lms:manage_course_list')


class CourseOwnerCreateView(LoginEndIsOwnerCourseMixin, generic.CreateView):
    """
    Обработчик для создания курса владельцу курса.
    """
    model = Course
    form_class = CourseModelForm
    template_name = 'lms/manage/course/course_create_form.html'
    permission_required = 'lms.add_course'
    success_url = reverse_lazy('lms:manage_course_list')


class CourseOwnerUpdateView(LoginEndIsOwnerCourseMixin, generic.UpdateView):
    """
    Обработчик для обновления курса владельцем курса.
    """
    model = Course
    form_class = CourseModelForm
    template_name = 'lms/manage/course/course_update_form.html'
    permission_required = 'lms.change_course'
    success_url = reverse_lazy('lms:manage_course_list')


class CourseOwnerDeleteView(LoginEndIsOwnerCourseMixin, generic.DeleteView):
    """
    Обработчик для удаления курса владельцем курса.
    """
    model = Course
    template_name = 'lms/manage/course/course_confirm_delete.html'
    permission_required = 'lms.delete_course'
    success_url = reverse_lazy('lms:manage_course_list')

