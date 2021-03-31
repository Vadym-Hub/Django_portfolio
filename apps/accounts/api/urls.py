from django.urls import path
from . import views


urlpatterns = [
    path('profile/<int:pk>/', views.ProfileViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
    path('<int:pk>/', views.ProfilePublicReadOnlyModelViewSet.as_view({'get': 'retrieve'})),
]
