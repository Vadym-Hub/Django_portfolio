from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from ..models import City


class CityListView(generic.ListView):
    """
    Обработчик вывода списка городов.
    """
    model = City
    template_name = 'travels/city/city_list.html'
    paginate_by = 5


class CityCreateView(SuccessMessageMixin, LoginRequiredMixin, generic.CreateView):
    """
    Обработчик вывода формы для создания города.
    """
    model = City
    fields = ('name',)
    template_name = 'travels/city/city_create_form.html'
    success_url = reverse_lazy('travels:city_list')
    success_message = 'Город создан!'
    login_url = '/accounts/login/'


class CityUpdateView(SuccessMessageMixin, LoginRequiredMixin, generic.UpdateView):
    """
    Обработчик вывода формы для редактирования города.
    """
    model = City
    fields = ('name',)
    template_name = 'travels/city/city_update_form.html'
    success_url = reverse_lazy('travels:city_list')
    success_message = 'Город отредактировано!'
    login_url = '/accounts/login/'


class CityDeleteView(SuccessMessageMixin, LoginRequiredMixin, generic.DeleteView):
    """
    Обработчик удаления города.
    """
    model = City
    template_name = 'travels/city/city_confirm_delete.html'
    success_url = reverse_lazy('travels:city_list')
    success_message = 'Город успешно удален!!'
    login_url = '/accounts/login/'

    # def get(self, request, *args, **kwargs):
    #     messages.success(request, 'Город успешно удален')
    #     return self.post(request, *args, **kwargs)
