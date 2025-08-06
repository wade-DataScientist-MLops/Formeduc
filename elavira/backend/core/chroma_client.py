import os
import chromadb
from sentence_transformers import SentenceTransformer
from typing import List
import subprocess

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

# Client et collection globale
chroma_client = get_chroma_client()
collection = chroma_client.get_or_create_collection("elavira_collection")

# --- Embedder SentenceTransformer ---
try:
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    print("✅ Embedder (SentenceTransformer 'all-MiniLM-L6-v2') initialisé.")
except Exception as e:
    print(f"❌ Erreur lors de l'initialisation de SentenceTransformer : {e}")
    raise RuntimeError(f"Échec de l'initialisation de l'embedder : {e}")

# --- Fonctions utilitaires ---

def index_documents(texts: List[str], ids: List[str] = None):
    if not texts:
        print("Aucun texte à indexer.")
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

# --- Fonction Ollama generate corrigée ---

def ollama_generate(prompt_text: str) -> str:
    print(f"[Ollama CLI] Envoi du prompt via stdin : {prompt_text[:100]}...")
    try:
        command = ["ollama", "run", "elavira"]
        result = subprocess.run(
            command,
            input=prompt_text,  # prompt envoyé via stdin
            capture_output=True,
            text=True,
            check=True,
            timeout=300
        )
        response = result.stdout.strip()
        print(f"[Ollama CLI] Réponse reçue : {response[:200]}...")
        return response
    except subprocess.CalledProcessError as e:
        print(f"[Ollama CLI] Erreur commande : {e.stderr}")
        return f"Erreur Ollama : {e.stderr or 'détails non disponibles'}"
    except FileNotFoundError:
        print("[Ollama CLI] Commande 'ollama' introuvable.")
        return "Erreur : programme Ollama introuvable."
    except Exception as e:
        print(f"[Ollama CLI] Erreur inattendue : {e}")
        return f"Erreur inattendue : {e}"