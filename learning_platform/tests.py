from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .model_factories import UserFactory


class ProfileViewTest(APITestCase):
    def test_profile_authenticated(self):
        user = UserFactory()
        self.client.force_authenticate(user=user)
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_unauthenticated(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class RegisterViewTest(APITestCase):
    def test_registration_successful(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword123'
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_registration_unsuccessful(self):
        response = self.client.post(reverse('register'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginViewTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()

    def test_login_successful(self):
        data = {
            'username': self.user.username,
            'password': 'defaultpassword'  # This is the password set by factory
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_unsuccessful(self):
        data = {
            'username': self.user.username,
            'password': 'wrongpassword'
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class LogoutViewTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_logout(self):
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)