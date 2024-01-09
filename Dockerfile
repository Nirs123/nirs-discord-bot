# Utiliser une image Python officielle comme base
FROM python:3.8

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt dans le conteneur
COPY requirements.txt .

# Installer les dépendances spécifiées dans requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copier le fichier Python dans le conteneur
COPY main.py .

# Commande pour exécuter votre fichier Python
CMD ["python3", "main.py"]