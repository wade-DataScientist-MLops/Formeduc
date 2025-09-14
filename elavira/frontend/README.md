# Formeduc React - Application de Chat Intelligent

Cette application React moderne remplace l'interface Streamlit d'Elavira avec une expérience utilisateur améliorée et des fonctionnalités avancées.

## 🚀 Fonctionnalités

### Authentification
- **Connexion** : Interface de connexion sécurisée
- **Inscription** : Création de compte utilisateur
- **Gestion des sessions** : Persistance de la connexion

### Chat Intelligent
- **Deux assistants** :
  - **Elavira** : Spécialiste en formations et secourisme
  - **Solenys** : Assistant IA généraliste
- **Interface de chat moderne** avec bulles de messages stylisées
- **Suggestions de prompts** contextuelles
- **Historique des conversations** persistant

### Fonctionnalités Audio
- **Enregistrement vocal** : Cliquez sur le microphone pour enregistrer
- **Transcription automatique** : Conversion audio → texte
- **Synthèse vocale** : Lecture des réponses des assistants
- **Contrôle audio** : Activation/désactivation du son

### Design & UX
- **Interface responsive** : Adaptée à tous les écrans
- **Animations fluides** : Transitions et effets visuels
- **Thème moderne** : Design épuré et professionnel
- **Accessibilité** : Navigation au clavier et lecteurs d'écran

## 🛠️ Installation et Démarrage

### Prérequis
- Node.js (version 16 ou supérieure)
- Backend FastAPI d'Elavira en cours d'exécution sur le port 8000

### Installation
```bash
cd formeduc-react
npm install
```

### Démarrage en mode développement
```bash
npm start
```

L'application sera accessible sur `http://localhost:3000`

### Build de production
```bash
npm run build
```

## 🔧 Configuration

### Variables d'environnement
Créez un fichier `.env` à la racine du projet :

```env
REACT_APP_API_BASE_URL=http://localhost:8000
```

### Configuration du backend
Assurez-vous que votre backend FastAPI est configuré pour accepter les requêtes CORS depuis `http://localhost:3000`.

## 📁 Structure du Projet

```
src/
├── components/
│   ├── Auth/
│   │   └── AuthForm.tsx          # Formulaire d'authentification
│   └── Chat/
│       ├── ChatInterface.tsx     # Interface principale du chat
│       ├── MessageBubble.tsx     # Composant de bulle de message
│       ├── MessageInput.tsx      # Zone de saisie et contrôles
│       ├── AgentSelector.tsx     # Sélecteur d'assistant
│       └── SuggestedPrompts.tsx  # Suggestions de prompts
├── context/
│   └── AppContext.tsx            # Gestion d'état global
├── services/
│   └── api.ts                    # Services API
├── types/
│   └── index.ts                  # Types TypeScript
├── App.tsx                       # Composant principal
└── index.tsx                     # Point d'entrée
```

## 🔌 Intégration API

L'application communique avec le backend FastAPI existant via les endpoints suivants :

### Authentification
- `POST /users/login/` - Connexion
- `POST /users/register/` - Inscription
- `GET /users/me/` - Informations utilisateur

### Chat
- `POST /chat/send_message/` - Envoi de message (Elavira)
- `GET /chat/history/` - Historique des messages
- `POST /chat/transcribe_audio/` - Transcription audio

### Solenys
- `GET /solenys/solenys_query` - Requête Solenys

## 🎨 Personnalisation

### Thèmes et Couleurs
Les couleurs et styles sont définis dans les composants styled-components. Vous pouvez facilement modifier :

- **Couleurs principales** : Modifiez les gradients dans les composants
- **Typographie** : Changez la police dans `GlobalStyle`
- **Espacement** : Ajustez les paddings et margins

### Ajout de fonctionnalités
1. **Nouveaux assistants** : Ajoutez-les dans `AgentSelector.tsx`
2. **Nouvelles API** : Étendez `services/api.ts`
3. **Nouveaux types** : Ajoutez-les dans `types/index.ts`

## 🐛 Dépannage

### Problèmes courants

1. **Erreur de connexion API**
   - Vérifiez que le backend FastAPI est démarré
   - Vérifiez l'URL dans `services/api.ts`

2. **Problèmes audio**
   - Vérifiez les permissions du microphone
   - Testez dans un navigateur moderne (Chrome, Firefox, Safari)

3. **Erreurs de build**
   - Vérifiez que toutes les dépendances sont installées
   - Nettoyez le cache : `npm start -- --reset-cache`

## 📱 Compatibilité

- **Navigateurs** : Chrome 80+, Firefox 75+, Safari 13+, Edge 80+
- **Appareils** : Desktop, tablette, mobile
- **Résolutions** : 320px - 4K

## 🚀 Déploiement

### Build de production
```bash
npm run build
```

### Serveur statique
```bash
npx serve -s build
```

### Docker (optionnel)
```dockerfile
FROM nginx:alpine
COPY build/ /usr/share/nginx/html/
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## 🤝 Contribution

1. Fork le projet
2. Créez une branche feature (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Committez vos changements (`git commit -m 'Ajout nouvelle fonctionnalité'`)
4. Push vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Ouvrez une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🆘 Support

Pour toute question ou problème :
- Créez une issue sur GitHub
- Contactez l'équipe de développement
- Consultez la documentation du backend FastAPI