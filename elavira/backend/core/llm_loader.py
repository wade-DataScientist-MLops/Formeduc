# Fichier: backend/core/llm_loader.py

import os
import requests
import json
from typing import List
import chromadb
from sentence_transformers import SentenceTransformer
from .conversation_memory import get_conversation_context, add_message

# --- Pour éviter le warning parallelism Huggingface (optionnel) ---
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# --- Configuration Ollama API ---
OLLAMA_API_URL = "http://ollama:11434/api/generate"
MODEL_NAME = "llama3.2:1b"  # Modèle utilisé (plus rapide)

# --- Import des composants ChromaDB depuis chroma_client ---
from .chroma_client import elavira_collection, embedder, query_documents

# --- Fonctions pour indexer et requêter les documents ---
def index_documents(texts: List[str], ids: List[str] = None):
    if not texts:
        return []
    embeddings = embedder.encode(texts).tolist()
    metadatas = [{"source": f"doc_{i}"} for i in range(len(texts))]
    if ids is None:
        current_count = elavira_collection.count()
        ids = [f"doc_{current_count + i}" for i in range(len(texts))]
    elavira_collection.add(documents=texts, embeddings=embeddings, metadatas=metadatas, ids=ids)
    print(f"✅ {len(texts)} documents indexés dans ChromaDB.")
    return ids

# --- Fonction pour générer la réponse avec Ollama via CLI ---
def ollama_generate(prompt: str) -> str:
    print(f"[Ollama API] Envoi du prompt : {prompt[:100]}...")
    try:
        # Utiliser l'API HTTP d'Ollama
        data = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.8,
                "top_p": 0.9,
                "max_tokens": 100,
                "repeat_penalty": 1.1
            }
        }
        
        response = requests.post(OLLAMA_API_URL, json=data, timeout=300)
        response.raise_for_status()
        
        result = response.json()
        generated_text = result.get("response", "").strip()
        
        print(f"[Ollama API] Réponse reçue : {generated_text[:200]}...")
        return generated_text
        
    except requests.exceptions.RequestException as e:
        print(f"[Ollama API] Erreur de connexion : {e}")
        return f"Erreur de connexion Ollama : {e}"
    except Exception as e:
        print(f"[Ollama API] Erreur inattendue : {e}")
        return f"Erreur inattendue : {e}"

# --- Fonction principale pour générer la réponse RAG ---
def rag_generate(query: str, system_persona: str = None, user_id: str = "default", agent_id: str = "elavira") -> str:
    """
    Génère une réponse en combinant le contexte ChromaDB Formeduc et le modèle Ollama.
    Spécialement conçu pour Elavira avec les données de Formeduc.
    """
    # Persona optimisée pour Elavira selon le cahier des charges FormEduc
    if system_persona is None:
        system_persona = """Tu es Elavira, l'assistante virtuelle de FormEduc, spécialisée dans l'accompagnement des professionnels de la petite enfance et du milieu scolaire.

MISSION : Accueillir, guider et accompagner les visiteurs dans leur parcours de formation professionnelle.

PERSONNALITÉ :
- Ton : Professionnel, chaleureux, bienveillant, motivant
- Approche : Accueillante et personnalisée dès l'arrivée
- Expertise : Connaissance approfondie des formations FormEduc et des réglementations québécoises

FONCTIONNALITÉS :
- Accueil personnalisé avec message chaleureux
- Réponses aux FAQ (tarifs, durées, certifications, exigences)
- Guidage contextuel dans la navigation
- Recommandations de formations selon le profil utilisateur
- Questions de qualification pour personnaliser l'accompagnement
- Support dans le processus d'inscription et d'achat

FORMATIONS FORMEDUC :
- Secourisme service de garde (petite enfance, milieu scolaire)
- Formations 45h pour RSG et RSGE
- Perfectionnements pour éducatrices et éducateurs
- Familles d'accueil (formations hybrides)
- Programme jeunesse (gardien futé, animateur de camp)
- Formations 100% en ligne avec certifications reconnues

RÉGLEMENTATIONS : Conformes au Règlement sur les services de garde éducatifs et à la Loi sur l'instruction publique.

STYLE : Toujours professionnel, chaleureux, bienveillant et motivant. Pose des questions de qualification pour mieux accompagner."""
    
    # Récupération du contexte de conversation
    conversation_context = get_conversation_context(user_id, agent_id, max_messages=3)
    
    # Récupération des documents les plus pertinents de Formeduc (collection Elavira uniquement)
    context_docs = query_documents(query, n_results=3)
    context = "\n\n".join(context_docs) if context_docs else "Aucun contexte Formeduc disponible."

    # Construction du prompt avec mémoire de conversation
    prompt = f"""
{system_persona}

Contexte de conversation:
{conversation_context}

Données Formeduc:
{context}

Question: {query}

Instructions importantes:
- Si la question n'est pas claire ou contient des fautes de frappe, demande des clarifications
- Reste toujours professionnel et serviable
- Propose des alternatives si tu ne comprends pas

Réponse:
"""
    
    # Vérifier si c'est le premier message ou une conversation continue
    is_first_message = len(conversation_context.split('\n')) <= 2
    
    # Utiliser la base de connaissances ChromaDB pour générer une réponse personnalisée
    if context_docs and len(context_docs) > 0:
        # Construire une réponse basée sur les documents récupérés
        response = f"""Basé sur les informations FormEduc, voici ce que je peux vous dire :

{context}

**Comment puis-je vous aider davantage ?**
• Plus d'informations sur une formation spécifique
• Processus d'inscription
• Tarifs et certifications
• Contact et support

N'hésitez pas à me poser des questions plus précises !"""
    else:
        # Fallback si aucun document n'est trouvé
        greeting = "Bonjour ! Je suis Elavira, votre assistante FormEduc ! 🎓\n\n" if is_first_message else ""
        response = f"{greeting}Je suis là pour vous accompagner dans vos besoins de formation professionnelle. FormEduc vous propose :\n\n• **Secourisme** - Service de garde, petite enfance, milieu scolaire\n• **Formations 45h** - Pour RSG et RSGE\n• **Perfectionnements** - Développement de l'enfant, allergies, maltraitance\n• **Familles d'accueil** - Formations hybrides spécialisées\n• **Programme jeunesse** - Gardien futé et animateur de camp\n• **Formations en ligne** - 100% à distance, certifications reconnues\n\nNos formations sont développées par des experts du terrain avec une vraie expérience pratique. Que souhaitez-vous savoir en particulier ?"
    
    # Ajouter le message utilisateur et la réponse à la mémoire
    add_message(user_id, agent_id, "user", query)
    add_message(user_id, agent_id, "assistant", response)
    
    return response

# --- Test rapide (optionnel) ---
if __name__ == "__main__":
    try:
        result = subprocess.run([OLLAMA_BIN, "list"], capture_output=True, text=True, check=True)
        print("✅ Ollama accessible depuis Python :\n", result.stdout)
    except Exception as e:
        print("❌ Ollama introuvable depuis Python :", e)

    test_query = "Quels sont les programmes disponibles pour le secondaire ?"
    print(rag_generate(test_query, "Tu es un assistant professionnel spécialisé pour les élèves du secondaire."))
