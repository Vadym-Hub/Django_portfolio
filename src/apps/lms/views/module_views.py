from django.shortcuts import get_object_or_404, redirect
from django.views import generic
from django.views.generic.base import TemplateResponseMixin

from ..forms import ModuleFormSet
from ..models import Course


# class ModuleEditView(generic.TemplateView):
class ModuleEditView(TemplateResponseMixin, generic.View):
    """
    Обрабатывает действия, связанные с набором форм по сохранению,
    редактированию и удалению модулей для конкретного курса.
    """
    template_name = 'lms/manage/module/module_form_set.html'
    course = None

    def get_formset(self, data=None):
        """
        Позволяет избежать дублирования кода,
        который отвечает за формирование набора форм.
        """
        return ModuleFormSet(instance=self.course, data=data)

    def dispatch(self, request, pk):
        """
        Если запрос отправлен с помощью GET, его обработка будет
        делегирована методу get() обработчика; если POST, то методу post().
        """
        self.course = get_object_or_404(Course, id=pk, owner=request.user)
        return super().dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        """
        Обрабатывает GET-запрос.
        """
        formset = self.get_formset()
        return self.render_to_response({'course': self.course,
                                        'formset': formset})

    def post(self, request, *args, **kwargs):
        """
        Обрабатывает POST-запросы.
        """
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('lms:manage_course_list')
        return self.render_to_response({'course': self.course,
                                        'formset': formset})
