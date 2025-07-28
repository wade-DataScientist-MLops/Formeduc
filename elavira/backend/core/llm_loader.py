from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from ollama import generate

# Initialiser l'embedding model
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Initialiser le client Chroma
chroma_client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="db"  # Chemin vers ta base de données Chroma
))

# Charger la collection d'embeddings
collection = chroma_client.get_or_create_collection(name="docs")


def get_context(query: str, k: int = 5) -> str:
    """Retourne les documents les plus pertinents pour la requête."""
    query_embedding = embedding_model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )
    documents = results["documents"][0] if results["documents"] else []
    return "\n\n".join(documents)


def rag_generate(query: str, model: str = "mistral") -> str:
    """Génère une réponse à partir d’un contexte extrait avec embeddings."""
    context = get_context(query)

    prompt = f"""
Tu es Elavira, une assistante virtuelle professionnelle pour Formeduc, spécialisée dans les formations au Québec. Tu réponds aux utilisateurs de manière claire, précise et polie. Tu t'exprimes de façon professionnelle et respectueuse, sans humour ni digression.

Voici des extraits du catalogue de Formeduc :
---
{context}
---

Réponds à la question suivante uniquement à partir des informations fournies. Si la réponse n’est pas dans le contexte, indique-le poliment sans inventer de réponse.

Question :
{query}

Réponse :
"""

    response = generate(
        model=model,
        prompt=prompt,
        options={"temperature": 0.1}  # plus fiable, moins créatif
    )
    return response['response'].strip()
