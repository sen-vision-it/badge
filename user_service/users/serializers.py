from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle User.
    Permet de convertir les objets utilisateur en JSON et vice versa.
    """

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'phone_number', 'is_verified']
