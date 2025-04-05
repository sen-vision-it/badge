from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import User


class UserAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.login(username='testuser', password='password123')

    def test_user_list(self):
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_change_role_as_admin(self):
        admin_user = User.objects.create_superuser(username="admin", password="adminpass")
        self.client.login(username='admin', password='adminpass')
        url = reverse('user-detail', args=[self.user.id]) + '/change_role/'
        response = self.client.patch(url, {'role': 'analyst'})
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.role, 'analyst')

    def test_logout(self):
        url = reverse('logout')
        response = self.client.post(url, {'refresh': 'valid-refresh-token'})
        self.assertEqual(response.status_code, 200)

    def test_permission_denied_for_non_admin(self):
        non_admin_user = User.objects.create_user(username="nonadmin", password="nonadminpass")
        self.client.login(username='nonadmin', password='nonadminpass')
        url = reverse('user-detail', args=[self.user.id]) + '/change_role/'
        response = self.client.patch(url, {'role': 'analyst'})
        self.assertEqual(response.status_code, 403)  # Forbidden
