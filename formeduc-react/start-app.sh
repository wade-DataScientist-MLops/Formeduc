#!/bin/bash

# Script de démarrage pour l'application Formeduc React
echo "🚀 Démarrage de l'application Formeduc React..."

# Vérifier si Node.js est installé
if ! command -v node &> /dev/null; then
    echo "❌ Node.js n'est pas installé. Veuillez l'installer depuis https://nodejs.org/"
    exit 1
fi

# Vérifier si npm est installé
if ! command -v npm &> /dev/null; then
    echo "❌ npm n'est pas installé. Veuillez l'installer avec Node.js"
    exit 1
fi

# Vérifier si le backend FastAPI est en cours d'exécution
echo "🔍 Vérification du backend FastAPI..."
if curl -s http://localhost:8000/ > /dev/null; then
    echo "✅ Backend FastAPI détecté sur le port 8000"
else
    echo "⚠️  Backend FastAPI non détecté sur le port 8000"
    echo "   Veuillez démarrer votre backend FastAPI avec :"
    echo "   cd ../elavira/backend && uvicorn main:app --reload"
    echo ""
    echo "   L'application React démarrera quand même, mais les fonctionnalités de chat ne fonctionneront pas."
    echo ""
fi

# Installer les dépendances si nécessaire
if [ ! -d "node_modules" ]; then
    echo "📦 Installation des dépendances..."
    npm install
fi

# Démarrer l'application React
echo "🎯 Démarrage de l'application React sur http://localhost:3000"
echo "   Appuyez sur Ctrl+C pour arrêter l'application"
echo ""

npm start

