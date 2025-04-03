from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserProfileView, LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


# Création d'un routeur pour générer automatiquement les routes CRUD
router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Inclut toutes les routes API générées par le routeur
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh Token
    path("logout/", LogoutView.as_view(), name="logout"), # Logout
    path("profile/", UserProfileView.as_view(), name="user-profile"), # User Profile
]
