
# backend/main.py

from fastapi import FastAPI
# from .api import routes_chat, routes_agents, routes_users, routes_documents, routes_logs # à décommenter quand vous les aurez
from .db.database import init_db # Importez la fonction d'initialisation de la BDD (CORRIGÉ !)
from contextlib import asynccontextmanager # Pour l'événement de démarrage asynchrone

# Fonction de gestion du cycle de vie de l'application
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Logique exécutée au démarrage de l'application
    print("Démarrage de l'application Elavira...")
    init_db() # Initialise la base de données (crée les tables si elles n'existent pas)
    print("Base de données initialisée.")
    yield
    # Logique exécutée à l'arrêt de l'application
    print("Arrêt de l'application Elavira...")

app = FastAPI(
    title="Elavira Backend API",
    description="API pour la plateforme Elavira, un assistant IA intelligent.",
    version="0.1.0",
    lifespan=lifespan # Utiliser le gestionnaire de cycle de vie
)

# # Inclure vos routes API (décommenter au fur et à mesure que vous les développez)
# app.include_router(routes_users.router, prefix="/users", tags=["users"])
# app.include_router(routes_chat.router, prefix="/chat", tags=["chat"])
# app.include_router(routes_agents.router, prefix="/agents", tags=["agents"])
# app.include_router(routes_documents.router, prefix="/documents", tags=["documents"])
# app.include_router(routes_logs.router, prefix="/logs", tags=["logs"])

# Route de test simple
@app.get("/")
async def read_root():
    return {"message": "Bienvenue sur l'API Backend d'Elavira !"}