from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework import status, views, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token

from .models import UserProfile
from .serializers import *
from .units import user_has_permission, generate_random_password


class UserView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfilePublicSerializer(request.user.profile)

        response_content = serializer.data

        try:
            user_profile = UserProfile.objects.get(user=request.user)
            response_content['perms'] = [perm.codename for perm in user_profile.role.permissions.all()]
            return Response(response_content)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User profile not found'}, status=500)


class ProfileView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfilePrivateSerializer(request.user.profile)
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
        user = authenticate(username=username, password=password)
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'username': user.username})
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(views.APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class CourseCreateView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Create a mutable copy of request.data (to be able to modify it)
        data = request.data.copy()

        # Use the custom utility function to check permissions
        if not user_has_permission(request.user, 'add_course'):
            return Response({'error': 'You do not have permission to add courses.'}, status=status.HTTP_403_FORBIDDEN)

        # Set the teacher to the current user
        data['teacher'] = request.user.id

        serializer = CourseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class AddTeacherView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Check if the user has permission to create profiles (admin or similar)
        if not user_has_permission(request.user, 'add_userprofile'):
            return Response({'error': 'You do not have permission to add teachers.'}, status=status.HTTP_403_FORBIDDEN)

        # Ensure the "Teacher" role exists
        try:
            teacher_role = Role.objects.get(name="Teacher")
        except Role.DoesNotExist:
            return Response({'error': 'Teacher role does not exist'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Generate the username in the format "teacher-000-001"
        current_teacher_count = UserProfile.objects.filter(role=teacher_role).count()
        new_teacher_id = f"teacher-{str(current_teacher_count + 1).zfill(6)}"

        # Password generation logic (you can choose to generate a random password or set a default)
        password = generate_random_password(10)

        # Create the new user with the generated username and password
        try:
            with transaction.atomic():
                new_user = User.objects.create_user(username=new_teacher_id, password=password)
                new_user_profile = UserProfile.objects.create(user=new_user, role=teacher_role)

            return Response({
                'username': new_user.username,
                'password': password,
                'message': 'Teacher created successfully.'
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.all().order_by('username')
        role_name = self.request.query_params.get('role', None)
        username = self.request.query_params.get('username', None)

        # Filter by role if specified
        if role_name:
            try:
                role = Role.objects.get(name=role_name)
                queryset = queryset.filter(profile__role=role)
            except Role.DoesNotExist:
                return User.objects.none()

        # Filter by username if specified
        if username:
            queryset = queryset.filter(username__icontains=username)

        return queryset
