# Fichier: backend/core/llm_loader.py

import os
import subprocess
from typing import List
import chromadb
from sentence_transformers import SentenceTransformer

# Pour éviter le warning parallelism Huggingface (optionnel)
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# --- Initialisation du client ChromaDB ---
# Utilisation de la méthode moderne chromadb.PersistentClient()
# Le chemin d'accès est corrigé pour être relatif au répertoire du script.
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
    print(f"❌ Erreur lors de l'initialisation de SentenceTransformer : {e}")
    raise RuntimeError(f"Échec de l'initialisation de l'embedder : {e}")

# --- Fonctions pour indexer et requêter les documents dans Chroma ---

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

# --- Fonction pour générer la réponse avec Ollama via CLI (externe) ---

def ollama_generate(prompt: str) -> str:
    print(f"[Ollama CLI] Envoi du prompt (début): {prompt[:100]}...")
    try:
        result = subprocess.run(
            ["ollama", "run", "elavira"],
            input=prompt.encode('utf-8'),
            capture_output=True,
            # text=True, # <--- CETTE LIGNE EST SUPPRIMÉE
            check=True,
            timeout=300
        )
        # Décodage manuel de stdout et stderr avec gestion des erreurs
        response_stdout = result.stdout.decode('utf-8', errors='replace').strip()
        response_stderr = result.stderr.decode('utf-8', errors='replace').strip()

        if response_stderr:
            print(f"[Ollama CLI] Erreur STDERR : {response_stderr}")
            # Si stdout est vide mais stderr contient une erreur, la renvoyer
            if not response_stdout:
                return f"Erreur Ollama (stderr) : {response_stderr}"

        print(f"[Ollama CLI] Réponse reçue (début): {response_stdout[:200]}...")
        return response_stdout
    except subprocess.CalledProcessError as e:
        # e.stderr est de type bytes ici, donc le décoder
        stderr_decoded = e.stderr.decode('utf-8', errors='replace').strip()
        print(f"[Ollama CLI] Erreur commande : {stderr_decoded}")
        return f"Erreur Ollama : {stderr_decoded or 'détails non disponibles'}"
    except FileNotFoundError:
        print("[Ollama CLI] Commande 'ollama' introuvable.")
        return "Erreur : programme Ollama introuvable. Assurez-vous qu'Ollama est installé et que le modèle 'elavira' est téléchargé."
    except Exception as e:
        # Convertir explicitement l'objet exception en chaîne de caractères
        error_message = str(e)
        print(f"[Ollama CLI] Erreur inattendue : {error_message}")
        return f"Erreur inattendue lors de l'appel Ollama : {error_message}"

# --- Fonction principale pour générer la réponse RAG ---

# Fichier: backend/core/llm_loader.py

# ... (vos imports existants)

# --- Fonction principale pour générer la réponse RAG ---
# MODIFICATION CLÉ ICI : Ajout de system_persona comme argument
def rag_generate(query: str, system_persona: str) -> str: # <-- Ajout de system_persona
    # 1. Rechercher les documents pertinents dans la base de données vectorielle
    context_docs = query_documents(query, n_results=5)
    context = "\n\n".join(context_docs)
    
    # 2. Créer le prompt pour le LLM avec le contexte ET la persona dynamique
    prompt = f"""
{system_persona} # <-- Utilisation de la persona passée en argument

Voici des extraits du catalogue de Formeduc :
---
{context}
---

Réponds à la question suivante uniquement à partir des informations fournies. Si la réponse n’est pas dans le contexte, indique-le poliment sans inventer de réponse.

Question :
{query}

Réponse :
"""
    # 3. Générer la réponse finale avec Ollama
    return ollama_generate(prompt)