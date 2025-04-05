from django.test import TestCase
from .models import User
from rest_framework.test import APIClient
from django.urls import reverse


class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(username="testuser", password="password123")
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.check_password("password123"))


class UserAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_list(self):
        url = reverse('user-list')  # Assurez-vous que l'URL est définie dans `users/urls.py`
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
