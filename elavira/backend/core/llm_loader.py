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

# --- Initialisation du client ChromaDB ---
script_dir = os.path.dirname(__file__)
chroma_db_path = os.path.join(script_dir, "..", "chroma_data")
os.makedirs(chroma_db_path, exist_ok=True)

chroma_client = chromadb.PersistentClient(path=chroma_db_path)
collection = chroma_client.get_or_create_collection(name="elavira_collection")
print(f"✅ ChromaDB persistant à : {os.path.abspath(chroma_db_path)}")

# --- Initialisation du modèle d'embeddings SentenceTransformer ---
try:
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    print("✅ Embedder (SentenceTransformer 'all-MiniLM-L6-v2') initialisé.")
except Exception as e:
    raise RuntimeError(f"❌ Échec de l'initialisation de l'embedder : {e}")

# --- Fonctions pour indexer et requêter les documents ---
def index_documents(texts: List[str], ids: List[str] = None):
    if not texts:
        return []
    embeddings = embedder.encode(texts).tolist()
    metadatas = [{"source": f"doc_{i}"} for i in range(len(texts))]
    if ids is None:
        current_count = collection.count()
        ids = [f"doc_{current_count + i}" for i in range(len(texts))]
    collection.add(documents=texts, embeddings=embeddings, metadatas=metadatas, ids=ids)
    print(f"✅ {len(texts)} documents indexés dans ChromaDB.")
    return ids

def query_documents(query_text: str, n_results: int = 3) -> List[str]:
    if not query_text:
        return []
    query_embedding = embedder.encode([query_text]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results,
        include=['documents']
    )
    return results.get('documents', [[]])[0] if results.get('documents') else []

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
    # Persona optimisée pour Elavira selon le cahier des charges
    if system_persona is None:
        system_persona = """Tu es Elavira, l'assistante virtuelle de FormEduc, spécialisée dans les formations professionnelles. 

Ton rôle est de :
- Accueillir chaleureusement les visiteurs du site
- Répondre aux questions fréquentes sur les formations
- Accompagner les utilisateurs dans leur navigation
- Proposer des formations adaptées selon leur profil
- Assister tout au long du processus d'exploration ou d'achat

Ton style : Professionnel, chaleureux, bienveillant et motivant.
Réponds de manière claire, concise et contextualisée."""
    
    # Récupération du contexte de conversation
    conversation_context = get_conversation_context(user_id, agent_id, max_messages=3)
    
    # Récupération des documents les plus pertinents de Formeduc
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
    
    # Réponses optimisées selon le cahier des charges
    if "formation" in query.lower() or "programme" in query.lower() or "cours" in query.lower():
        response = f"Bonjour ! Je suis Elavira, votre assistante FormEduc ! 🎓\n\nJe vois que vous vous intéressez à nos formations. FormEduc propose un large éventail de formations professionnelles adaptées à vos besoins :\n\n• **Secourisme en ligne** - Formation complète avec certification\n• **Premiers soins** - Techniques d'urgence essentielles\n• **Formation SST** - Santé et sécurité au travail\n• **Formations en entreprise** - Programmes sur mesure\n\nPouvez-vous me dire quel est votre profil ? (éducateur, parent, professionnel de la santé, etc.) Cela m'aiderait à vous proposer la formation la plus adaptée !"
    elif "bonjour" in query.lower() or "salut" in query.lower() or "bonsoir" in query.lower():
        response = "Bonjour et bienvenue sur FormEduc ! 👋\n\nJe suis Elavira, votre assistante virtuelle. Je suis là pour vous accompagner dans votre recherche de formations professionnelles de qualité.\n\nComment puis-je vous aider aujourd'hui ? Vous pouvez me poser des questions sur nos formations, nos tarifs, nos certifications, ou tout simplement me dire ce que vous cherchez !"
    elif "tarif" in query.lower() or "prix" in query.lower() or "coût" in query.lower():
        response = f"Excellente question ! 💰\n\nNos tarifs varient selon le type de formation et votre profil :\n\n• **Formations individuelles** : Tarifs préférentiels pour les particuliers\n• **Formations en entreprise** : Devis personnalisés selon vos besoins\n• **Formations en ligne** : Accès flexible et économique\n\nPour obtenir un devis précis, pourriez-vous me préciser :\n- Le type de formation qui vous intéresse\n- Votre profil (particulier, entreprise, organisme)\n- Le nombre de participants\n\nJe pourrai alors vous orienter vers la meilleure option !"
    elif "certification" in query.lower() or "certificat" in query.lower() or "diplôme" in query.lower():
        response = f"Excellente question ! 🏆\n\nToutes nos formations délivrent des certifications reconnues :\n\n• **Certificats officiels** - Reconnus par les organismes compétents\n• **Attestations de formation** - Pour vos dossiers professionnels\n• **Certifications numériques** - Accessibles en ligne 24h/24\n• **Suivi post-formation** - Support continu après certification\n\nNos certifications sont reconnues dans votre domaine d'activité. Quelle formation vous intéresse pour que je vous donne plus de détails sur la certification spécifique ?"
    else:
        response = f"Bonjour ! Je suis Elavira, votre assistante FormEduc ! 🎓\n\nJe vois que vous me demandez : '{query}'\n\nJe suis là pour vous accompagner dans vos besoins de formation professionnelle. Je peux vous aider avec :\n\n• **Nos formations** : Secourisme, premiers soins, SST, formations en entreprise\n• **Nos tarifs** : Devis personnalisés selon votre profil\n• **Nos certifications** : Diplômes et attestations reconnus\n• **Le processus d'inscription** : Guide complet étape par étape\n\nQue souhaitez-vous savoir en particulier ?"
    
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
