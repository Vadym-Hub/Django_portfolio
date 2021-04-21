from django.contrib.auth import get_user_model
from posts.models import Post


User = get_user_model()


class Feed:
    """
    Service feeds.
    """
    def get_post_list(self, user: User):
        """
        Оптимизированный запрос к БД (делает за 2 запроса) для ленты, достает
        список постов всех подпищиков, отфильтрованных по дате создания.
        """
        return Post.objects.filter(author__follow__subscriber=user).order_by(
            '-created').select_related('author').prefetch_related('comments')

    def get_single_post(self, pk: int):
        """
        Оптимизированный запрос к БД (делает 2 запроса) для ленты, достает один пост.
        """
        return Post.objects.select_related('author').prefetch_related('comments').get(id=pk)


feed_service = Feed()
