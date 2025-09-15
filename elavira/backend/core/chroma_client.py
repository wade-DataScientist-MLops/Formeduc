import os
import chromadb
from sentence_transformers import SentenceTransformer
from typing import List
import requests
import json

# Pour éviter le warning parallelism Huggingface (optionnel)
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# --- Initialisation du client ChromaDB ---
def get_chroma_client(persistent: bool = True, path: str = "./backend/chroma_data"):
    if persistent:
        os.makedirs(path, exist_ok=True)
        print(f"✅ ChromaDB persistant à : {os.path.abspath(path)}")
        return chromadb.PersistentClient(path=path)
    else:
        print("🧪 Client ChromaDB en mémoire (non persistant)")
        return chromadb.Client()

# Client et collections globales
chroma_client = get_chroma_client()
elavira_collection = chroma_client.get_or_create_collection("elavira_collection")
solenys_collection = chroma_client.get_or_create_collection("solenys_collection")

# Collection par défaut pour compatibilité
collection = elavira_collection

# --- Embedder SentenceTransformer ---
try:
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    print("✅ Embedder (SentenceTransformer 'all-MiniLM-L6-v2') initialisé.")
except Exception as e:
    print(f"❌ Erreur lors de l'initialisation de SentenceTransformer : {e}")
    raise RuntimeError(f"Échec de l'initialisation de l'embedder : {e}")

# --- Fonctions utilitaires ---

def index_documents(texts: List[str], ids: List[str] = None, collection_name: str = "elavira"):
    if not texts:
        print("Aucun texte à indexer.")
        return []

    # Sélectionner la bonne collection
    target_collection = elavira_collection if collection_name == "elavira" else solenys_collection

    embeddings = embedder.encode(texts).tolist()
    metadatas = [{"source": f"doc_{i}"} for i in range(len(texts))]

    if ids is None:
        current_count = target_collection.count()
        ids = [f"doc_{current_count + i}" for i in range(len(texts))]

    target_collection.add(documents=texts, embeddings=embeddings, metadatas=metadatas, ids=ids)
    print(f"✅ {len(texts)} documents indexés dans la collection {collection_name}.")
    return ids

def query_documents(query_text: str, n_results: int = 3, collection_name: str = "elavira") -> List[str]:
    if not query_text:
        return []

    # Sélectionner la bonne collection
    target_collection = elavira_collection if collection_name == "elavira" else solenys_collection

    query_embedding = embedder.encode([query_text]).tolist()

    results = target_collection.query(
        query_embeddings=query_embedding,
        n_results=n_results,
        include=['documents']
    )
    return results.get('documents', [[]])[0] if results.get('documents') else []

# --- Fonction Ollama generate corrigée ---

def ollama_generate(prompt_text: str) -> str:
    print(f"[Ollama API] Envoi du prompt : {prompt_text[:100]}...")
    try:
        # Utiliser l'API HTTP d'Ollama
        url = "http://ollama:11434/api/generate"
        data = {
            "model": "llama3.2:1b",
            "prompt": prompt_text,
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
        
        print(f"[Ollama API] Réponse reçue : {generated_text[:200]}...")
        return generated_text
        
    except requests.exceptions.RequestException as e:
        print(f"[Ollama API] Erreur de connexion : {e}")
        return f"Erreur de connexion Ollama : {e}"
    except Exception as e:
        print(f"[Ollama API] Erreur inattendue : {e}")
        return f"Erreur inattendue : {e}"