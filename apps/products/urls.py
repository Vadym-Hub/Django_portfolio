from django.urls import path
from . import views


app_name = 'products'

urlpatterns = [
    # URLS продуктов.
    path('', views.ProductListView.as_view(), name='product_list'),
    path('<slug:category_slug>/', views.ProductListView.as_view(), name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
]