# Fichier: backend/core/solenys_logic.py

import uuid
from datetime import datetime
import requests
import os

# --- Configuration Solenys ---
# Solenys utilise directement Ollama sans ChromaDB

def ask_solenys(question: str) -> dict:
    """
    Fonction pour interroger l'assistant Solenys avec une question donnée.
    Solenys utilise directement Ollama sans base de données vectorielle.
    """
    response_text = ""
    
    # Définition de la persona de Solenys
    solenys_persona = (
        "Tu es Solenys, professeur de mathématiques pour élèves du secondaire. "
        "Réponds de manière directe et concise. "
        "Pour les calculs simples, donne directement la réponse : 2 x 2 = 4, 4 + 4 = 8. "
        "Si on demande 'explique plus', explique brièvement la méthode. "
        "Garde le contexte de la conversation précédente."
    )

    # Réponses prédéfinies pour calculs simples
    question_lower = question.lower().strip()
    
    if "bonjour" in question_lower or "qui es-tu" in question_lower():
        response_text = (
            "Bonjour ! Je suis Solenys, professeur de mathématiques. "
            "Que voulez-vous calculer ?"
        )
    elif "2 fois 2" in question_lower or "2 x 2" in question_lower:
        response_text = "2 x 2 = 4"
    elif "4 plus 4" in question_lower or "4 + 4" in question_lower:
        response_text = "4 + 4 = 8"
    elif "explique plus" in question_lower:
        response_text = "Pour additionner : on compte les unités. Pour multiplier : on répète l'addition."
    else:
        # Utiliser directement Ollama sans ChromaDB
        response_text = ollama_generate_simple(question, solenys_persona)

    return {
        "id": f"{datetime.now().isoformat()}_assistant_response_{str(uuid.uuid4())[:8]}",
        "text": response_text,
        "user_id": "Solenys Assistant",
        "timestamp": datetime.now().isoformat()
    }

def ollama_generate_simple(prompt: str, system_persona: str) -> str:
    """Génère une réponse via Ollama sans ChromaDB"""
    print(f"[Solenys] Envoi du prompt : {prompt[:100]}...")
    try:
        url = "http://ollama:11434/api/generate"
        data = {
            "model": "llama3.2:1b",
            "prompt": f"{system_persona}\n\nQuestion: {prompt}\n\nRéponse:",
            "stream": False,
            "options": {
                "temperature": 0.6,
                "top_p": 0.9,
                "max_tokens": 50,
                "repeat_penalty": 1.1
            }
        }
        
        response = requests.post(url, json=data, timeout=300)
        response.raise_for_status()
        
        result = response.json()
        generated_text = result.get("response", "").strip()
        
        print(f"[Solenys] Réponse reçue : {generated_text[:200]}...")
        return generated_text
        
    except requests.exceptions.RequestException as e:
        print(f"[Solenys] Erreur de connexion : {e}")
        return f"Erreur de connexion Ollama : {e}"
    except Exception as e:
        print(f"[Solenys] Erreur inattendue : {e}")
        return f"Erreur inattendue : {e}"

# --- Test rapide (optionnel) ---
if __name__ == "__main__":
    question = "Bonjour, qui es-tu ?"
    response = ask_solenys(question)
    print(response)
