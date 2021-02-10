from django.urls import path
from . import views


app_name = 'scraping'

urlpatterns = [
    path('list/', views.VacancyListView.as_view(), name='vacancy_list'),
    path('create/', views.VacancyCreateView.as_view(), name='vacancy_create'),
    path('detail/<int:pk>/', views.VacancyDetailView.as_view(), name='vacancy_detail'),
    path('update/<int:pk>/', views.VacancyUpdateView.as_view(), name='vacancy_update'),
    path('delete/<int:pk>/', views.VacancyDeleteView.as_view(), name='vacancy_delete'),
    path('', views.VacancyFindFormView.as_view(), name='vacancy_find'),
]
