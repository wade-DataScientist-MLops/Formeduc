#!/bin/bash

echo "🚀 Démarrage des applications Formeduc"
echo "======================================"

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages colorés
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Vérifier si Node.js est installé
if ! command -v node &> /dev/null; then
    print_error "Node.js n'est pas installé. Veuillez l'installer depuis https://nodejs.org/"
    exit 1
fi

# Vérifier si npm est installé
if ! command -v npm &> /dev/null; then
    print_error "npm n'est pas installé. Veuillez l'installer avec Node.js"
    exit 1
fi

print_status "Démarrage de l'application React..."

# Démarrer l'application React
cd /Users/admin/Formeduc/formeduc-react

# Vérifier si les dépendances sont installées
if [ ! -d "node_modules" ]; then
    print_status "Installation des dépendances React..."
    npm install
fi

print_success "Application React démarrée sur http://localhost:3000"
print_warning "Note: Le backend FastAPI n'est pas démarré. L'application fonctionne en mode démo."

echo ""
echo "🎉 Applications démarrées avec succès !"
echo "======================================"
echo "📱 Application React: http://localhost:3000"
echo "🎠 Carrousel d'images: Activé"
echo "👩‍🏫 Elavira & 🤖 Solenys: Prêts"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter l'application"

# Démarrer l'application React
npm start

