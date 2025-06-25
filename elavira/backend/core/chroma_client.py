import os
import chromadb
from sentence_transformers import SentenceTransformer # <-- Ajoutez cette ligne

def get_chroma_client(persistent=True, path="./backend/chroma_data"):
    if persistent:
        os.makedirs(path, exist_ok=True)
        print(f"✅ ChromaDB persistant à : {path}") # Ajout pour confirmer le chemin
        return chromadb.PersistentClient(path=path)
    else:
        return chromadb.Client()

chroma_client = get_chroma_client()
collection = chroma_client.get_or_create_collection("elavira_collection")

# --- AJOUTEZ CETTE LIGNE POUR DÉFINIR L'EMBEDDER ---
# Choisissez un modèle d'embedding. 'all-MiniLM-L6-v2' est un bon choix polyvalent et léger.
embedder = SentenceTransformer('all-MiniLM-L6-v2')