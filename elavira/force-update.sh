#!/bin/bash

echo "🔄 Force update du code sur le VPS..."

# Forcer la mise à jour
git fetch origin
git reset --hard origin/main

# Vérifier la correction
echo "🔍 Vérification de la correction..."
if grep -q "'Allergies ? Je réagis !'" backend/core/llm_loader.py; then
    echo "✅ Correction trouvée - guillemets simples utilisés"
else
    echo "❌ Correction non trouvée - problème persistant"
fi

# Rebuild et redémarrer
echo "🔨 Rebuild et redémarrage..."
docker-compose down
docker-compose up --build -d

echo "✅ Mise à jour forcée terminée !"
