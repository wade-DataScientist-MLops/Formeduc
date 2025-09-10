#!/bin/bash

# Script de déploiement pour le serveur
echo "🚀 Déploiement de l'application Formeduc sur le serveur..."

# Aller dans le répertoire elavira
cd /Users/admin/Formeduc/elavira

# Arrêter les conteneurs existants
echo "🛑 Arrêt des conteneurs existants..."
docker-compose down

# Supprimer les anciennes images (optionnel)
echo "🗑️ Nettoyage des anciennes images..."
docker system prune -f

# Construire et démarrer les nouveaux conteneurs
echo "🔨 Construction et démarrage des nouveaux conteneurs..."
docker-compose up --build -d

# Vérifier le statut des conteneurs
echo "📊 Statut des conteneurs:"
docker-compose ps

# Afficher les logs
echo "📝 Logs des services:"
docker-compose logs --tail=50

echo "✅ Déploiement terminé!"
echo "🌐 Application React: http://localhost:3000"
echo "🌐 Application Streamlit: http://localhost:8501"
echo "🔧 Backend API: http://localhost:8000"
echo "🤖 Ollama: http://localhost:11434"
