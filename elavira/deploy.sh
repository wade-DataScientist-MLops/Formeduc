#!/bin/bash

# Script de déploiement FormEduc
echo "🚀 Déploiement FormEduc en cours..."

# Arrêter les conteneurs existants
echo "📦 Arrêt des conteneurs existants..."
docker-compose down

# Mettre à jour le code
echo "📥 Mise à jour du code..."
git pull origin main

# Nettoyer Docker si nécessaire
echo "🧹 Nettoyage Docker..."
docker system prune -f

# Rebuild et lancer
echo "🔨 Build et démarrage..."
docker-compose up --build -d

# Vérifier le statut
echo "✅ Vérification du statut..."
sleep 5
docker-compose ps

echo "🎉 Déploiement terminé !"
echo "🌐 Application disponible sur le port 3000"
