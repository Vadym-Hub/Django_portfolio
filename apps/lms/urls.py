from django.urls import path
from . import views


app_name = 'lms'

urlpatterns = [
    path('', views.CourseListView.as_view(), name='course_list'),

    path('subject/<slug:subject_slug>/', views.CourseListView.as_view(), name='course_list_by_subject'),
    path('preview/<slug:slug>/', views.PreviewCourseDetailView.as_view(), name='course_detail'),

    path('owner/', views.ManageCourseListView.as_view(), name='manage_course_list'),
    path('create/', views.CourseOwnerCreateView.as_view(), name='course_owner_create'),
    path('<pk>/update/', views.CourseOwnerUpdateView.as_view(), name='course_owner_update'),
    path('<pk>/delete/', views.CourseOwnerDeleteView.as_view(), name='course_owner_delete'),

    path('<pk>/module/', views.ModuleEditView.as_view(), name='module_edit'),

    path('module/<int:module_id>/content/<model_name>/create/', views.ContentCreateUpdateView.as_view(), name='module_content_create'),
    path('module/<int:module_id>/content/<model_name>/<id>/', views.ContentCreateUpdateView.as_view(),  name='module_content_update'),
    path('content/<int:id>/delete/', views.ContentDeleteView.as_view(), name='module_content_delete'),
    path('module/<int:module_id>/', views.ModuleContentListView.as_view(), name='module_content_list'),


    path('student/enroll-course/', views.StudentEnrollCourseView.as_view(), name='enroll_to_course'),
    path('student/courses/', views.StudentCourseListView.as_view(), name='student_course_list'),
    path('student/course/<pk>/', views.StudentCourseDetailView.as_view(), name='student_course_detail'),
    path('student/course/<pk>/<module_id>/', views.StudentCourseDetailView.as_view(), name='student_course_detail_module'),
]
