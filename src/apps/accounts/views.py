from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from .forms import CustomUserCreationForm, CustomUserEditForm


User = get_user_model()


class UserSignupView(generic.CreateView):
    """
    Обработчик регистрации пользователя.
    """
    form_class = CustomUserCreationForm
    template_name = 'registration/signup_form.html'
    success_url = reverse_lazy('accounts:login')


# def logout_view(request):
#     """
#     Выход из системы.
#     """
#     logout(request)
#     return redirect('home')

class UserProfileDetailView(LoginRequiredMixin, generic.DetailView):
    """
    Обработчик вывода профиля пользователя.
    """
    template_name = 'accounts/profile_detail.html'

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class UserProfileEditView(LoginRequiredMixin, generic.UpdateView):
    """
    Обработчик редактирования профиля пользователя.
    """
    form_class = CustomUserEditForm
    template_name = 'accounts/profile_edit_form.html'
    success_url = reverse_lazy('accounts:profile')
