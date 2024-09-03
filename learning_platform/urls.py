from django.urls import path
from .api import *
from .views import *

urlpatterns = [
    path('api/user/', UserView.as_view(), name='api_user'),
    path('api/profile/', ProfileView.as_view(), name='api_profile'),
    path('api/register/', RegisterView.as_view(), name='api_register'),
    path('api/login/', LoginView.as_view(), name='api_login'),
    path('api/logout/', LogoutView.as_view(), name='api_logout'),
    path('api/course/create', CourseCreateView.as_view(), name='api_course_create'),
    path('api/courses/', CourseListView.as_view(), name='api_course_list'),

    path('', index, name='index'),
    path('profile/', profile, name='profile'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('courses/', courses, name='courses')
]
