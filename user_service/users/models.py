from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class CustomUser(AbstractUser):
    """
    Modèle d'utilisateur personnalisé basé sur le modèle Django User.
    Ajoute un champ `role` pour définir le type d'utilisateur.
    """
    role = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_verified = models.BooleanField(default=False)  # Vérification email/téléphone

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Ajoutez un related_name unique
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions_set',  # Ajoutez un related_name unique
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return f"{self.username} ({self.role})"
