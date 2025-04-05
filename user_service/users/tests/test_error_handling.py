from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.core.exceptions import PermissionDenied


class ErrorHandlingTests(APITestCase):
    def test_permission_denied(self):
        #from users.views import ForbiddenExampleView
        response = self.client.get(reverse('forbidden-example'))  # URL à mapper
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response['Content-Type'], "application/problem+json")

    def test_not_found(self):
        response = self.client.get("/non/existant/route/")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response['Content-Type'], "application/problem+json")

    def test_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalid.jwt.token')
        response = self.client.get(reverse('user-profile'))  # endpoint protégé
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response['Content-Type'], "application/problem+json")

    def test_validation_error(self):
        response = self.client.post(reverse('user-create'), {
            "email": "not-an-email",
            "password": "short"
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response['Content-Type'], "application/problem+json")
