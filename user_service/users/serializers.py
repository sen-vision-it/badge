from rest_framework import serializers
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle CustomUser.
    Permet de convertir les objets utilisateur en JSON et vice versa.
    """

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'phone_number', 'is_verified']
