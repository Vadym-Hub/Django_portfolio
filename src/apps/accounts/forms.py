from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField, UserChangeForm

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """
    Кастомная форма регистрации нового пользователя.
    """

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        field_classes = {'username': UsernameField}


class CustomUserEditForm(UserChangeForm):
    """
    Форма редактирования пользователя.
    """

    class Meta:
        model = User
        fields = '__all__'
        field_classes = {'username': UsernameField}

