from django.views.generic import TemplateView


class HomePageTemplateView(TemplateView):
    """
    Обработчик вывода базоврй страницы с инфо о проекте.
    """
    template_name = 'base/home.html'
