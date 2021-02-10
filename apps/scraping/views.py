from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic

from .forms import FindForm, VacancyModelForm
from .models import Vacancy


class VacancyFindFormView(generic.FormView):
    """
    Обработчик вывода формы для поиска вакансии.
    """

    form_class = FindForm
    template_name = 'scraping/vacancy/vacancy_find_form.html'


class VacancyListView(generic.ListView):
    """
    Обработчик вывода списка вакансий.
    """
    model = Vacancy
    template_name = 'scraping/vacancy/vacancy_list.html'
    form = FindForm()
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['city'] = self.request.GET.get('city')
        context['language'] = self.request.GET.get('language')
        context['form'] = self.form
        return context

    def get_queryset(self):
        city = self.request.GET.get('city')
        language = self.request.GET.get('language')
        qs = []
        if city or language:
            _filter = {}
            if city:
                _filter['city__slug'] = city
            if language:
                _filter['language__slug'] = language
            qs = Vacancy.objects.filter(**_filter).select_related('city', 'language')
        return qs


class VacancyDetailView(generic.DetailView):
    """
    Обработчик вывода информации об конкретной вакансии.
    """
    model = Vacancy
    template_name = 'scraping/vacancy/vacancy_detail.html'


class VacancyCreateView(generic.CreateView):
    """
    Обработчик вывода формы для создания вакансии.
    """
    model = Vacancy
    form_class = VacancyModelForm
    template_name = 'scraping/vacancy/vacancy_create_form.html'
    success_url = reverse_lazy('scraping:vacancy_find')


class VacancyUpdateView(generic.UpdateView):
    """
    Обработчик вывода формы для обновления вакансии.
    """
    model = Vacancy
    form_class = VacancyModelForm
    template_name = 'scraping/vacancy/vacancy_update_form.html'
    success_url = reverse_lazy('scraping:vacancy_find')


class VacancyDeleteView(generic.DeleteView):
    """
    Обработчик удаления вакансии.
    """
    model = Vacancy
    success_url = reverse_lazy('scraping:vacancy_find')

    def get(self, request, *args, **kwargs):
        messages.success(request, 'Запись успешно удалена.')
        return self.post(request, *args, **kwargs)
