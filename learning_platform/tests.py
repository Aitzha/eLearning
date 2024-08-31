from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token

from .model_factories import UserFactory, UserProfileFactory
from .models import *
from .units import user_has_permission


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


class PermissionUtilityTests(APITestCase):
    def test_user_has_permission_true(self):
        """User with permission should return True"""

        # Get add_course permission
        add_course_perm = Permission.objects.get(codename='add_course')

        # Create user, role and assign them to user profile
        teacher_role = Role.objects.create(name="Teacher")
        teacher_role.permissions.add(add_course_perm)
        teacher = User.objects.create_user(username='teacher', password='teacher123')
        UserProfile.objects.create(user=teacher, role=teacher_role)

        # Check the output
        self.assertTrue(user_has_permission(teacher, 'add_course'))

    def test_user_has_permission_false(self):
        """User without permission should return False"""

        # Create user, role and assign them to user profile
        student_role = Role.objects.create(name="Student")
        student = User.objects.create_user(username='student', password='student123')
        UserProfile.objects.create(user=student, role=student_role)

        # Check the output
        self.assertFalse(user_has_permission(student, 'add_course'))
