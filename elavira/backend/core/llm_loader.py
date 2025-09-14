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
    # Persona optimisée pour Elavira selon le site FormEduc
    if system_persona is None:
        system_persona = """Tu es Elavira, l'assistante virtuelle de FormEduc, spécialisée dans les formations pour les professionnels de la petite enfance et du milieu scolaire.

FormEduc propose :
- Secourisme service de garde (petite enfance, milieu scolaire)
- Formations 45h pour RSG et RSGE
- Perfectionnements pour éducatrices et éducateurs
- Familles d'accueil (formations hybrides)
- Programme jeunesse (gardien futé, animateur de camp)
- Formations 100% en ligne avec certifications reconnues

Tes réponses doivent être conformes aux réglementations québécoises (Règlement sur les services de garde éducatifs, Loi sur l'instruction publique).

Ton style : Professionnel, chaleureux, bienveillant et expert en petite enfance."""
    
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
    
    # Vérifier si c'est le premier message ou une conversation continue
    is_first_message = len(conversation_context.split('\n')) <= 2
    
    # Réponses optimisées avec le contenu réel du site FormEduc
    if "formation" in query.lower() or "programme" in query.lower() or "cours" in query.lower():
        greeting = "Bonjour ! Je suis Elavira, votre assistante FormEduc ! 🎓\n\n" if is_first_message else ""
        response = f"{greeting}Je vois que vous vous intéressez à nos formations. FormEduc propose des formations spécialisées pour les professionnels de la petite enfance et du milieu scolaire :\n\n• **Secourisme service de garde** - Adapté à la petite enfance (8h) et milieu scolaire\n• **Formations garderie** - Programme de 45h pour RSG/RSGE\n• **Familles d'accueil** - Formations hybrides spécialisées\n• **Programme jeunesse** - Cours de gardien futé et animateur de camp\n• **Formations en ligne** - Accès 24h/24, certifications reconnues\n\nNos formations sont conformes au Règlement sur les services de garde éducatifs et à la Loi sur l'instruction publique. Quel est votre profil professionnel ?"
    elif "bonjour" in query.lower() or "salut" in query.lower() or "bonsoir" in query.lower():
        response = "Bonjour et bienvenue sur FormEduc ! 👋\n\nJe suis Elavira, votre assistante virtuelle spécialisée dans les formations pour les professionnels de la petite enfance et du milieu scolaire.\n\nFormEduc vous propose :\n• **Secourisme** adapté à la petite enfance et milieu scolaire\n• **Formations 45h** pour RSG et RSGE\n• **Perfectionnements** pour éducatrices et éducateurs\n• **Formations en ligne** avec certifications reconnues\n\nComment puis-je vous aider aujourd'hui ?"
    elif "tarif" in query.lower() or "prix" in query.lower() or "coût" in query.lower():
        response = f"Excellente question ! 💰\n\nNos tarifs varient selon le type de formation et votre profil :\n\n• **Formations individuelles** : Tarifs préférentiels pour les particuliers\n• **Formations en entreprise** : Devis personnalisés selon vos besoins\n• **Formations en ligne** : Accès flexible et économique\n\nPour obtenir un devis précis, pourriez-vous me préciser :\n- Le type de formation qui vous intéresse\n- Votre profil (particulier, entreprise, organisme)\n- Le nombre de participants\n\nJe pourrai alors vous orienter vers la meilleure option !"
    elif "certification" in query.lower() or "certificat" in query.lower() or "diplôme" in query.lower():
        response = f"Excellente question ! 🏆\n\nToutes nos formations délivrent des certifications reconnues :\n\n• **Certificats conformes** au Règlement sur les services de garde éducatifs en milieu scolaire\n• **Attestations** conformes à la Loi sur l'instruction publique (chapitre l-13.3, a. 454.1)\n• **Certifications numériques** - Accessibles en ligne 24h/24\n• **Formations 100% en ligne** - Accès où que vous soyez, à tout moment\n\nNos certifications sont reconnues par les organismes de services de garde. Quelle formation vous intéresse ?"
    elif "rsg" in query.lower() or "rsge" in query.lower() or "responsable" in query.lower():
        greeting = "Parfait ! Vous vous intéressez aux formations pour responsables de service de garde ! 🏠\n\n" if is_first_message else "Parfait ! 🏠\n\n"
        response = f"{greeting}FormEduc propose des formations spécialisées pour RSG et RSGE :\n\n• **Formation obligatoire de 45 heures** pour RSGE\n• **Le programme éducatif** en service de garde\n• **Le développement de l'enfant** - Formation complète\n• **Santé, sécurité et alimentation**\n• **Le rôle de la responsable** d'un service de garde\n\nCes formations sont essentielles pour exercer légalement en service de garde familial. Souhaitez-vous plus d'informations sur une formation spécifique ?"
    elif "secourisme" in query.lower() or "premiers soins" in query.lower():
        response = f"Excellent choix ! 🚑\n\nFormEduc propose des formations de secourisme spécialisées :\n\n• **Secourisme adapté à la petite enfance** - 8 heures en ligne\n• **Renouvellement** de secourisme petite enfance - 6 heures\n• **Secourisme en milieu scolaire** - Formation en ligne\n• **Secourisme pour chauffeur d'autobus** - Enfants d'âge scolaire, 8 heures\n• **Trousse de premiers soins** pour garderie\n\nToutes nos formations de secourisme sont adaptées aux besoins spécifiques des professionnels de la petite enfance et du milieu scolaire. Quelle formation vous intéresse ?"
    elif "perfectionnement" in query.lower() or "développement" in query.lower():
        response = f"Parfait ! 📚\n\nFormEduc propose de nombreux cours de perfectionnement pour éducatrices et éducateurs :\n\n• **Développement de l'enfant** - Formation complète et assistant/remplaçant\n• **Allergies ? Je réagis !** - Gestion des allergies en garderie\n• **Bien dormir pour bien grandir** - Troubles du sommeil\n• **Briser la chaîne infectieuse** - Prévention des infections\n• **Cultiver l'intelligence émotionnelle** de l'enfant\n• **De A à Z… 26 techniques d'intervention**\n• **La maltraitance** - Intervenir pour protéger l'enfant\n• **Le développement langagier** - Acquisition et dépistage\n\nCes formations vous permettent d'améliorer vos compétences professionnelles. Quel sujet vous intéresse ?"
    else:
        greeting = "Je vois que vous me demandez : '{query}'\n\n" if is_first_message else "Je comprends : '{query}'\n\n"
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
