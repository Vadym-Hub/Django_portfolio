from django.urls import path, include

from . import views

app_name = 'accounts'

urlpatterns = [
    # Базовые URLs авторизации (путь: from django.contrib.auth.urls).
    path('', include('django.contrib.auth.urls')),
    # path('logout/', views.logout_view, name='logout'),
    # URL регистрации пользователя.
    path('signup/', views.UserSignupView.as_view(), name='signup'),
    # URL редактирования пользователя.
    path('<int:pk>/', views.UserProfileDetailView.as_view(), name='profile'),
    # URL редактирования пользователя.
    path('<int:pk>/edit/', views.UserProfileEditView.as_view(), name='profile_edit'),
]
