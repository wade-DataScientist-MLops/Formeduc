# Fichier: backend/core/llm_loader.py

import os
import subprocess
from typing import List
import chromadb
from sentence_transformers import SentenceTransformer

# --- Pour éviter le warning parallelism Huggingface (optionnel) ---
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# --- Ajouter le chemin vers Ollama au PATH pour macOS Apple Silicon ---
ollama_path = "/opt/homebrew/bin"
if ollama_path not in os.environ["PATH"]:
    os.environ["PATH"] += os.pathsep + ollama_path

OLLAMA_BIN = os.path.join(ollama_path, "ollama")  # Chemin absolu correct
MODEL_NAME = "qwen2:1.5b"  # Modèle utilisé

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
    print(f"[Ollama CLI] Envoi du prompt (début) : {prompt[:100]}...")
    try:
        result = subprocess.run(
            [OLLAMA_BIN, "run", MODEL_NAME],
            input=prompt.encode('utf-8'),
            capture_output=True,
            check=True,
            timeout=300
        )
        stdout = result.stdout.decode('utf-8', errors='replace').strip()
        stderr = result.stderr.decode('utf-8', errors='replace').strip()
        if stderr and not stdout:
            return f"Erreur Ollama (stderr) : {stderr}"
        return stdout
    except FileNotFoundError:
        return f"Erreur : programme Ollama introuvable à {OLLAMA_BIN}."
    except subprocess.CalledProcessError as e:
        return f"Erreur Ollama : {e.stderr.decode('utf-8', errors='replace').strip()}"
    except Exception as e:
        return f"Erreur inattendue lors de l'appel Ollama : {str(e)}"

# --- Fonction principale pour générer la réponse RAG ---
def rag_generate(query: str, system_persona: str) -> str:
    """
    Génère une réponse en combinant le contexte ChromaDB et le modèle Ollama.
    """
    # Récupération des documents les plus pertinents
    context_docs = query_documents(query, n_results=5)
    context = "\n\n".join(context_docs) if context_docs else "Aucun contexte disponible."

    # Construction du prompt
    prompt = f"""
{system_persona}

Voici des extraits du catalogue de Formeduc :
---
{context}
---

Réponds à la question suivante uniquement à partir des informations fournies. 
Si la réponse n’est pas dans le contexte, indique-le poliment sans inventer de réponse.

Question :
{query}

Réponse :
"""
    return ollama_generate(prompt)

# --- Test rapide (optionnel) ---
if __name__ == "__main__":
    try:
        result = subprocess.run([OLLAMA_BIN, "list"], capture_output=True, text=True, check=True)
        print("✅ Ollama accessible depuis Python :\n", result.stdout)
    except Exception as e:
        print("❌ Ollama introuvable depuis Python :", e)

    test_query = "Quels sont les programmes disponibles pour le secondaire ?"
    print(rag_generate(test_query, "Tu es un assistant professionnel spécialisé pour les élèves du secondaire."))
