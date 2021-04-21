from django.urls import path
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register('profiles', views.ProfileViewSet)
# router.register('groups', views.GroupViewSet, basename='groups')


urlpatterns = [

    path('profiles/avatar/', views.ProfileAvatarAPIView.as_view()),

]

urlpatterns += router.urls
