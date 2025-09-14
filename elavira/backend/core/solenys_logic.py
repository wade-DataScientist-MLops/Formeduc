# Fichier: backend/core/solenys_logic.py

import os
import requests
import json
from datetime import datetime
import uuid
from .conversation_memory import get_conversation_context, add_message

def ask_solenys(question: str, user_id: str = "default") -> dict:
    """
    Fonction principale pour interagir avec Solenys, le professeur québécois.
    Spécialisé dans l'enseignement secondaire selon le programme PFEQ.
    """
    print(f"[Solenys] Question reçue: {question}")
    
    # Récupération du contexte de conversation
    conversation_context = get_conversation_context(user_id, "solenys", max_messages=3)
    
    # Construction du prompt avec mémoire de conversation
    full_prompt = f"""
Tu es Solenys, professeur québécois spécialisé dans l'enseignement secondaire selon le programme PFEQ du Québec.

Contexte de conversation:
{conversation_context}

Instructions:
- Réponds comme un professeur québécois bienveillant et compétent
- Adapte ton niveau au secondaire (12-17 ans)
- Utilise des exemples concrets et pratiques
- Sois encourageant et motivant
- Reste dans le cadre du programme PFEQ
- Sois concis et direct
- Maximum 2-3 phrases

Réponse:
"""
        # Réponse personnalisée de Solenys
        if "math" in question.lower() or "mathématiques" in question.lower():
            response_text = f"Salut ! Je suis Solenys, ton prof de mathématiques ! 📐\n\nTu demandes : '{question}'\n\nJe peux t'aider avec :\n• Algèbre et équations\n• Géométrie\n• Statistiques et probabilités\n• Fonctions et graphiques\n• Calcul différentiel et intégral\n\nQuelle matière veux-tu qu'on travaille ?"
        elif "science" in question.lower() or "physique" in question.lower() or "chimie" in question.lower():
            response_text = f"Salut ! Je suis Solenys, ton prof de sciences ! 🔬\n\nTu demandes : '{question}'\n\nJe peux t'aider avec :\n• Physique (mécanique, électricité, ondes)\n• Chimie (réactions, liaisons, équilibres)\n• Biologie (cellules, génétique, évolution)\n\nQuelle matière scientifique t'intéresse ?"
        elif "français" in question.lower() or "littérature" in question.lower():
            response_text = f"Salut ! Je suis Solenys, ton prof de français ! 📚\n\nTu demandes : '{question}'\n\nJe peux t'aider avec :\n• Grammaire et syntaxe\n• Littérature québécoise\n• Analyse de textes\n• Rédaction et composition\n• Communication orale\n\nQuel aspect du français veux-tu travailler ?"
        elif "bonjour" in question.lower() or "salut" in question.lower():
            response_text = "Salut ! Je suis Solenys, ton professeur québécois ! 👋\n\nJe suis spécialisé dans l'enseignement secondaire selon le programme PFEQ du Québec. Je peux t'aider en mathématiques, sciences, français, et autres matières.\n\nQuelle matière veux-tu qu'on travaille ensemble ?"
        else:
            response_text = f"Salut ! Je suis Solenys, ton professeur québécois ! 🎓\n\nTu me demandes : '{question}'\n\nJe suis spécialisé dans l'enseignement secondaire selon le programme PFEQ. Je peux t'aider en mathématiques, sciences, français, histoire, géographie, et plus encore !\n\nQuelle matière veux-tu qu'on explore ?"

    # Ajouter le message utilisateur et la réponse à la mémoire
    add_message(user_id, "solenys", "user", question)
    add_message(user_id, "solenys", "assistant", response_text)

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
                "temperature": 0.7,
                "top_p": 0.9,
                "max_tokens": 200,
                "repeat_penalty": 1.1
            }
        }
        
        response = requests.post(url, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        generated_text = result.get("response", "").strip()
        
        print(f"[Solenys] Réponse Ollama reçue : {generated_text[:100]}...")
        return generated_text
        
    except requests.exceptions.RequestException as e:
        print(f"[Solenys] Erreur de connexion Ollama : {e}")
        return "Désolé, je ne peux pas répondre pour le moment."
    except Exception as e:
        print(f"[Solenys] Erreur inattendue : {e}")
        return "Désolé, je ne peux pas répondre pour le moment."
