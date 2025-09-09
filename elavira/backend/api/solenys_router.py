from fastapi import APIRouter
from ..core.solenys_logic import ask_solenys

from datetime import datetime
import io
import base64
from gtts import gTTS

router = APIRouter()


def _synthesize_speech_base64_fr(text: str) -> str:
    try:
        mp3_fp = io.BytesIO()
        tts = gTTS(text, lang="fr")
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        return base64.b64encode(mp3_fp.read()).decode("utf-8")
    except Exception:
        return None


@router.get("/solenys_query")
async def solenys_query(q: str):
    response_text = ask_solenys(q)

    audio_base64 = _synthesize_speech_base64_fr(response_text)

    message = {
        "id": int(datetime.utcnow().timestamp() * 1000),
        "text": response_text,
        "user_id": "Solenys Assistant",
        "timestamp": datetime.utcnow().isoformat(),
        "audio_base64": audio_base64,
        "suggested_prompts": [
            "Quelles sont tes capacités ?",
            "Donne-moi un exemple d'utilisation.",
            "Peux-tu résumer ce texte ?",
            "Explique-moi étape par étape.",
        ],
    }

    return {"answer": message}
