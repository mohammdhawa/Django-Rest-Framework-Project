from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User


class RegisterTestCase(APITestCase):

    def test_register(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@test.com',
            'password': 'testPassword123',
            'password2': 'testPassword123'
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LoginLogoutTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@test.com', password='testPassword123')

        self.login_url = reverse('login')
        self.logout_url = reverse('logout')

    def test_login(self):
        data = {
            'username': 'testuser',
            'password': 'testPassword123'
        }

        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        # Log in to get tokens
        login_data = {
            'username': 'testuser',
            'password': 'testPassword123'
        }
        login_response = self.client.post(self.login_url, login_data)
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        # Extract tokens
        access_token = login_response.data.get('access')
        refresh_token = login_response.data.get('refresh')
        self.assertIsNotNone(access_token, "Access token not found in login response")
        self.assertIsNotNone(refresh_token, "Refresh token not found in login response")

        # Include the access token in the Authorization header
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # Make the logout request with the refresh token
        response = self.client.post(reverse('logout'), {"refresh": refresh_token}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)



