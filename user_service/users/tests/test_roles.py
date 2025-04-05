import pytest
from rest_framework.test import APIClient
from users.models import User


@pytest.mark.django_db
def test_admin_can_change_role():
    admin = User.objects.create_user(username="admin", password="admin123", role="admin")
    target = User.objects.create_user(username="bob", password="pass123", role="user")

    client = APIClient()
    res = client.post("/api/login/", {"username": "admin", "password": "admin123"}, format="json")
    token = res.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    res = client.patch(f"/api/users/{target.id}/change_role/", {"role": "analyst"}, format="json")
    assert res.status_code == 200
    target.refresh_from_db()
    assert target.role == "analyst"


@pytest.mark.django_db
def test_non_admin_cannot_change_role():
    user = User.objects.create_user(username="user", password="pass123", role="user")
    target = User.objects.create_user(username="bob", password="pass123", role="user")

    client = APIClient()
    res = client.post("/api/login/", {"username": "user", "password": "pass123"}, format="json")
    token = res.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    res = client.patch(f"/api/users/{target.id}/change_role/", {"role": "admin"}, format="json")
    assert res.status_code == 403  # Forbidden


@pytest.mark.django_db
def test_get_roles_authenticated():
    user = User.objects.create_user(username="authuser", password="pass123")
    client = APIClient()
    res = client.post("/api/login/", {"username": "authuser", "password": "pass123"}, format="json")
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {res.data['access']}")

    res = client.get("/api/roles/")
    assert res.status_code == 200
    assert "admin" in res.data


@pytest.mark.django_db
def test_admin_only_endpoint_accessible_by_admin():
    admin = User.objects.create_user(username="admin", password="admin123", role="admin")
    client = APIClient()
    res = client.post("/api/login/", {"username": "admin", "password": "admin123"}, format="json")
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {res.data['access']}")

    res = client.get("/api/admin-only/")
    assert res.status_code == 200
    assert "Bienvenue Admin" in res.data["msg"]


@pytest.mark.django_db
def test_admin_only_endpoint_denied_for_user():
    user = User.objects.create_user(username="user", password="user123", role="user")
    client = APIClient()
    res = client.post("/api/login/", {"username": "user", "password": "user123"}, format="json")
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {res.data['access']}")

    res = client.get("/api/admin-only/")
    assert res.status_code == 403
