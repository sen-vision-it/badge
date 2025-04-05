from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from .permissions import IsAdmin, IsAnalyst
from rest_framework import generics
from django.core.exceptions import PermissionDenied
from django.http import Http404


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['patch'], permission_classes=[IsAdminUser])
    def change_role(self, request, pk=None):
        user = self.get_object()
        new_role = request.data.get('role')
        if new_role not in dict(User.ROLE_CHOICES):
            return Response({"error": "Rôle invalide"}, status=status.HTTP_400_BAD_REQUEST)
        user.role = new_role
        user.save()
        return Response({"success": f"Rôle changé en {new_role}"})


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'username': user.username,
            'email': user.email,
            # Add other user fields as needed
        })


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Un jeton d'actualisation est requis"}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()  # Invalide le token

            return Response({"detail": "Déconnexion réussie"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AvailableRolesView(APIView):
    def get(self, request):
        roles = dict(User.ROLE_CHOICES)
        return Response(roles)


class AdminOnlyView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        return Response({"msg": f"Bienvenue Admin {request.user.username}"})


class AnalystOnlyView(APIView):
    permission_classes = [IsAnalyst]

    def get(self, request):
        return Response({"msg": f"Bienvenue Analyste {request.user.username}"})


class ForbiddenExampleView(APIView):
    def get(self, request):
        raise PermissionDenied("Vous n'êtes pas autorisé à accéder à cette ressource.")


class NotFoundExampleView(APIView):
    def get(self, request):
        raise Http404("Cette ressource n'existe pas.")
