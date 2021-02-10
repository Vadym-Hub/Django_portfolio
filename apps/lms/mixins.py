"""
Свои миксины.
"""
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class LoginEndIsOwnerCourseMixin(LoginRequiredMixin, PermissionRequiredMixin):
    """
    Миксин получает только объекты, владельцем которых
    является текущий пользователь, проверztn на логинизацию
    и автоматически заполняет поле owner в сохраняемых объектах.
    """

    def get_queryset(self):
        """
        Метод возвращает объекты, владельцем которых
        является текущий пользователь.
        """
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)

    def form_valid(self, form):
        """
        Метод автоматически заполняет  поле owner сохраняемого объекта.
        """
        form.instance.owner = self.request.user
        return super().form_valid(form)


class LoginEndIsEnrollToCourseMixin(LoginRequiredMixin):
    """
    Миксин получает только объекты, студентом которых
    является текущий пользователь с проверкой на логинизацию.
    """

    def get_queryset(self):
        """
        Метод возвращает объекты, студентом которых
        является текущий пользователь.
        """
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])
