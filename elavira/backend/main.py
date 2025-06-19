from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os

# --- Import des routeurs (si tu veux les activer plus tard) ---
from backend.api import routes_users
from backend.api import routes_chat
# from backend.api import routes_agents

# --- ChromaDB ---
import chromadb

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
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routeurs utilisateurs/chat ---
app.include_router(routes_users.router)
app.include_router(routes_chat.router)
# app.include_router(routes_agents.router)  # À activer plus tard

# --- ChromaDB Setup ---
def get_chroma_client(persistent: bool = True, path: str = "./chroma_data"):
    if persistent:
        os.makedirs(path, exist_ok=True)
        print(f"✅ ChromaDB persistant à : {os.path.abspath(path)}")
        return chromadb.PersistentClient(path=path)
    else:
        print("🧪 Client ChromaDB en mémoire")
        return chromadb.Client()

def get_chroma_collection(client, name="elavira_collection"):
    return client.get_or_create_collection(name)

# --- Initialisation ChromaDB ---
script_dir = os.path.dirname(__file__)
chroma_db_path = os.path.join(script_dir, "chroma_data")

chroma_client = get_chroma_client(persistent=True, path=chroma_db_path)
collection = get_chroma_collection(chroma_client, "elavira_collection")

# --- Modèles ---
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

@app.post("/add_documents/")
async def add_documents(request: AddDocumentsRequest):
    try:
        print(f"📥 Documents reçus : {request.texts}")
        ids = [f"doc_{i}" for i in range(collection.count(), collection.count() + len(request.texts))]
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