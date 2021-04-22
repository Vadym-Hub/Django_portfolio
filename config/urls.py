from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
import debug_toolbar

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title='Portfolio by Pashynskyi',
      default_version='v1',
      description='API for portfolio',
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="vadym.is.pashynskyi@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),  # Django admin
    # Local apps.
    path('', include('base.urls')),
    path('accounts/', include('accounts.urls')),
    path('blog/', include('blog.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('travels/', include('travels.urls')),
    path('products/', include('products.urls')),
    path('orders/', include('orders.urls')),
    path('crm/',  include('crm.urls')),
    path('lms/', include('lms.urls')),
    path('scraping/', include('scraping.urls')),
    # API urls.
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include('routers')),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += path('__debug__/', include(debug_toolbar.urls)),
