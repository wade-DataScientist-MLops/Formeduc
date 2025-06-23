import chromadb
from sentence_transformers import SentenceTransformer
import subprocess

# Initialisation globale
model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="./chroma_data")
collection = client.get_or_create_collection(name="formeduc_secourisme")

def index_documents(texts, ids=None):
    embeddings = model.encode(texts).tolist()
    metadatas = [{"source": f"doc_{i}"} for i in range(len(texts))]
    if ids is None:
        ids = [f"id_{i}" for i in range(len(texts))]
    collection.add(documents=texts, embeddings=embeddings, metadatas=metadatas, ids=ids)

def query_documents(query, n_results=3):
    query_embedding = model.encode([query]).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=n_results)
    return results["documents"][0] if results["documents"] else []

def ollama_generate(prompt: str) -> str:
    try:
        result = subprocess.run(
            ["ollama", "generate", "elavira", "--prompt", prompt],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Erreur Ollama : {e}"
