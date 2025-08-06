# Fichier: backend/core/solenys_logic.py

import uuid
from datetime import datetime
from .llm_loader import rag_generate # Assurez-vous que cet import est correct

def ask_solenys(question: str) -> dict:
    response_text = ""
    
    # Définition de la persona de Solenys
    solenys_persona = "Tu es Solenys, une assistante virtuelle professionnelle pour Formeduc, spécialisée dans la gestion des agents et des processus internes, et plus spécifiquement conçue pour aider les élèves du secondaire. Tu réponds aux utilisateurs de manière claire, précise et polie. Tu t'exprimes de façon professionnelle et respectueuse, sans humour ni digression."

    if "bonjour" in question.lower() or "qui es-tu" in question.lower():
        response_text = "Bonjour, je suis Solenys, je gère les agents et je suis là pour aider les élèves du secondaire."
    else:
        # TRÈS IMPORTANT : Passer la persona à rag_generate
        response_text = rag_generate(question, system_persona=solenys_persona) # <-- C'est la ligne clé
        
    return {
        "id": datetime.now().isoformat() + "_assistant_response_" + str(uuid.uuid4())[:8],
        "text": response_text,
        "user_id": "Solenys Assistant",
        "timestamp": datetime.now().isoformat()
    }