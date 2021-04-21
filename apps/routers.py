from django.urls import path, include
from rest_framework import routers


router = routers.SimpleRouter()


urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('', include('accounts.api.urls')),
    path('posts/', include('posts.urls')),
    path('feeds/', include('feeds.urls')),
    path('followers/', include('followers.urls')),

    path('lms/', include('lms.api.urls')),
]

urlpatterns += router.urls
