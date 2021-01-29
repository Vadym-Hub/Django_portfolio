from django.urls import path
from . import views
from . import feeds


app_name = 'blog'

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='article_list'),
    path('category/<slug:category_slug>/', views.ArticleListView.as_view(), name='article_list_by_category'),
    path('owner/', views.ArticleOwnerListView.as_view(), name='article_owner_list'),
    path('<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('create/', views.ArticleCreateView.as_view(), name='article_create'),
    path('<int:pk>/edit/', views.ArticleUpdateView.as_view(), name='article_edit'),
    path('<int:pk>/delete/', views.ArticleDeleteView.as_view(), name='article_delete'),
    path('search/', views.SearchView.as_view(), name='search'),

    path('<slug:category_slug>/', views.ArticleListView.as_view(), name='article_list_by_category'),

    path('tag/<slug:tag_slug>/', views.ArticleListView.as_view(), name='article_list_by_tag'),
    path('feed/', feeds.LatestArticlesFeed(), name='article_feed'),

]
