# Fichier: backend/core/solenys_logic.py

import uuid
from datetime import datetime
import requests
import os
import chromadb
from sentence_transformers import SentenceTransformer

# --- Configuration Solenys ---
# Solenys utilise ChromaDB avec le document PFEQ + Ollama

# Initialisation ChromaDB pour Solenys
def get_solenys_chroma_client():
    """Initialise le client ChromaDB pour Solenys"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    chroma_db_path = os.path.join(script_dir, "..", "chroma_data")
    os.makedirs(chroma_db_path, exist_ok=True)
    
    client = chromadb.PersistentClient(path=chroma_db_path)
    collection = client.get_or_create_collection(name="elavira_collection")
    return collection

def get_solenys_embedder():
    """Initialise l'embedder pour Solenys"""
    try:
        embedder = SentenceTransformer('all-MiniLM-L6-v2')
        return embedder
    except Exception as e:
        print(f"❌ Erreur initialisation embedder Solenys : {e}")
        return None

def query_solenys_documents(query: str, n_results: int = 3):
    """Recherche dans les documents PFEQ pour Solenys"""
    try:
        collection = get_solenys_chroma_client()
        embedder = get_solenys_embedder()
        
        if not embedder:
            return []
        
        # Générer l'embedding de la requête
        query_embedding = embedder.encode([query]).tolist()[0]
        
        # Rechercher dans ChromaDB
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=['documents', 'distances', 'metadatas']
        )
        
        return results['documents'][0] if results['documents'] else []
        
    except Exception as e:
        print(f"❌ Erreur recherche documents Solenys : {e}")
        return []

def ask_solenys(question: str) -> dict:
    """
    Fonction pour interroger l'assistant Solenys avec une question donnée.
    Solenys utilise ChromaDB avec le document PFEQ + Ollama.
    """
    response_text = ""
    
    # Définition de la persona de Solenys
    solenys_persona = (
        "Tu es Solenys, professeur spécialisé dans le programme de secondaire du Québec (PFEQ). "
        "Tu aides les élèves avec les mathématiques, sciences, français selon le curriculum québécois. "
        "Réponds de manière claire et pédagogique en te basant sur le programme officiel."
    )

    # Réponses prédéfinies pour calculs simples
    question_lower = question.lower().strip()
    
    if "bonjour" in question_lower or "qui es-tu" in question_lower:
        response_text = (
            "Bonjour ! Je suis Solenys, professeur spécialisé dans le programme de secondaire du Québec. "
            "Je peux vous aider avec les mathématiques, sciences, français selon le PFEQ. "
            "Que souhaitez-vous apprendre ?"
        )
    elif "2 fois 2" in question_lower or "2 x 2" in question_lower:
        response_text = "2 x 2 = 4"
    elif "4 plus 4" in question_lower or "4 + 4" in question_lower:
        response_text = "4 + 4 = 8"
    elif "explique plus" in question_lower:
        response_text = "Pour additionner : on compte les unités. Pour multiplier : on répète l'addition."
    else:
        # Utiliser ChromaDB + Ollama avec le document PFEQ
        context_docs = query_solenys_documents(question, n_results=3)
        context = "\n\n".join(context_docs) if context_docs else "Aucun contexte PFEQ disponible."
        
        full_prompt = f"""
{solenys_persona}

Programme de formation de l'école québécoise (PFEQ) :
{context}

Question de l'élève : {question}

Réponse pédagogique :
"""
        response_text = ollama_generate_simple(full_prompt, "")

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
