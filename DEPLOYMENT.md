# 🚀 Guide de Déploiement Formeduc

## 📋 Prérequis

- Docker et Docker Compose installés
- Git configuré
- Accès au serveur VPS

## 🔧 Déploiement Local

### 1. Cloner le dépôt
```bash
git clone https://github.com/wade-DataScientist-MLops/Formeduc.git
cd Formeduc/elavira
```

### 2. Déployer avec Docker
```bash
# Déploiement automatique
./deploy-server.sh

# Ou déploiement manuel
docker-compose up --build -d
```

## 🌐 Services Disponibles

| Service | URL | Description |
|---------|-----|-------------|
| **React Frontend** | http://localhost:3000 | Interface moderne avec carrousel |
| **Streamlit Frontend** | http://localhost:8501 | Interface legacy (optionnel) |
| **Backend API** | http://localhost:8000 | API FastAPI |
| **Ollama** | http://localhost:11434 | Modèles IA |
| **PostgreSQL** | localhost:5432 | Base de données |

## 🐳 Conteneurs Docker

- `elavira-backend-1` : Backend FastAPI
- `elavira-frontend-react-1` : Frontend React
- `elavira-frontend-streamlit-1` : Frontend Streamlit (optionnel)
- `elavira-ollama-1` : Service Ollama
- `elavira-db-1` : Base de données PostgreSQL

## 🔄 Commandes Utiles

```bash
# Voir les logs
docker-compose logs -f

# Redémarrer un service
docker-compose restart frontend-react

# Arrêter tous les services
docker-compose down

# Voir le statut
docker-compose ps
```

## 🚀 Déploiement Production

### Variables d'environnement
Créer un fichier `.env` :
```env
POSTGRES_DB=elaviradb
POSTGRES_USER=mon_user
POSTGRES_PASSWORD=mon_password
REACT_APP_API_URL=http://votre-serveur:8000
```

### Déploiement sur VPS
```bash
# Sur le serveur
git pull origin main
cd elavira
./deploy-server.sh
```

## 🛠️ Dépannage

### Problèmes courants
1. **Port déjà utilisé** : Changer les ports dans docker-compose.yml
2. **Erreur de build** : Vérifier les Dockerfiles
3. **Connexion DB** : Vérifier les variables d'environnement

### Logs détaillés
```bash
docker-compose logs backend
docker-compose logs frontend-react
docker-compose logs ollama
```

## 📱 Accès Mobile

L'application React est responsive et accessible sur mobile via :
- http://votre-ip:3000
