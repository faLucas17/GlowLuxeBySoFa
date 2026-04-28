#!/usr/bin/env bash

echo "Début du déploiement sur Render..."

# Installer les dépendances
echo "Installation des dépendances..."
pip install -r requirements.txt

# Collecter les fichiers statiques
echo "Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

echo "Build terminé avec succès!"