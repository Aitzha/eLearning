from django.contrib.auth import authenticate, login, logout
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import UserProfile
from .serializers import UserSerializer, UserProfilePrivateSerializer, UserProfilePublicSerializer


class ProfileView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfilePrivateSerializer(user_profile)
        return Response(serializer.data)


class RegisterView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response()
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response()