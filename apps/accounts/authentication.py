"""
Кастомная аутентификация.
Позволяет входить в аккаутт как через username так и через e-mail.

Добавить в settings.py:
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # Проверка на авторизацию через (username, password)
    'accounts.authentication.EmailAuthBackend',  # Проверка на авторизацию через (email, password)
)
"""
from django.contrib.auth import get_user_model


User = get_user_model()


class EmailAuthBackend(object):
    """
    Выполняет аутентификацию пользователя по e-mail вместо username.
    """
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
