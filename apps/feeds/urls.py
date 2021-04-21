from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register('', views.FeedViewSet, basename='feeds')

urlpatterns = router.urls

