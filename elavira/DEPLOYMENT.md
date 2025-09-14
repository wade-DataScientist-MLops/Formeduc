# 🚀 Guide de Déploiement FormEduc

## 📋 Prérequis
- Docker et Docker Compose installés
- Git installé
- Permissions Docker configurées

## 🔧 Configuration des Permissions Docker

```bash
# Exécuter le script de correction des permissions
./fix-docker-permissions.sh

# Ou manuellement :
sudo usermod -aG docker $USER
sudo systemctl restart docker
newgrp docker  # Redémarrer la session
```

## 🚀 Déploiement Rapide

```bash
# Déploiement automatique
./deploy.sh
```

## 🔨 Déploiement Manuel

```bash
# 1. Arrêter les conteneurs
docker-compose down

# 2. Mettre à jour le code
git pull origin main

# 3. Nettoyer si nécessaire
docker system prune -f

# 4. Rebuild et lancer
docker-compose up --build -d

# 5. Vérifier le statut
docker-compose ps
```

## 🔍 Vérification

```bash
# Voir les logs
docker-compose logs

# Voir les logs du backend
docker-compose logs backend

# Voir les logs du frontend
docker-compose logs frontend

# Statut des conteneurs
docker-compose ps
```

## 🌐 Accès

- **Frontend** : http://localhost:3000
- **Backend API** : http://localhost:8000
- **Documentation API** : http://localhost:8000/docs

## 🆘 Dépannage

### Problème d'espace disque
```bash
# Nettoyer Docker
docker system prune -a -f --volumes
docker image prune -a -f
docker volume prune -f

# Nettoyer le système
sudo apt clean
sudo apt autoremove -y
```

### Problème de permissions Docker
```bash
# Vérifier les groupes
groups $USER

# Redémarrer Docker
sudo systemctl restart docker

# Tester sans sudo
docker ps
```

## 📊 Fonctionnalités

✅ **Elavira** - Assistante FormEduc optimisée selon le cahier des charges
✅ **Solenys** - Professeur québécois spécialisé PFEQ
✅ **Avatars personnalisés** - Images SVG pour chaque agent
✅ **Landing page** - Interface d'inscription inspirée de Limova.ai
✅ **Conversation memory** - Mémoire des conversations
✅ **Création d'agents** - Système de création d'agents personnalisés
✅ **Interface vocale** - Support audio (TTS/STT)

## 🎯 Tests

1. **Accéder à l'interface** : http://localhost:3000
2. **Tester Elavira** : "Bonjour, je suis éducatrice en CPE"
3. **Tester Solenys** : "Salut, j'ai besoin d'aide en mathématiques"
4. **Vérifier les avatars** : Les images doivent s'afficher correctement
5. **Tester la création d'agents** : Bouton "Créer un agent" sur le dashboard
