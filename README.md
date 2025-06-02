# Formeduc creation d'une plateforme IA chatboot conversationnel 
# 🤖 Elavira – Plateforme d’agents intelligents personnalisés

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
