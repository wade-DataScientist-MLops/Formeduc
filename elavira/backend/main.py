import os
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Assurez-vous que ces modules existent dans api
from api import routes_users
from api import routes_chat
from api import solenys_router

# --- ChromaDB ---
import chromadb
# La classe Settings est nécessaire pour la configuration de la dépréciation, mais pas pour le client persistant
from sentence_transformers import SentenceTransformer

# --- Initialisation FastAPI ---
app = FastAPI(
    title="API Elavira",
    description="Une API pour l'assistant intelligent Elavira",
    version="0.0.1",
)

# --- CORS ---
origins = [
    "http://localhost",
    "http://127.0.0.1:8000",
    "http://localhost:3000",   # React
    "http://localhost:8501",   # Streamlit
    "http://104.254.182.118:3000",  # React sur serveur
    "http://104.254.182.118:8000",  # Backend sur serveur
    "http://104.254.182.118",       # Serveur principal
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Inclusion des routeurs ---
app.include_router(routes_users.router)
app.include_router(routes_chat.router)
# Ajout d'un prefixe /solenys pour ce routeur
app.include_router(solenys_router.router, prefix="/solenys")

# --- ChromaDB Setup (CORRIGÉ) ---
script_dir = os.path.dirname(__file__)
chroma_db_path = os.path.join(script_dir, "chroma_data")
os.makedirs(chroma_db_path, exist_ok=True) # S'assurer que le dossier existe

# Utilisation de la nouvelle API de ChromaDB pour le client persistant, qui résout la ValueError
chroma_client = chromadb.PersistentClient(path=chroma_db_path)

collection = chroma_client.get_or_create_collection(name="elavira_collection")

print(f"✅ ChromaDB persistant à : {os.path.abspath(chroma_db_path)}")

# --- Embedder SentenceTransformer ---
try:
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    print("✅ Embedder (SentenceTransformer 'all-MiniLM-L6-v2') initialisé.")
except Exception as e:
    print(f"❌ Erreur lors de l'initialisation de SentenceTransformer : {e}")
    raise RuntimeError(f"Échec de l'initialisation de l'embedder : {e}")

# --- Modèles Pydantic ---
class AddDocumentsRequest(BaseModel):
    texts: List[str]

class EmbeddingItem(BaseModel):
    id: str
    embedding: List[float]
    document: str

class QueryRequest(BaseModel):
    query_embedding: List[float]
    n_results: int = 5

# --- Endpoints ---
@app.get("/")
async def read_root():
    return {"message": "Bienvenue sur l'API Elavira!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "elavira-api"}

@app.post("/add_documents/")
async def add_documents(request: AddDocumentsRequest):
    try:
        print(f"📥 Documents reçus : {request.texts}")
        start_index = collection.count()
        ids = [f"doc_{i}" for i in range(start_index, start_index + len(request.texts))]
        collection.add(documents=request.texts, ids=ids)
        print(f"✅ {len(request.texts)} documents ajoutés.")
        return {"message": "Documents ajoutés", "ids": ids}
    except Exception as e:
        print(f"❌ Erreur ajout documents : {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur ajout documents : {str(e)}")

@app.post("/chroma/add_embedding/")
async def add_embedding(item: EmbeddingItem):
    try:
        collection.add(
            ids=[item.id],
            embeddings=[item.embedding],
            documents=[item.document]
        )
        return {"status": "embedding added", "id": item.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur ajout embedding : {str(e)}")

@app.post("/chroma/query/")
async def query_embedding(request: QueryRequest):
    try:
        results = collection.query(
            query_embeddings=[request.query_embedding],
            n_results=request.n_results,
            include=['documents', 'distances', 'metadatas']
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur requête embeddings : {str(e)}")