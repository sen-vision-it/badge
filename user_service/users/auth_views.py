from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
def logout(request):
    """
    Vue pour révoquer le token de l'utilisateur (Logout).
    Supprime le token Refresh pour empêcher toute nouvelle connexion avec l'ancien token.
    """
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()  # Ajoute le token à la liste noire
        return Response({"detail": "Déconnexion réussie."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
