from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework import status, views, generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
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
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.all().order_by('-username')
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


class UserCoursesAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Get the user's profile
            user_profile = request.user.profile
            can_add_courses = user_profile.role.permissions.filter(codename='add_course').exists()

            # Get courses created by the user (if they are allowed to add courses)
            user_courses = Course.objects.filter(teacher=user_profile) if can_add_courses else []

            # Use CourseSerializer to serialize the user_courses
            user_courses_data = CourseSerializer(user_courses, many=True).data

            return Response({
                'can_add_courses': can_add_courses,
                'user_courses': user_courses_data
            })
        except UserProfile.DoesNotExist:
            return Response({'error': 'User profile not found'}, status=404)


class CourseEnrollmentAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id, action):
        try:
            course = Course.objects.get(id=course_id)

            # Check if the user is the course creator
            if course.teacher == request.user.profile:
                return Response({'error': 'You cannot enroll/withdraw from your own course'}, status=400)

            # Handle the enrollment action
            if action == 'enroll':
                # Check if the user is already enrolled
                if Enrollment.objects.filter(course=course, student=request.user.profile).exists():
                    return Response({'error': 'You are already enrolled in this course'}, status=400)

                # Create a new enrollment
                Enrollment.objects.create(course=course, student=request.user.profile)
                return Response({'success': 'Enrolled successfully'}, status=200)

            elif action == 'withdraw':
                # Check if the user is enrolled in the course
                enrollment = Enrollment.objects.filter(course=course, student=request.user.profile).first()
                if not enrollment:
                    return Response({'error': 'You are not enrolled in this course'}, status=400)

                # Delete the enrollment
                enrollment.delete()
                return Response({'success': 'Withdrawn successfully'}, status=200)

            return Response({'error': 'Invalid action'}, status=400)

        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=404)


class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseManageAPIView(views.APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, course_id=None):
        if course_id:
            try:
                course = Course.objects.get(id=course_id)
                sections = course.sections.all()  # Assuming related name "sections"
                course_data = CourseSerializer(course).data
                sections_data = SectionSerializer(sections, many=True).data

                # Initialize values for unauthenticated users
                is_enrolled = False
                can_view_profile = False
                is_creator = False

                # Check if the user is authenticated
                if request.user.is_authenticated:
                    # Check if the user is the course creator
                    is_creator = course.teacher == request.user.profile
                    # Check if the user is enrolled in the course via the Enrollment model
                    is_enrolled = Enrollment.objects.filter(course=course, student=request.user.profile).exists()
                    # Check if the user has the 'can view profile' permission
                    can_view_profile = request.user.profile.role.permissions.filter(codename='view_profile').exists()

                return Response({
                    'course': course_data,
                    'sections': sections_data,
                    'is_creator': is_creator,
                    'is_enrolled': is_enrolled,
                    'can_view_profile': can_view_profile
                })
            except Course.DoesNotExist:
                return Response({'error': 'Course not found'}, status=404)

        return Response({'error': 'Course ID is required for GET'}, status=400)

    def post(self, request):
        data = request.data.copy()

        if not user_has_permission(request.user, 'add_course'):
            return Response({'error': 'You do not have permission to add courses.'}, status=status.HTTP_403_FORBIDDEN)

        data['teacher_id'] = request.user.profile.id

        serializer = CourseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
            if course.teacher != request.user.profile:
                return Response({'error': 'Permission denied'}, status=403)
            course.delete()
            return Response({'success': True}, status=200)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=404)


class SectionManageAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, section_id):
        try:
            section = Section.objects.get(id=section_id)
            content_items = ContentItem.objects.filter(section=section)
            content_items_data = [
                {
                    'id': content_item.id,
                    'title': content_item.title,
                    'content_type': content_item.content_type,
                    'file': content_item.file.url if content_item.file else None,
                    'video_url': content_item.video_url
                }
                for content_item in content_items
            ]

            return Response({'course_id': section.course_id, 'content_items': content_items_data}, status=200)
        except Section.DoesNotExist:
            return Response({'error': 'Section not found.'}, status=404)

    def post(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
            title = request.data.get('title')

            last_section = Section.objects.filter(course=course, next_section__isnull=True).first()

            new_section = Section.objects.create(
                title=title,
                course=course,
                previous_section=last_section
            )

            if last_section:
                last_section.next_section = new_section
                last_section.save()

            return Response({'success': True, 'section_id': new_section.id}, status=201)
        except Course.DoesNotExist:
            return Response({'error': 'You are not the course creator.'}, status=403)

    def put(self, request, section_id):
        try:
            section = Section.objects.get(id=section_id)
            section.title = request.data.get('title', section.title)
            section.save()
            return Response({'success': True}, status=200)
        except Section.DoesNotExist:
            return Response({'error': 'Section not found or you are not the course creator.'}, status=404)

    def delete(self, request, section_id):
        try:
            section = Section.objects.get(id=section_id)

            # Update the linked list pointers
            previous_section = section.previous_section
            next_section = section.next_section

            if previous_section:
                previous_section.next_section = next_section
                previous_section.save()

            if next_section:
                next_section.previous_section = previous_section
                next_section.save()

            # Delete the section
            section.delete()

            return Response({'success': True}, status=200)
        except Section.DoesNotExist:
            return Response({'error': 'Section not found or you are not the course creator.'}, status=404)


class ContentItemManageAPIView(views.APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, content_id):
        try:
            content_item = ContentItem.objects.get(id=content_id)
            serializer = ContentItemSerializer(content_item)
            return Response(serializer.data, status=200)
        except ContentItem.DoesNotExist:
            return Response({'error': 'Content item not found'}, status=404)

    def post(self, request, section_id):
        try:
            section = Section.objects.get(id=section_id)

            title = request.data.get('title')
            content_type = request.data.get('content_type')

            # Handling different content types
            if content_type == 'video':
                video_url = request.data.get('video_url')
                content_item = ContentItem.objects.create(
                    section=section,
                    title=title,
                    content_type='video',
                    video_url=video_url
                )
            elif content_type == 'pdf':
                file = request.FILES.get('file')
                content_item = ContentItem.objects.create(
                    section=section,
                    title=title,
                    content_type='pdf',
                    file=file
                )
            else:
                return Response({'error': 'Invalid content type.'}, status=400)

            return Response({'success': True, 'content_id': content_item.id}, status=201)
        except Section.DoesNotExist:
            return Response({'error': 'Section not found.'}, status=404)

    def put(self, request, content_id):
        try:
            content_item = ContentItem.objects.get(id=content_id)
            content_item.title = request.data.get('title', content_item.title)
            content_item.content_type = request.data.get('content_type', content_item.content_type)

            if content_item.content_type == 'video':
                # If it's video, update the video URL and clear the file
                content_item.video_url = request.data.get('video_url', content_item.video_url)
                content_item.file = None  # Clear file if switching to video
            elif content_item.content_type == 'pdf':
                # If it's a PDF, clear the video URL and upload the file
                content_item.video_url = None  # Clear video URL if switching to PDF
                if 'file' in request.FILES:
                    content_item.file = request.FILES['file']

            content_item.save()
            return Response({'success': True, 'section_id': content_item.section.id}, status=200)
        except ContentItem.DoesNotExist:
            return Response({'error': 'Content not found'}, status=404)

    def delete(self, request, content_id):
        try:
            content_item = ContentItem.objects.get(id=content_id)
            content_item.delete()
            return Response({'success': True}, status=200)
        except ContentItem.DoesNotExist:
            return Response({'error': 'Content item not found or you are not the course creator.'}, status=404)