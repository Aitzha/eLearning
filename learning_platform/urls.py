from django.urls import path
from .api import *
from .views import *

urlpatterns = [
    path('api/user', UserView.as_view(), name='api_user'),
    path('api/profile', ProfileView.as_view(), name='api_profile'),
    path('api/register', RegisterView.as_view(), name='api_register'),
    path('api/login', LoginView.as_view(), name='api_login'),
    path('api/logout', LogoutView.as_view(), name='api_logout'),
    path('api/course-create', CourseCreateView.as_view(), name='api_course_create'),
    path('api/courses', CourseListView.as_view(), name='api_course_list'),
    path('api/user-courses', UserCoursesAPIView.as_view(), name='api_user-courses'),
    path('api/courses/<int:course_id>', CourseDetailAPIView.as_view(), name='api_course_detail'),

    path('api/add-teacher', AddTeacherView.as_view(), name='api_add_teacher'),
    path('api/users', UserListView.as_view(), name='api_users_list'),

    # API endpoints to manage sections (create, update, delete)
    path('api/courses/<int:course_id>/sections', SectionManagementAPIView.as_view(), name='section-create'),
    path('api/sections/<int:section_id>', SectionManagementAPIView.as_view(), name='section-manage'),

    # API endpoints to manage content items (create, update, delete)
    path('api/sections/<int:section_id>/content-items', ContentItemManagementAPIView.as_view(), name='content-item-create'),
    path('api/content-items/<int:content_id>', ContentItemManagementAPIView.as_view(), name='content-item-manage'),

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
]
