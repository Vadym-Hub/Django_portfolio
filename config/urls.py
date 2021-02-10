"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
import debug_toolbar

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),

    # Local apps
    path('', include('base.urls')),

    path('accounts/', include('accounts.urls')),

    path('blog/', include('blog.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    # 1 URL для путешественника.
    path('travels/', include('travels.urls')),
    # 2 URLs для магазина.
    path('products/', include('products.urls')),
    path('orders/', include('orders.urls')),
    # 1 URL для CRM.
    path('crm/',  include('crm.urls')),
    # 1 URL для LRM.
    path('lms/', include('lms.urls')),
    # 1 URL для scraping.
    path('scraping/', include('scraping.urls')),


    path('api_lms/v1/', include('lms.api.urls')),

]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns