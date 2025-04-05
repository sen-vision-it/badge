from rest_framework import serializers
from users.models import User
import re


def validate_email(value):
    if not value.endswith('@example.com'):
        raise serializers.ValidationError("Email must be from domain @example.com")
    return value


def validate_password(value):
    # Exemple de règles fortes : 8+ caractères, majuscule, minuscule, chiffre
    if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$', value):
        raise serializers.ValidationError(
            "Password must contain at least 1 uppercase, 1 lowercase, and 1 digit."
        )
    return value


class UserSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle User.
    Permet de convertir les objets utilisateur en JSON et vice versa.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField(min_length=2)
    last_name = serializers.CharField(min_length=2)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'role', 'phone_number']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
