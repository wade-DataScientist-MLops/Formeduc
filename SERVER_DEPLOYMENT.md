# 🚀 Guide de Déploiement sur Serveur VPS

## 📋 Instructions pour votre serveur VPS

### 1. Se connecter au serveur
```bash
ssh vps-25-8953@votre-serveur-ip
```

### 2. Aller dans le répertoire du projet
```bash
cd ~/Formeduc/elavira
```

### 3. Mettre à jour le code
```bash
git pull origin main
```

### 4. Arrêter les services existants
```bash
docker-compose down
```

### 5. Construire et démarrer les nouveaux services
```bash
docker-compose up --build -d
```

### 6. Vérifier le statut
```bash
docker-compose ps
docker-compose logs --tail=50
```

## 🔧 Configuration du docker-compose.yml

Le fichier `docker-compose.yml` a été mis à jour avec :

### ✅ Nouveaux services :
- **Ollama** : Service IA (port 11434)
- **Frontend React** : Interface moderne (port 3000)
- **Frontend Streamlit** : Interface legacy (port 8501)

### 🔄 Services existants :
- **Backend FastAPI** : API (port 8000)
- **PostgreSQL** : Base de données (port 5432)

## 🌐 URLs d'accès

| Service | URL | Description |
|---------|-----|-------------|
| **React (Nouveau)** | http://votre-ip:3000 | Interface moderne avec carrousel |
| **Streamlit (Legacy)** | http://votre-ip:8501 | Interface originale |
| **API Backend** | http://votre-ip:8000 | API FastAPI |
| **Ollama** | http://votre-ip:11434 | Service IA |

## 🛠️ Commandes de maintenance

```bash
# Voir les logs en temps réel
docker-compose logs -f

# Redémarrer un service spécifique
docker-compose restart frontend-react

# Voir l'utilisation des ressources
docker stats

# Nettoyer les images inutilisées
docker system prune -f
```

## 🔒 Sécurité

### Firewall (si nécessaire)
```bash
# Ouvrir les ports nécessaires
sudo ufw allow 3000  # React
sudo ufw allow 8000  # API
sudo ufw allow 8501  # Streamlit
sudo ufw allow 11434 # Ollama
```

### Variables d'environnement
Créer un fichier `.env` sur le serveur :
```env
POSTGRES_DB=elaviradb
POSTGRES_USER=mon_user
POSTGRES_PASSWORD=mon_password_secure
REACT_APP_API_URL=http://votre-ip:8000
```

## 📱 Accès mobile

L'application React est responsive et fonctionne sur mobile via :
- http://votre-ip:3000

## 🚨 Dépannage

### Problèmes courants :
1. **Port occupé** : Vérifier avec `netstat -tulpn | grep :3000`
2. **Erreur de build** : Vérifier les logs avec `docker-compose logs frontend-react`
3. **Connexion API** : Vérifier que le backend fonctionne sur le port 8000

### Logs détaillés :
```bash
# Logs de tous les services
docker-compose logs

# Logs d'un service spécifique
docker-compose logs frontend-react
docker-compose logs backend
docker-compose logs ollama
```

## ✅ Vérification du déploiement

1. **React** : http://votre-ip:3000 → Doit afficher le carrousel
2. **API** : http://votre-ip:8000/docs → Documentation Swagger
3. **Ollama** : http://votre-ip:11434 → Interface Ollama

## 🔄 Mise à jour future

Pour mettre à jour l'application :
```bash
cd ~/Formeduc/elavira
git pull origin main
docker-compose down
docker-compose up --build -d
```
