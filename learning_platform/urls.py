from django.conf.urls.static import static
from django.urls import path
from .api import *
from .views import *

urlpatterns = [
    path('api/user', UserView.as_view(), name='api_user'),
    path('api/profile', ProfileView.as_view(), name='api_profile'),
    path('api/register', RegisterView.as_view(), name='api_register'),
    path('api/login', LoginView.as_view(), name='api_login'),
    path('api/logout', LogoutView.as_view(), name='api_logout'),
    path('api/courses', CourseListView.as_view(), name='api_course_list'),
    path('api/user-courses', UserCoursesAPIView.as_view(), name='api_user-courses'),

    path('api/add-teacher', AddTeacherView.as_view(), name='api_add_teacher'),
    path('api/users', UserListView.as_view(), name='api_users_list'),

    path('api/courses/<int:course_id>', CourseManageAPIView.as_view(), name='api_course_detail'),
    path('api/courses/create', CourseManageAPIView.as_view(), name='api_course_create'),

    path('api/sections/<int:section_id>', SectionManageAPIView.as_view(), name='section-manage'),
    path('api/sections/<int:course_id>/add', SectionManageAPIView.as_view(), name='section-manage'),

    path('api/content-items/<int:content_id>', ContentItemManageAPIView.as_view(), name='content-item-manage'),
    path('api/content-items/<int:section_id>/add', ContentItemManageAPIView.as_view(), name='content-item-add'),

    path('api/courses/<int:course_id>/<str:action>', CourseEnrollmentAPIView.as_view(), name='course-enroll-withdraw'),

    path('', index, name='index'),
    path('profile', profile, name='profile'),
    path('login', login, name='login'),
    path('register', register, name='register'),
    path('courses', course_list, name='courses'),
    path('teacher-manager', teacher_manager, name='teacher_manager'),
    path('courses/create', course_create, name='add_course'),
    path('courses/<int:course_id>', course_details, name='course_details'),
    path('courses/<int:course_id>/edit', course_edit, name='course_edit'),
    path('sections/<int:section_id>/edit', section_edit, name='section_edit'),
    path('content/<int:section_id>/create', add_content, name='add_content'),
    path('content/<int:content_id>/edit', content_edit, name='content-edit'),
    path('content/<int:content_id>/view', content_view, name='content-view'),
]

# This serves media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
