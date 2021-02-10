from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from ..mixins import LoginEndIsEnrollToCourseMixin
from ..models import Course
from ..forms import CourseEnrollForm


class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    """
    Обработчик записи студента на курс.
    """
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('lms:student_course_detail', args=[self.course.id])


class StudentCourseListView(LoginEndIsEnrollToCourseMixin, ListView):
    """
    Обработчик для вывода курсов, на которые записан студент.
    """
    model = Course
    template_name = 'lms/student_course/student_course_list.html'
    paginate_by = 10


class StudentCourseDetailView(LoginEndIsEnrollToCourseMixin, DetailView):
    """
    Обработчик для вывода деталей курса, на который записан студент.
    """
    model = Course
    template_name = 'lms/student_course/student_course_detail.html'
