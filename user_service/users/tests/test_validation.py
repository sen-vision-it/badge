from rest_framework.test import APITestCase
from django.urls import reverse

class UserValidationTests(APITestCase):
    def test_invalid_email_domain(self):
        response = self.client.post(reverse('user-create'), {
            'email': 'invalid@gmail.com',
            'password': 'Strongpass1',
            'first_name': 'John',
            'last_name': 'Doe'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('email', response.data)

    def test_weak_password(self):
        response = self.client.post(reverse('user-create'), {
            'email': 'john@example.com',
            'password': '123456',
            'first_name': 'John',
            'last_name': 'Doe'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('password', response.data)
