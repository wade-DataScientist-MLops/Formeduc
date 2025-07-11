from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime
import requests
import base64
import io
from gtts import gTTS
from backend.core.chroma_client import collection, embedder

# ✅ Routeur principal
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
    audio_base64: str = None

# --- "Fake DB" locale ---
fake_db_messages: List[Dict] = []
message_id_counter = 0

# --- Génération de réponse IA via Ollama ---
def generate_ai_response(prompt: str, context: str = "", model: str = "llama3") -> str:
    base_system_prompt = (
        "Tu es une assistante IA bienveillante et chaleureuse, appelée Elavira. "
        "Tu travailles pour Formeduc, une plateforme qui propose des cours de secourisme. "
        "Tu réponds de manière concise, utile et uniquement si le contexte le permet. "
        "Tu n'as pas besoin de commenter des éléments hors sujet comme 'le chat dort' ou 'le chien aboie'. "
        "Si une question n'est pas claire ou ne contient pas d'information pertinente, demande une précision."
    )

    greetings = ["salut", "bonjour", "coucou"]
    if prompt.lower().strip() in greetings:
        system_prompt = base_system_prompt + (
            " Quand quelqu’un te salue, tu réponds avec douceur : "
            "\"Bonjour, je suis Elavira, votre éducatrice en secourisme.\""
        )
    else:
        system_prompt = base_system_prompt + " Ne te présente pas dans cette réponse."

    full_prompt = f"{system_prompt}\n\nContexte : {context}\nQuestion : {prompt}\nRéponds précisément."

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": full_prompt, "stream": False}
        )
        response.raise_for_status()
        return response.json().get("response", "Désolé, je n’ai pas compris.")
    except Exception as e:
        print(f"[Ollama] Erreur : {e}")
        return "Erreur lors de la génération de la réponse IA."

# --- Synthèse vocale (TTS avec gTTS) ---
def synthesize_speech(text: str) -> str:
    try:
        mp3_fp = io.BytesIO()
        tts = gTTS(text, lang="fr")
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        audio_bytes = mp3_fp.read()
        return base64.b64encode(audio_bytes).decode("utf-8")
    except Exception as e:
        print(f"[TTS] Erreur synthèse vocale : {e}")
        return None

# --- Routes FastAPI ---

@router.get("/")
async def read_chat_status():
    return {"message": "Chat routes are working!", "status": "active"}

@router.post("/send_message/", response_model=MessageDisplay)
async def send_message(message: MessageCreate):
    global message_id_counter

    # Sauvegarde du message utilisateur
    message_id_counter += 1
    user_msg = {
        "id": message_id_counter,
        "text": message.text,
        "user_id": message.user_id,
        "timestamp": datetime.utcnow().isoformat()
    }
    fake_db_messages.append(user_msg)

    # Recherche contextuelle
    question_embedding = embedder.encode(message.text).tolist()
    results = collection.query(query_embeddings=[question_embedding], n_results=3)
    docs_found = results['documents'][0] if results['documents'] else []
    context = "\n\n".join(docs_found)

    # Génération réponse IA
    ai_response = generate_ai_response(message.text, context)

    # Synthèse vocale de la réponse
    audio_base64 = synthesize_speech(ai_response)

    # Sauvegarde de la réponse IA
    if not fake_db_messages or fake_db_messages[-1]["text"] != ai_response:
        message_id_counter += 1
        bot_msg = {
            "id": message_id_counter,
            "text": ai_response,
            "user_id": "Elavira Assistant",
            "timestamp": datetime.utcnow().isoformat(),
            "audio_base64": audio_base64
        }
        fake_db_messages.append(bot_msg)
    else:
        bot_msg = fake_db_messages[-1]

    return bot_msg

@router.get("/history/", response_model=List[MessageDisplay])
async def get_chat_history():
    return fake_db_messages

@router.post("/transcribe_audio/")
async def transcribe_audio(file: UploadFile = File(...)):
    try:
        if not file:
            raise HTTPException(status_code=400, detail="Aucun fichier n’a été fourni.")
        audio_bytes = await file.read()
        response = requests.post(
            "http://localhost:11434/api/transcribe",
            files={"audio": ("audio.wav", audio_bytes, "audio/wav")}
        )
        response.raise_for_status()
        data = response.json()
        text = data.get("text", "")
        return {"transcribed_text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de transcription : {e}")
