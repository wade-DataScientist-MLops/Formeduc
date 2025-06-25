from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime
import requests
import base64
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
    audio_base64: str = None  # Champ pour l'audio TTS en base64

# --- Mémoire (temporaire) ---

fake_db_messages: List[Dict] = []
message_id_counter = 0

# --- Fonction génération réponse IA via Ollama ---

def generate_ai_response(prompt: str, context: str = "", model: str = "llama3") -> str:
    SYSTEM_PROMPT = """Tu es Elavira Assistant, un assistant IA utile et amical.
Ton rôle est de répondre aux questions des utilisateurs en te basant sur les informations fournies dans les documents de référence.
Si la question porte sur ton identité (par exemple, "qui es-tu ?", "comment t'appelles-tu ?"), réponds que tu es Elavira Assistant et que tu es là pour aider.
Si la question ne peut pas être répondue avec les informations fournies dans le contexte, indique poliment que tu n'as pas l'information.
Réponds de manière concise et pertinente.
"""
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

# --- TTS : Transformer réponse texte en audio MP3 (base64) ---

def synthesize_speech(text: str) -> str:
    try:
        # Envoie à une route de TTS locale si tu as une API dédiée.
        # Sinon, gTTS ou moteur local peut être utilisé ici.
        from gtts import gTTS
        import io
        mp3_fp = io.BytesIO()
        tts = gTTS(text, lang="fr")
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        audio_bytes = mp3_fp.read()
        return base64.b64encode(audio_bytes).decode("utf-8")
    except Exception as e:
        print(f"[TTS] Erreur synthèse vocale : {e}")
        return None

# --- Routes ---

@router.get("/")
async def read_chat_status():
    return {"message": "Chat routes are working!", "status": "active"}

@router.post("/send_message/", response_model=MessageDisplay)
async def send_message(message: MessageCreate):
    global message_id_counter

    # Enregistrer message utilisateur
    message_id_counter += 1
    user_msg = {
        "id": message_id_counter,
        "text": message.text,
        "user_id": message.user_id,
        "timestamp": datetime.utcnow().isoformat()
    }
    fake_db_messages.append(user_msg)

    # Embedding + Recherche Chroma
    question_embedding = embedder.encode(message.text).tolist()
    results = collection.query(query_embeddings=[question_embedding], n_results=3)
    docs_found = results['documents'][0] if results['documents'] else []
    context = "\n\n".join(docs_found)

    # Réponse IA
    ai_response = generate_ai_response(message.text, context)

    # TTS (base64)
    audio_base64 = synthesize_speech(ai_response)

    # Enregistrer réponse bot
    message_id_counter += 1
    bot_msg = {
        "id": message_id_counter,
        "text": ai_response,
        "user_id": "Elavira Assistant",
        "timestamp": datetime.utcnow().isoformat(),
        "audio_base64": audio_base64
    }
    fake_db_messages.append(bot_msg)
    return bot_msg

@router.get("/history/", response_model=List[MessageDisplay])
async def get_chat_history():
    return fake_db_messages

@router.post("/transcribe_audio/")
async def transcribe_audio(file: UploadFile = File(...)):
    try:
        # Lecture du fichier audio
        audio_bytes = await file.read()

        # Appel à Ollama Whisper local
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
