from django.urls import path
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register('', views.FollowerListViewSet, basename='followers')


urlpatterns = [

    path('<int:pk>', views.FollowerActionAPIView.as_view()),

]

urlpatterns += router.urls
