from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

# Crée une instance de APIRouter pour les routes de chat
router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

# ========================
# 🚀 SCHEMAS / MODELS
# ========================

class ChatRequest(BaseModel):
    user_id: str  # ou int selon ton système
    message: str

class ChatResponse(BaseModel):
    reply: str
    user_id: str

# ========================
# ✅ ROUTES
# ========================

@router.get("/")
async def read_chat_status():
    """
    Endpoint de test pour vérifier que les routes de chat fonctionnent.
    """
    return {"message": "Chat routes are working!", "status": "active"}

@router.post("/ask", response_model=ChatResponse)
async def ask_chat(request: ChatRequest):
    """
    Envoie une question de l'utilisateur et retourne une réponse simulée.
    À connecter à LocalAI ou Ollama par la suite.
    """
    user_message = request.message

    # 🧠 Simulation IA (à remplacer par appel réel)
    response_text = f"Tu as dit : '{user_message}'. Je suis une IA en cours d'intégration."

    return ChatResponse(reply=response_text, user_id=request.user_id)

# ========================
# (Optionnel) Historique
# ========================

# @router.get("/history/{user_id}")
# async def get_chat_history(user_id: str):
#     """
#     (Optionnel) Récupère l'historique des messages d'un utilisateur.
#     """
#     # Exemple de réponse simulée
#     history = [
#         {"message": "Bonjour", "reply": "Salut !"},
#         {"message": "Quel temps fait-il ?", "reply": "Je ne suis pas encore connecté à la météo..."}
#     ]
#     return {"user_id": user_id, "history": history}
