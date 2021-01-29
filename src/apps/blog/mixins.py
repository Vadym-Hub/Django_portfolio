from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class AuthorAndLoginRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Класс проверяет, что текущий пользователь аутентифицирован
    и является автором статьи.
    """

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user
