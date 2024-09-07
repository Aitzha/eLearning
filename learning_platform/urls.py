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

    path('', index, name='index'),
    path('profile', profile, name='profile'),
    path('login', login, name='login'),
    path('register', register, name='register'),
    path('courses', course_list, name='courses'),
    path('teacher-manager', teacher_manager, name='teacher-manager'),
    path('courses/create', course_create, name='course-create'),
    path('courses/<int:course_id>', course_details, name='course-details'),
]
