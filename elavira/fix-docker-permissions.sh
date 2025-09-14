#!/bin/bash

# Script pour résoudre les permissions Docker
echo "🔧 Résolution des permissions Docker..."

# Ajouter l'utilisateur au groupe docker
echo "👤 Ajout de l'utilisateur au groupe docker..."
sudo usermod -aG docker $USER

# Redémarrer Docker
echo "🔄 Redémarrage du service Docker..."
sudo systemctl restart docker

# Tester Docker
echo "🧪 Test de Docker..."
sudo docker --version
sudo docker ps

echo "✅ Permissions Docker configurées !"
echo "💡 Redémarrez votre session SSH ou exécutez: newgrp docker"
