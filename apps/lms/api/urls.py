from rest_framework import routers
from . import views


app_name = 'courses'


router = routers.DefaultRouter()
router.register('subjects', views.SubjectReadOnlyViewSet)
router.register('courses', views.CourseReadOnlyViewSet)

urlpatterns = router.urls
