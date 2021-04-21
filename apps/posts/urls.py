from rest_framework.routers import SimpleRouter

from . import views


router = SimpleRouter()
router.register('', views.PostViewSet, basename='posts')
router.register('comments', views.CommentViewSet, basename='comments')

urlpatterns = router.urls
