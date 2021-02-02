from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from ..models import Train


class TrainListView(generic.ListView):
    """
    Обработчик вывода списка поездов.
    """
    model = Train
    template_name = 'travels/train/train_list.html'
    paginate_by = 5


class TrainCreateView(SuccessMessageMixin, LoginRequiredMixin, generic.CreateView):
    """
    Обработчик вывода формы для создания поезда.
    """
    model = Train
    fields = ('name', 'from_city', 'to_city', 'travel_time',)
    template_name = 'travels/train/train_create_form.html'
    success_url = reverse_lazy('travels:train_list')
    success_message = 'Поезд создан!'
    login_url = '/accounts/login/'


class TrainUpdateView(SuccessMessageMixin, LoginRequiredMixin, generic.UpdateView):
    """
    Обработчик вывода формы для редактирования поезда.
    """
    model = Train
    fields = ('name', 'from_city', 'to_city', 'travel_time',)
    template_name = 'travels/train/train_update_form.html'
    success_url = reverse_lazy('travels:train_list')
    success_message = 'Поезд отредактирован!'
    login_url = '/accounts/login/'


class TrainDeleteView(SuccessMessageMixin, LoginRequiredMixin, generic.DeleteView):
    """
    Обработчик удаления поезда.
    """
    model = Train
    template_name = 'travels/train/train_confirm_delete.html'
    success_url = reverse_lazy('travels:train_list')
    success_message = 'Поезд удален!'
    login_url = '/accounts/login/'
