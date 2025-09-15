#!/bin/bash

echo "🧹 NETTOYAGE COMPLET DU VPS - FormEduc"
echo "======================================"

# Arrêter tous les conteneurs
echo "1. Arrêt des conteneurs Docker..."
sudo docker-compose down 2>/dev/null || true

# Nettoyer Docker complètement
echo "2. Nettoyage Docker complet..."
sudo docker system prune -a -f --volumes

# Nettoyer les logs Docker
echo "3. Nettoyage des logs Docker..."
sudo find /var/lib/docker/containers -name "*-json.log" -exec truncate -s 0 {} \; 2>/dev/null || true

# Nettoyer le cache apt
echo "4. Nettoyage du cache apt..."
sudo apt clean
sudo apt autoremove -y

# Nettoyer les logs système
echo "5. Nettoyage des logs système..."
sudo journalctl --vacuum-time=1d

# Nettoyer le cache pip
echo "6. Nettoyage du cache pip..."
rm -rf ~/.cache/pip
rm -rf /root/.cache/pip

# Nettoyer les fichiers temporaires
echo "7. Nettoyage des fichiers temporaires..."
sudo rm -rf /tmp/*
sudo rm -rf /var/tmp/*

# Nettoyer les packages orphelins
echo "8. Nettoyage des packages orphelins..."
sudo apt autoremove --purge -y

# Vérifier l'espace disponible
echo "9. Espace disponible après nettoyage :"
df -h

echo "✅ Nettoyage terminé !"
echo "Vous pouvez maintenant essayer : sudo docker-compose up --build -d"
