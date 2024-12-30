from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from django.urls import reverse

from watchlist_app.api import serializers
from watchlist_app.models import StreamPlatform, WatchList, Review


class StreamPlatformTestCase(APITestCase):
    def setUp(self):
        self.super_user = User.objects.create_superuser(username='testuser',
                                                        email='testuser@test.com', password='testPassword123')
        self.normal_user = User.objects.create_user(username='testuser2', email='testuser2@test.com',
                                                    password='testPassword123')

        self.stream = StreamPlatform.objects.create(name="Netflix", about="This is an entertainment platform.",
                                                    website="https://www.netflix.com/")

    def test_streamplatform_create_with_admin(self):
        # Log in as admin
        login_data = {"username": "testuser", "password": "testPassword123"}
        login_response = self.client.post(reverse('login'), login_data)
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        # Set the access token for authenticated requests
        access_token = login_response.data.get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # Attempt to create a new stream platform
        data = {
            "name": "Netflix",
            "about": "This is an entertainment platform.",
            "website": "https://www.netflix.com/"
        }
        response = self.client.post(reverse('streamplatform-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_streamplatform_create_with_normal_user(self):
        # Loggin in as admin in order to create a watchlist
        login_data = {
            "username": "testuser2",
            "password": "testPassword123"
        }
        login_response = self.client.post(reverse('login'), login_data)
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        # Extract tokens
        access_token = login_response.data.get('access')
        refresh_token = login_response.data.get('refresh')
        self.assertIsNotNone(access_token, "Access token not found in login response")
        self.assertIsNotNone(refresh_token, "Refresh token not found in login response")

        # Include the access token in the Autherization header
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        data = {
            "name": "Netflix",
            "about": "this is an entertainment platform",
            "website": "https://www.netflix.com/"
        }

        response = self.client.post(reverse('streamplatform-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_streamplatform_list(self):
        resonse = self.client.get(reverse('streamplatform-list'))
        self.assertEqual(resonse.status_code, status.HTTP_200_OK)

    def test_streamplatform_retrieve(self):
        resonse = self.client.get(reverse('streamplatform-detail', args=[self.stream.id]))
        self.assertEqual(resonse.status_code, status.HTTP_200_OK)

    def test_streamplatform_update(self):
        # Loggin in as admin in order to create a watchlist
        login_data = {
            "username": "testuser",
            "password": "testPassword123"
        }
        login_response = self.client.post(reverse('login'), login_data)
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        # Extract tokens
        access_token = login_response.data.get('access')
        refresh_token = login_response.data.get('refresh')
        self.assertIsNotNone(access_token, "Access token not found in login response")
        self.assertIsNotNone(refresh_token, "Refresh token not found in login response")

        # Include the access token in the Autherization header
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        updated_data = {
            "name": "Netflix - updated",
            "about": "this is an entertainment platform - updated",
            "website": "https://www.netflix2.com/"
        }

        response = self.client.put(reverse('streamplatform-detail', args=(self.stream.id,)), updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_streamplatform_delete(self):
        # Loggin in as admin in order to create a watchlist
        login_data = {
            "username": "testuser",
            "password": "testPassword123"
        }
        login_response = self.client.post(reverse('login'), login_data)
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        # Extract tokens
        access_token = login_response.data.get('access')
        refresh_token = login_response.data.get('refresh')
        self.assertIsNotNone(access_token, "Access token not found in login response")
        self.assertIsNotNone(refresh_token, "Refresh token not found in login response")

        # Include the access token in the Autherization header
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        response = self.client.delete(reverse('streamplatform-detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class WatchListTestCase(APITestCase):
    def setUp(self):
        self.super_user = User.objects.create_superuser(username='testuser',
                                                        email='testuser@test.com', password='testPassword123')
        self.normal_user = User.objects.create_user(username='testuser2', email='testuser2@test.com',
                                                    password='testPassword123')
        self.stream = StreamPlatform.objects.create(name="Netflix", about="This is an entertainment platform.",
                                                    website="https://www.netflix.com/")
        self.watchlist = WatchList.objects.create(title="The Matrix", storyline="This is a storyline",
                                                  platform=self.stream, active=True, avg_rating=5.0, number_rating=100)

    def test_watchlist_create_with_normal_user(self):
        # Log in as admin
        login_data = {"username": "testuser2", "password": "testPassword123"}
        login_response = self.client.post(reverse('login'), login_data)
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        # Set the access token for authenticated requests
        access_token = login_response.data.get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        data = {
            "title": "The Matrix",
            "storyline": "This is a storyline",
            "platform": self.stream.id,
            "active": True,
            "avg_rating": 5.0,
            "number_rating": 100
        }

        response = self.client.post(reverse('watchlist'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_watchlist_create_with_admin_user(self):
        # Log in as admin
        login_data = {"username": "testuser", "password": "testPassword123"}
        login_response = self.client.post(reverse('login'), login_data)
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        # Set the access token for authenticated requests
        access_token = login_response.data.get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        data = {
            "title": "The Matrix",
            "storyline": "This is a storyline",
            "platform": self.stream.id,  # Use the ID of the stream platform
            "active": True
        }

        response = self.client.post(reverse('watchlist'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_watchlist_list(self):
        response = self.client.get(reverse('watchlist'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_watchlist_retrieve(self):
        response = self.client.get(reverse('watchlist-detail', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_watchlist_update(self):
        # Log in as admin
        login_data = {"username": "testuser", "password": "testPassword123"}
        login_response = self.client.post(reverse('login'), login_data)
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        # Set the access token for authenticated requests
        access_token = login_response.data.get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        data = {
            "title": "The Matrix - updated",
            "storyline": "This is a storyline - updated",
            "platform": self.stream.id,  # Use the ID of the stream platform
            "active": True
        }

        response = self.client.put(reverse('watchlist-detail', args=(self.watchlist.id, )), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_watchlist_delete(self):
        # Log in as admin
        login_data = {"username": "testuser", "password": "testPassword123"}
        login_response = self.client.post(reverse('login'), login_data)
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        # Set the access token for authenticated requests
        access_token = login_response.data.get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        response = self.client.delete(reverse('watchlist-detail', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
