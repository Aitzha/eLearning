from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .model_factories import UserFactory, UserProfileFactory


class ProfileViewTest(APITestCase):
    def test_profile_authenticated(self):
        self.user_profile = UserProfileFactory()
        self.client.force_authenticate(user=self.user_profile.user)
        response = self.client.get(reverse('api_profile'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_unauthenticated(self):
        response = self.client.get(reverse('api_profile'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class RegisterViewTest(APITestCase):
    def test_registration_successful(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword123'
        }
        response = self.client.post(reverse('api_register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_registration_unsuccessful(self):
        response = self.client.post(reverse('api_register'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginViewTest(APITestCase):
    def setUp(self):
        self.password = "password"
        self.user = UserFactory.create(password=self.password)
        self.client = APIClient()

    def test_login_successful(self):
        data = {
            'username': self.user.username,
            'password': self.password
        }
        response = self.client.post(reverse('api_login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_unsuccessful(self):
        data = {
            'username': self.user.username,
            'password': 'wrongpassword'
        }
        response = self.client.post(reverse('api_login'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class LogoutViewTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_logout(self):
        response = self.client.post(reverse('api_logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)