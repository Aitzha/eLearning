from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token

from .model_factories import UserProfileFactory, RoleFactory, UserFactory
from .models import *
from .units import user_has_permission, generate_random_password


class UserViewAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_authenticated(self):
        # Preparation data
        user_profile = UserProfileFactory()
        token = Token.objects.create(user=user_profile.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # Send request
        response = self.client.get(reverse('api_user'))

        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], user_profile.user.username)
        self.assertEqual(response.data['role'], user_profile.role.name)

    def test_user_unauthenticated(self):
        # Send request
        response = self.client.get(reverse('api_user'))

        # Check response
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ProfileViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_profile_authenticated(self):
        # Preparation data
        user_profile = UserProfileFactory()
        token = Token.objects.create(user=user_profile.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # Send request
        response = self.client.get(reverse('api_profile'))

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], user_profile.user.username)
        self.assertEqual(response.data['email'], user_profile.user.email)
        self.assertEqual(response.data['role'], user_profile.role.name)

    def test_profile_unauthenticated(self):
        # Send request
        response = self.client.get(reverse('api_profile'))

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class RegisterViewTest(APITestCase):
    def test_registration_successful(self):
        # Preparation data
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword123'
        }

        # Send request
        response = self.client.post(reverse('api_register'), data)

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check Database
        user = User.objects.get(username=data['username'])
        user_profile = UserProfile.objects.get(user=user)
        self.assertNotEquals(None, user)
        self.assertNotEquals(None, user_profile)

    def test_registration_unsuccessful(self):
        # Send reqeust
        response = self.client.post(reverse('api_register'))

        # Check response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginViewTest(APITestCase):
    def setUp(self):
        self.password = "password"
        self.user = UserFactory.create(password=self.password)
        UserProfileFactory.create(user=self.user)
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()

    def test_login_successful(self):
        # Preparation data
        data = {
            'username': self.user.username,
            'password': self.password
        }

        # Send request
        response = self.client.post(reverse('api_login'), data)

        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['token'], self.token.key)
        self.assertEqual(response.data['username'], self.user.username)

    def test_login_unsuccessful(self):
        # Preparation data
        data = {
            'username': self.user.username,
            'password': 'wrongpassword'
        }

        # Send request
        response = self.client.post(reverse('api_login'), data)

        # Check response
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class LogoutViewTest(APITestCase):
    def test_logout(self):
        user_profile = UserProfileFactory()
        token = Token.objects.create(user=user_profile.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post(reverse('api_logout'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CourseCreateAPITests(APITestCase):
    def setUp(self):
        """Simple Setup before every test"""

        # Get URL
        self.url = reverse("api_course_create")

    def test_create_course_with_permission(self):
        """
        Testing course creation with the appropriate permissions and valid data.
        Should succeed and create new course in database.
        """

        # Get "add_course" permission
        self.add_course_perm = Permission.objects.get(codename='add_course')

        # Create role and assign it to user profile
        teacher_role = RoleFactory.create(name="Teacher")
        teacher_role.permissions.add(self.add_course_perm)
        teacher = UserProfileFactory.create(role=teacher_role)

        # Create and add credentials
        token = Token.objects.create(user=teacher.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # Create a data for new course
        data = {'title': 'New Course', 'description': 'A new course description'}

        # Send request
        response = self.client.post(self.url, data)

        # Check response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check Database
        self.assertEqual(Course.objects.count(), 1)
        self.assertEqual(Course.objects.first().title, 'New Course')

    def test_create_course_without_permission(self):
        """
        Testing course creation without permissions and valid data.
        Should fail and forbid endpoint access.
        """

        # Create user, role and assign them to user profile
        student_role = RoleFactory()
        student = UserProfileFactory.create(role=student_role)

        # Create and add credentials
        token = Token.objects.create(user=student.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # Create a data for new course
        data = {'title': 'Unauthorized Course', 'description': 'This should not be created'}

        # Send request
        response = self.client.post(self.url, data)

        # Check response
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Check Database
        self.assertEqual(Course.objects.count(), 0)

    def test_create_course_unauthorized(self):
        """
        Testing course creation unauthorized
        Should fail and block endpoint access.
        """

        # Send request
        response = self.client.post(self.url)

        # Check response
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PermissionUtilityTests(APITestCase):
    def test_user_has_permission_true(self):
        """
        Testing user with permission
        Should return True
        """

        # Get "add_course" permission
        add_course_perm = Permission.objects.get(codename='add_course')

        # Create role and assign it to user profile
        teacher_role = RoleFactory.create(name="Teacher")
        teacher_role.permissions.add(add_course_perm)
        teacher = UserProfileFactory.create(role=teacher_role)

        # Check the output
        self.assertTrue(user_has_permission(teacher.user, 'add_course'))

    def test_user_has_permission_false(self):
        """
        Testing user without permission
        Should return False
        """

        # Create role and assign it to user profile
        student_role = RoleFactory()
        student = UserProfileFactory.create(role=student_role)

        # Check the output
        self.assertFalse(user_has_permission(student.user, 'add_course'))


class CourseListPaginationAPITest(APITestCase):
        def setUp(self):
            """
            Setup before every test
            Permission:
                1) Get url to the endpoint
                2) Create teacher account
                3) Get page size from settings
                4) Create multiple courses
            """

            # Get url
            self.url = reverse('api_course_list')

            # Create teacher user profile
            teacher = UserProfileFactory()

            # Get page size from settings (create more course than page size by 1)
            self.page_size = settings.REST_FRAMEWORK['PAGE_SIZE']
            self.courses_number = self.page_size + 1

            # Create courses
            for i in range(self.courses_number):
                Course.objects.create(title=f'Course {i + 1}', description=f'Description {i + 1}',
                                      teacher=teacher)

        def test_pagination_works(self):
            """
            Test that pagination works correctly
            Should return the correct number of items per page
            """

            # Send request
            response = self.client.get(self.url)

            # Check the response
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn('results', response.data)
            self.assertIn('count', response.data)
            self.assertIn('next', response.data)
            self.assertIn('previous', response.data)

            self.assertEqual(response.data['count'], self.courses_number)
            self.assertEqual(len(response.data['results']), self.page_size)

        def test_next_page(self):
            """
            Test that the next page link works
            Should return the remaining courses
            """

            # Send first request to get url for next page
            first_page_response = self.client.get(self.url)

            # Send request using next page url
            response = self.client.get(first_page_response.data['next'])

            # Check the response
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data['results']), self.courses_number - self.page_size)

        def test_page_out_of_bounds(self):
            """
            Test requesting a page that is out of bounds
            Should return 404 error
            """

            # Send request (there can be only 2 pages)
            response = self.client.get(f'{self.url}?page=3')

            # Check response
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PasswordUtilityTests(APITestCase):
    def test_generate_password(self):
        """
        Testing random password generation
        Should return random password of given length
        """

        password_len = 10
        self.assertEqual(len(generate_random_password(password_len)), password_len)


class AddTeacherAPITests(APITestCase):
    def setUp(self):
        """
        Setup before every test
        Preparations:
            1) Get url to the endpoint
            2) Add Teacher role
            3) Get add user profile permission
        """

        # Get url
        self.url = reverse('api_add_teacher')

        # Set up roles
        self.teacher_role = Role.objects.create(name="Teacher")

        # Get add user profile permission
        self.add_userprofile_perm = Permission.objects.get(codename='add_userprofile')

    def test_create_teacher_successful(self):
        """
        Test teacher account creation with admin account
        Should successfully create teacher account
        """

        # Create role and assign it to user profile
        admin_role = Role.objects.create(name="Admin")
        admin_role.permissions.add(self.add_userprofile_perm)
        admin = UserProfileFactory.create(role=admin_role)

        # Create and add credentials
        token = Token.objects.create(user=admin.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # Send request
        response = self.client.post(self.url)

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('username', response.data)
        self.assertIn('password', response.data)

        # Check Database
        new_teacher_username = response.data['username']
        new_teacher = User.objects.get(username=new_teacher_username)
        new_teacher_profile = UserProfile.objects.get(user=new_teacher)
        self.assertTrue(new_teacher.username.startswith('teacher-'))
        self.assertEqual(new_teacher.username, response.data['username'])
        self.assertEqual(new_teacher_profile.role, self.teacher_role)

    def test_create_teacher_permission_denied(self):
        """
        Test teacher account creation without admin account
        Should forbid teacher account creation
        """

        # Create role and assign it to user profile
        teacher = UserProfileFactory.create(role=self.teacher_role)

        # Create and add credentials
        token = Token.objects.create(user=teacher.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # Send request
        response = self.client.post(self.url)

        # Check that permission is denied
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('error', response.data)

    def test_create_teacher_no_auth(self):
        """
        Test teacher account create unauthenticated
        Should forbid teacher account creation
        """

        # Send request
        response = self.client.post(self.url)

        # Check that the request is unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_teacher_no_teacher_role(self):
        """
        Test teacher creation when no teacher role exist
        Should return bad request error
        """

        # Delete Teacher role
        self.teacher_role.delete()

        # Create role and assign it to user profile
        admin_role = Role.objects.create(name="Admin")
        admin_role.permissions.add(self.add_userprofile_perm)
        admin = UserProfileFactory.create(role=admin_role)

        # Create and add credentials
        token = Token.objects.create(user=admin.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # Send request
        response = self.client.post(self.url)

        # Check response
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn('error', response.data)
