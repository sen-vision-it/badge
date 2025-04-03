# Utilisation de l’image officielle Python
FROM python:3.10

# Définition du dossier de travail
WORKDIR /app

# Copie des dépendances et installation
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source
COPY . .

# Exposer le port de Django
EXPOSE 8000

# Lancer le serveur Django
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]