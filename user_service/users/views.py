from rest_framework import viewsets
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status


class UserViewSet(viewsets.ModelViewSet):
    """
    Vue API REST pour gérer les utilisateurs.
    Autorise uniquement les utilisateurs authentifiés via JWT.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        user = request.user
        return Response({
            'username': user.username,
            'email': user.email,
            # Add other user fields as needed
        })


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Un jeton d'actualisation est requis"}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()  # Invalide le token

            return Response({"detail": "Déconnexion réussie"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
