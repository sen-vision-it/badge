# Service d'Authentification

Service microservice d'authentification et de gestion des utilisateurs avec RBAC (Role-Based Access Control).

## Fonctionnalités

- Gestion des utilisateurs avec authentification Auth0
- Système de rôles et permissions
- API REST sécurisée avec HTTPS
- Documentation API avec Swagger
- Tests unitaires, d'intégration et end-to-end
- Déploiement avec Docker et Kubernetes
- Journalisation et audit des actions
- Gestion robuste des erreurs

## Architecture

Le service est construit avec les technologies suivantes:

- **Backend**: Django & Django REST Framework
- **Base de données**: PostgreSQL
- **Authentification**: Auth0 JWT
- **Documentation API**: Swagger/OpenAPI
- **Conteneurisation**: Docker
- **Orchestration**: Kubernetes
- **Serveur web**: Nginx avec SSL/TLS

## Installation

### Avec Docker Compose

1. Clonez le dépôt:
```
git clone https://github.com/votre-organisation/service-authentication.git
cd service-authentication
```

2. Configurez le fichier `.env` (utilisez `.env.example` comme modèle)

3. Démarrez les conteneurs:
```
docker-compose up -d
```

4. Créez un superutilisateur:
```
docker-compose exec web python manage.py createsuperuser
```

### Déploiement sur Kubernetes

1. Configurez les secrets:
```
kubectl create namespace auth-system
kubectl apply -f kubernetes/secrets.yaml
kubectl apply -f kubernetes/configmap.yaml
```

2. Déployez les services:
```
kubectl apply -f kubernetes/
```

## Utilisation de l'API

L'API est documentée avec Swagger et accessible à l'adresse:
```
https://your-domain.com/swagger/
```

### Points d'entrée principaux:

- `/api/users/` - Gestion des utilisateurs
- `/api/roles/` - Gestion des rôles
- `/api/permissions/` - Gestion des permissions
- `/api/profile/` - Profil de l'utilisateur courant
- `/api/health/` - Vérification de l'état du service

## Tests

### Exécuter les tests unitaires:
```
python manage.py test
```

### Exécuter les tests avec couverture:
```
pytest --cov=service_authentication
```

## Sécurité

Le service est sécurisé avec:

- HTTPS (TLS 1.2+)
- Authentification JWT avec Auth0
- RBAC (contrôle d'accès basé sur les rôles)
- En-têtes de sécurité HTTP (HSTS, CSP, etc.)
- Journalisation d'audit

## Maintenance

### Mise à jour des dépendances:
```
pip install -r requirements.txt --upgrade
```

### Application des migrations:
```
python manage.py migrate
```

## Licence

Ce projet est sous licence propriétaire. Tous droits réservés.