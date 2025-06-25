from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime
import requests
from backend.core.chroma_client import collection, embedder

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

# --- Modèles Pydantic ---

class MessageCreate(BaseModel):
    text: str
    user_id: str = "Guest"

class MessageDisplay(BaseModel):
    id: int
    text: str
    user_id: str
    timestamp: str

# --- Base mémoire pour stocker messages ---

fake_db_messages: List[Dict] = []
message_id_counter = 0

# --- Fonction génération réponse IA via Ollama ---

def generate_ai_response(prompt: str, context: str = "", model: str = "llama3") -> str:
    ### AJOUTÉ ###
    # Définition du prompt système pour donner des instructions à l'IA sur son identité et son comportement.
    SYSTEM_PROMPT = """Tu es Elavira Assistant, un assistant IA utile et amical.
Ton rôle est de répondre aux questions des utilisateurs en te basant sur les informations fournies dans les documents de référence.
Si la question porte sur ton identité (par exemple, "qui es-tu ?", "comment t'appelles-tu ?"), réponds que tu es Elavira Assistant et que tu es là pour aider.
Si la question ne peut pas être répondue avec les informations fournies dans le contexte, indique poliment que tu n'as pas l'information.
Ne dis pas de choses comme "le chat dort et le chien aboie" ou "je suis le chien qui aboie".
Réponds de manière concise et pertinente.
"""
    ### MODIFIÉ : Construction du prompt complet incluant le prompt système ###
    # Le prompt système doit précéder le contexte et la question pour guider le modèle.
    full_prompt = f"{SYSTEM_PROMPT}\n\nContexte : {context}\nQuestion : {prompt}\nRéponds précisément."

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": full_prompt, "stream": False}
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

    # 1. Enregistrer message utilisateur
    message_id_counter += 1
    user_msg = {
        "id": message_id_counter,
        "text": message.text,
        "user_id": message.user_id,
        "timestamp": datetime.utcnow().isoformat()
    }
    fake_db_messages.append(user_msg)
    print(f"[USER] {user_msg}")

    # 2. Convertir question en embedding
    question_embedding = embedder.encode(message.text).tolist()

    # 3. Recherche documents proches dans ChromaDB
    results = collection.query(query_embeddings=[question_embedding], n_results=3)
    docs_found = results['documents'][0] if results['documents'] else []
    context = "\n\n".join(docs_found)

    # Debug prints
    print(f"Question : {message.text}")
    print(f"Embedding (5 premières dimensions) : {question_embedding[:5]}")
    print(f"Documents trouvés : {docs_found}")
    # Ce print peut être commenté ou modifié pour montrer le prompt final avec le SYSTEM_PROMPT
    # print(f"Prompt envoyé à Ollama:\n{full_prompt}") # Supprimer ou commenter cette ligne

    # 4. Générer réponse IA avec contexte
    ai_response = generate_ai_response(message.text, context) # Ici, la fonction génère le prompt complet

    # 5. Enregistrer message IA
    message_id_counter += 1
    bot_msg = {
        "id": message_id_counter,
        "text": ai_response,
        "user_id": "Elavira Assistant",
        "timestamp": datetime.utcnow().isoformat()
    }
    fake_db_messages.append(bot_msg)
    print(f"[BOT] {bot_msg}")

    # 6. Retourner la réponse IA au front
    return bot_msg

@router.get("/history/", response_model=List[MessageDisplay])
async def get_chat_history():
    return fake_db_messages