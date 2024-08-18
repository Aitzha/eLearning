from django.urls import path
from .api import ProfileView, RegisterView, LoginView, LogoutView
from .views import index

urlpatterns = [
    path('api/profile/', ProfileView.as_view(), name='profile'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),

    path('', index, name='index')
]
