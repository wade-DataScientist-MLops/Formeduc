# elavira/backend/api/routes_chat.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime
import requests

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

# --- Modèles Pydantic ---
class MessageCreate(BaseModel):
    text: str
    user_id: str = "Guest" # <-- CHANGEMENT ICI : user_id est maintenant de type str

class MessageDisplay(BaseModel):
    id: int
    text: str
    user_id: str # <-- CHANGEMENT ICI : user_id est maintenant de type str
    timestamp: str

# --- Simulation d'une base en mémoire ---
fake_db_messages: List[Dict] = []
message_id_counter = 0

# --- Fonction utilitaire pour générer une réponse via Ollama (inchangée) ---
def generate_ai_response(prompt: str, model: str = "llama3") -> str:
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt, "stream": False}
        )
        response.raise_for_status()
        return response.json().get("response", "Désolé, je n'ai pas compris.")
    except Exception as e:
        print(f"[Ollama] Erreur : {e}")
        return "Erreur lors de la génération de la réponse IA."

# --- Routes ---

@router.get("/")
async def read_chat_status():
    return {"message": "Chat routes are working!", "status": "active"}

@router.post("/send_message/", response_model=MessageDisplay)
async def send_message(message: MessageCreate):
    global message_id_counter

    # 1. Enregistrement du message utilisateur
    message_id_counter += 1
    user_msg = {
        "id": message_id_counter,
        "text": message.text,
        "user_id": message.user_id, # C'est déjà une str grâce au modèle
        "timestamp": datetime.utcnow().isoformat()
    }
    fake_db_messages.append(user_msg)
    print(f"[USER] {user_msg}")

    # 2. Génération de la réponse IA
    ai_response = generate_ai_response(message.text)

    # 3. Enregistrement du message IA
    message_id_counter += 1
    bot_msg = {
        "id": message_id_counter,
        "text": ai_response,
        "user_id": "Elavira Assistant",  # <-- CHANGEMENT ICI : L'IA est maintenant une chaîne
        "timestamp": datetime.utcnow().isoformat()
    }
    fake_db_messages.append(bot_msg)
    print(f"[BOT] {bot_msg}")

    # 4. Retour du message utilisateur uniquement (ou bot_msg si tu préfères)
    return user_msg

@router.get("/history/", response_model=List[MessageDisplay])
async def get_chat_history():
    return fake_db_messages