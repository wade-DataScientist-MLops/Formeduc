
# 🤖 Elavira – Plateforme d’agents intelligents personnalisés
![4 - Elavira](https://github.com/user-attachments/assets/9c924868-7310-48c4-882a-e2038e3195e3)


Elavira est une plateforme modulaire et auto-hébergée permettant de créer, configurer et exploiter des agents intelligents pour l’éducation et la formation. Elle repose sur une architecture moderne en Python (FastAPI), PostgreSQL, et des moteurs LLM locaux comme **Ollama**.  

> 🔒 **Objectif :** garantir la **confidentialité**, l’**autonomie** et la **personnalisation** des IA.

---

## 🧩 1. Modules principaux

### 📌 1.1 Frontend Web (Python)
- Authentification sécurisée (JWT)
- Interface de chat avec les agents
- Tableau de bord administrateur

### 📌 1.2 API REST (FastAPI)
- Gestion des utilisateurs, agents, conversations
- Intégration avec PostgreSQL
- Endpoints REST : `/chat`, `/agents`, `/documents`, `/logs`

### 📌 1.3 Base de données (PostgreSQL)
Schéma recommandé :
```sql
users(id, email, password_hash, is_admin)
agents(id, name, config, owner_id)
conversations(id, user_id, agent_id, timestamp)
messages(id, conversation_id, sender, content, timestamp)
documents(id, filename, embedding_path, agent_id)
logs(timestamp, action, user_id, details)
````

### 📌 1.4 Moteur de recherche vectoriel local

* Objectif : recherche rapide sur documents internes
* Outils supportés :

  * `Chroma` (léger, intégré Python)
  * `Weaviate` (scalable)

### 📌 1.5 Moteurs IA

* Support natif des LLM locaux via **Ollama** : LLaMA3, Mistral, etc.
* Option de fallback : OpenAI, Claude, Mistral API

### 📌 1.6 Agent Router (Orchestrateur)

Responsable de :

* Identifier l’agent actif
* Charger sa configuration (prompt, moteur, base vectorielle…)
* Router la requête vers :

  * IA locale (via Ollama)
  * IA distante (si activé)
  * Recherche vectorielle (RAG)

### 📌 1.7 Tableau de bord

Réservé aux admins :

* Statistiques d’utilisation
* Journalisation des activités
* Gestion des utilisateurs, agents, documents




![5 - Coeur d'Elavira](https://github.com/user-attachments/assets/65a719cf-5c70-4e03-a242-0a1823cd3595)


## 🐳 2. Déploiement local (Docker)

Tu peux déployer l’ensemble des services avec `docker-compose`.

Extrait :

```yaml
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    depends_on:
      - db

  db:
    image: postgres
    environment:
      POSTGRES_USER: elavira
      POSTGRES_PASSWORD: password
      POSTGRES_DB: elavira_db

  ollama:
    image: ollama/ollama
    ports:
      - "11434:11434"
```

➡️ [Installer Docker](https://www.docker.com/)

---

## ⚠️ 3. Modularité (Elavira Core)

Chaque agent est une classe Python modulaire :

```python
class ElaviraAgent:
    def __init__(self, config):
        self.vector_db = load_vector_db(config.documents)
        self.llm = load_llm(config.llm_name)

    def respond(self, query):
        docs = self.vector_db.similarity_search(query)
        context = "\n".join(docs)
        return self.llm.generate_response(query, context=context)
```

---

## 🧪 4. Tests & Sécurité

* ✅ Tests unitaires avec `pytest`
* 🔐 Authentification via JWT + mot de passe hashé (bcrypt)
* 📦 Journalisation complète des actions (logs PostgreSQL)
* ♻️ Sauvegardes régulières de la base PostgreSQL

---

## 📚 Documentation complémentaire

* `docs/architecture.png` : Schéma complet de l’architecture technique
* `docs/api_reference.md` : Spécification des endpoints REST
* `docs/config_example.json` : Exemple de configuration d’un agent

---

## 📜 Licence

Projet sous licence MIT – libre de réutilisation dans un cadre académique ou éducatif.

---

## 🚧 En cours pour le MVP (Septembre 2025)

* 🔄 Interface web finalisée (React ou Python-based UI)
* ⚙️ Upload intelligent de documents internes
* 🧠 Système de mémoire à long terme pour chaque agent
* 🔌 Plugin "professeur virtuel" pour FormEduc

---

## 👤 Équipe

Développé par Wade et Danny   dans le cadre du projet de stage .
Voici une **proposition d’arborescence propre et modulaire** pour ton projet Elavira :

---

```
elavira/
├── README.md
├── docker-compose.yml
├── .env                         # Variables d’environnement (DB, ports, clés)
├── requirements.txt             # Dépendances Python
│
├── backend/
│   ├── main.py                  # Point d’entrée FastAPI
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes_chat.py       # /chat endpoint
│   │   ├── routes_agents.py     # /agents endpoint
│   │   ├── routes_users.py      # /users endpoint
│   │   ├── routes_documents.py  # /documents endpoint
│   │   └── routes_logs.py       # /logs endpoint
│   │
│   ├── core/
│   │   ├── agent_router.py      # Logique de routage intelligent
│   │   ├── auth.py              # JWT, bcrypt
│   │   ├── config.py            # Chargement de configs dynamiques
│   │   ├── vector_store.py      # Chroma / Weaviate wrapper
│   │   └── llm_loader.py        # Ollama / OpenAI loader
│   │
│   ├── db/
│   │   ├── models.py            # ORM Pydantic / SQLAlchemy
│   │   ├── database.py          # Connexion à PostgreSQL
│   │   └── schemas.py           # Schémas Pydantic
│   │
│   ├── tests/
│   │   ├── test_auth.py
│   │   ├── test_chat.py
│   │   └── test_vector_search.py
│   │
│   └── utils/
│       ├── logger.py            # Logging centralisé
│       ├── security.py          # Hash, JWT
│       └── file_handler.py      # Upload/Download de fichiers
│
├── frontend/![5 - Coeur d'Elavira](https://github.com/user-attachments/assets/c91d2201-d5b0-4fdb-a030-caf7d86f7dbd)

│   ├── app.py                   # (optionnel) Interface Python (Streamlit, Gradio…)
│   └── web/                     # Ou React / Vue si projet web
│       ├── public/
│       ├── src/
│       │   ├── components/
│       │   ├── pages/
│       │   ├── services/        # API calls
│       │   └── App.tsx
│       └── package.json
│
├── docs/
│   ├── architecture.png         # Diagramme visuel
│   ├── api_reference.md         # Doc des endpoints
│   └── config_example.json      # Exemple de fichier agent
│
└── scripts/
    ├── backup_db.sh             # Sauvegarde PostgreSQL
    └── seed_db.py               # Création utilisateurs de test
```

---

### 📌 Avantages de cette structure

* **Modularité :** chaque composant (auth, LLM, base vectorielle) est isolé
* **Scalabilité :** facile à étendre (multi-agents, plugins, monitoring)
* **Séparation claire frontend/backend**



