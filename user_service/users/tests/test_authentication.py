from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from users.models import User


class AuthTests(APITestCase):
    def test_login_success(self):
        user = User.objects.create_user(email="user@example.com", password="pass1234")
        response = self.client.post(reverse('token_obtain_pair'), {
            'email': 'user@example.com',
            'password': 'pass1234'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)

    def test_login_failure(self):
        response = self.client.post(reverse('token_obtain_pair'), {
            'email': 'nouser@example.com',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 401)
