# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from sqlalchemy.orm import Session # Si vous utilisez une base de données avec SQLAlchemy
# from typing import Annotated # Si vous utilisez des annotations pour les dépendances

# Importez vos routeurs ici
# Assurez-vous que ces fichiers existent dans backend/api/
# Décommentez les lignes correspondantes si vous avez ces fichiers et que vous voulez les inclure
from backend.api import routes_users
from backend.api import routes_chat
# from backend.api import routes_agents # Décommentez si vous avez ce routeur et qu'il est corrigé

# =======================================================
# CODE SUPPRIMÉ : C'est le code Streamlit qui était là par erreur
# import base64
# import os
# current_dir = os.path.dirname(os.path.abspath(__file__))
# image_path = os.path.join(current_dir, "images", "4 - Elavira (1).png")
# def add_bg_from_local(image_file):
#     with open(image_file, "rb") as file:
#         encoded = base64.b64encode(file.read()).decode()
#     css = f"""
#     <style>
#     .stApp {{
#         background-image: url("data:image/png;base64,{encoded}");
#         background-size: 47% auto;
#         background-position: center;
#         background-repeat: no-repeat;
#         background-attachment: fixed;
#     }}
#     </style>
#     """
#     # st.markdown(css, unsafe_allow_html=True) # Streamlit n'est pas importé ici
# =======================================================


app = FastAPI(
    title="API Elavira",
    description="Une API pour l'assistant Elavira",
    version="0.0.1",
)

# --- Configuration CORS ---
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:3000",
    "http://localhost:8080",
    "http://localhost:4200",
    "http://localhost:8501", # Le port par défaut de Streamlit
    # Ajoutez ici l'URL de votre frontend en production lorsque vous la déployerez
    # "https://votre-domaine-frontend.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --- Fin de la configuration CORS ---


# --- Inclure vos routeurs d'API ---
app.include_router(routes_users.router)
app.include_router(routes_chat.router)
# app.include_router(routes_agents.router) # Décommentez ceci quand vous aurez corrigé routes_agents.py


# --- Routes de base de l'application ---
@app.get("/")
async def read_root():
    """
    Point d'accès racine de l'API.
    Retourne un message de bienvenue.
    """
    return {"message": "Bienvenue sur l'API Elavira!"}

# Ajoutez d'autres routes de haut niveau ici si nécessaire