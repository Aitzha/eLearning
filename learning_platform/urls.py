from django.urls import path
from .api import ProfileView, RegisterView, LoginView, LogoutView
from .views import index

urlpatterns = [
    path('api/profile/', ProfileView.as_view(), name='api_profile'),
    path('api/register/', RegisterView.as_view(), name='api_register'),
    path('api/login/', LoginView.as_view(), name='api_login'),
    path('api/logout/', LogoutView.as_view(), name='api_logout'),

    path('', index, name='index')
]
