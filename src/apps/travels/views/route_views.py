from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from ..forms import RouteForm, RouteModelForm
from ..models import Route, City, Train
from ..services import get_routes


def home(request):
    """
    Обработчик вывода главной страницы.
    """
    form = RouteForm()
    return render(request, 'travels/home.html', {'form': form})


def find_route(request):
    """
    Обработчик поиска маршрута.
    """
    if request.method == "POST":
        form = RouteForm(request.POST)
        if form.is_valid():
            try:
                context = get_routes(request, form)
            except ValueError as e:
                messages.error(request, e)
                return render(request, 'travels/home.html', {'form': form})
            return render(request, 'travels/home.html', context)
        return render(request, 'travels/home.html', {'form': form})
    else:
        form = RouteForm()
        messages.error(request, 'Нет данных для поиска')
        return render(request, 'travels/home.html', {'form': form})


def add_route(request):
    """
    Обработчик добавления маршрута.
    """
    if request.method == 'POST':
        context = {}
        data = request.POST
        if data:
            total_time = int(data['total_time'])
            from_city_id = int(data['from_city'])
            to_city_id = int(data['to_city'])
            trains = data['trains'].split(',')
            trains_lst = [int(t) for t in trains if t.isdigit()]
            qs = Train.objects.filter(id__in=trains_lst).select_related('from_city', 'to_city')
            cities = City.objects.filter(id__in=[from_city_id, to_city_id]).in_bulk()
            form = RouteModelForm(initial={'from_city': cities[from_city_id],
                                           'to_city': cities[to_city_id],
                                           'travel_times': total_time,
                                           'trains': qs})
            context['form'] = form
        return render(request, 'travels/route/route_create_form.html', context)
    else:
        messages.error(request, 'Невозможно сохранить несуществующий маршрут')
        return redirect('/travels')


def save_route(request):
    """
    Обработчик сохранения маршрута.
    """
    if request.method == "POST":
        form = RouteModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Маршрут успешно сохранен")
            return redirect('/travels/route')
        return render(request, 'travels/route/route_create.html', {'form': form})
    else:
        messages.error(request, 'Невозможно сохранить несуществующий маршрут')
        return redirect('/travels')


class RouteListView(generic.ListView):
    """
    Обработчик списка списка маршрутов.
    """
    model = Route
    template_name = 'travels/route/route_list.html'
    paginate_by = 5


class RouteDetailView(generic.DetailView):
    """
    Обработчик вывода деталей маршрута.
    """
    model = Route
    template_name = 'travels/route/route_detail.html'


class RouteDeleteView(SuccessMessageMixin, LoginRequiredMixin, generic.DeleteView):
    """
    Обработчик удаления маршрута.
    """
    model = Route
    template_name = 'travels/route/route_confirm_delete.html'
    success_url = reverse_lazy('travels:route_list')
    success_message = 'Маршрут удален!'
    login_url = '/accounts/login/'



