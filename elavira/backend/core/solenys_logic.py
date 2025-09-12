# Fichier: backend/core/solenys_logic.py

import uuid
from datetime import datetime
from .llm_loader import rag_generate  # Utilise bien ton llm_loader avec qwen2:1.5b
import os

# --- Configuration Solenys ---
# Utilise l'API HTTP d'Ollama via llm_loader

def ask_solenys(question: str) -> dict:
    """
    Fonction pour interroger l'assistant Solenys avec une question donnée.
    Utilise la fonction rag_generate avec la persona spécifique de Solenys.
    """
    response_text = ""
    
    # Définition de la persona de Solenys
    solenys_persona = (
        "Tu es Solenys, une assistante virtuelle professionnelle pour Prof academie, "
        "spécialisée dans la gestion des agents et des processus internes, "
        "et plus spécifiquement conçue pour aider les élèves du secondaire. "
        "Tu réponds aux utilisateurs de manière claire, précise et polie. "
        "Tu t'exprimes de façon professionnelle et respectueuse, sans humour ni digression."
    )

    # Réponses simples prédéfinies
    if "bonjour" in question.lower() or "qui es-tu" in question.lower():
        response_text = (
            "Bonjour, je suis Solenys, je gère les agents et je suis là pour aider les élèves du secondaire."
        )
    else:
        # TRÈS IMPORTANT : passer la persona à rag_generate
        response_text = rag_generate(question, system_persona=solenys_persona)

    return {
        "id": f"{datetime.now().isoformat()}_assistant_response_{str(uuid.uuid4())[:8]}",
        "text": response_text,
        "user_id": "Solenys Assistant",
        "timestamp": datetime.now().isoformat()
    }

# --- Test rapide (optionnel) ---
if __name__ == "__main__":
    question = "Bonjour, qui es-tu ?"
    response = ask_solenys(question)
    print(response)
