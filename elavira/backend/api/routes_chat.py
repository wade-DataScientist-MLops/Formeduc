# backend/api/routes_chat.py

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel # Pour définir le modèle de données du message
from typing import List, Dict # Pour les types de données

# Importez vos modèles et schémas nécessaires ici si vous les utilisez
# from backend.db import models, schemas
# from backend.db.database import get_db

# Crée une instance de APIRouter pour les routes de chat
router = APIRouter(
    prefix="/chat",  # Toutes les routes ici commenceront par /chat
    tags=["Chat"]    # Pour l'organisation dans la documentation Swagger/OpenAPI
)

# --- Modèles Pydantic pour les données du chat ---
# Ce modèle définit la structure d'un message entrant
class MessageCreate(BaseModel):
    text: str
    user_id: int = 1 # Pour l'exemple, nous allons fixer l'user_id à 1 pour l'instant

# Ce modèle pourrait définir la structure d'un message stocké ou retourné
class MessageDisplay(BaseModel):
    id: int
    text: str
    user_id: int
    timestamp: str # Ou datetime.datetime si vous gérez les dates réelles

# --- Simulation d'une base de données de chat (en mémoire) ---
# Cette liste simule l'historique des messages. Elle sera effacée à chaque redémarrage du serveur.
fake_db_messages: List[Dict] = []
message_id_counter = 0

@router.get("/")
async def read_chat_status():
    """
    Endpoint de test pour vérifier que les routes de chat fonctionnent.
    """
    return {"message": "Chat routes are working!", "status": "active"}

@router.post("/send_message/", response_model=MessageDisplay)
async def send_message(message: MessageCreate):
    """
    Endpoint pour envoyer un nouveau message.
    """
    global message_id_counter
    message_id_counter += 1
    new_message = {
        "id": message_id_counter,
        "text": message.text,
        "user_id": message.user_id,
        "timestamp": "2025-06-11 T10:00:00Z" # Date/heure fixe pour l'instant
    }
    fake_db_messages.append(new_message)
    print(f"Nouveau message reçu : {new_message}") # Pour voir dans le terminal FastAPI
    return new_message

@router.get("/history/", response_model=List[MessageDisplay])
async def get_chat_history():
    """
    Endpoint pour récupérer l'historique complet des messages.
    """
    return fake_db_messages

# @router.get("/history/{user_id}", response_model=List[MessageDisplay])
# async def get_user_chat_history(user_id: int):
#     """
#     Endpoint pour récupérer l'historique des messages d'un utilisateur spécifique.
#     """
#     user_messages = [msg for msg in fake_db_messages if msg["user_id"] == user_id]
#     return user_messages