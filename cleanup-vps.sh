#!/bin/bash

echo "🧹 Nettoyage du VPS - Libération d'espace disque"
echo "=================================================="

# Vérifier l'espace avant nettoyage
echo "📊 Espace disque avant nettoyage :"
df -h

echo ""
echo "🗑️ Nettoyage des images Docker..."
docker system prune -a -f

echo ""
echo "🗑️ Nettoyage des volumes Docker..."
docker volume prune -f

echo ""
echo "🗑️ Nettoyage des builders Docker..."
docker builder prune -a -f

echo ""
echo "🗑️ Nettoyage des logs Docker..."
docker logs $(docker ps -aq) 2>/dev/null | head -0
docker system prune -f

echo ""
echo "🗑️ Nettoyage des caches pip..."
pip cache purge 2>/dev/null || echo "Pas de cache pip à nettoyer"

echo ""
echo "🗑️ Nettoyage des caches npm..."
npm cache clean --force 2>/dev/null || echo "Pas de cache npm à nettoyer"

echo ""
echo "🗑️ Suppression des node_modules..."
rm -rf /root/Formeduc/formeduc-react/node_modules 2>/dev/null || echo "node_modules déjà supprimé"

echo ""
echo "🗑️ Suppression des anciens builds..."
rm -rf /root/Formeduc/formeduc-react/build 2>/dev/null || echo "Build déjà supprimé"

echo ""
echo "🗑️ Nettoyage des fichiers temporaires..."
rm -rf /tmp/* 2>/dev/null || echo "Pas de fichiers temporaires à supprimer"

echo ""
echo "📊 Espace disque après nettoyage :"
df -h

echo ""
echo "✅ Nettoyage terminé !"
echo "💡 Vous pouvez maintenant essayer de rebuilder l'application"
