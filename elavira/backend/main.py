
from fastapi import FastAPI
from .db.database import init_db
from contextlib import asynccontextmanager

# 🟢 Import du routeur chat
from .api.routes_chat import router as chat_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Démarrage de l'application Elavira...")
    init_db()
    print("Base de données initialisée.")
    yield
    print("Arrêt de l'application Elavira...")

app = FastAPI(
    title="Elavira Backend API",
    description="API pour la plateforme Elavira, un assistant IA intelligent.",
    version="0.1.0",
    lifespan=lifespan
)

# ✅ Inclusion effective du routeur chat
app.include_router(chat_router)

# Route test
@app.get("/")
async def read_root():
    return {"message": "Bienvenue sur l'API Backend d'Elavira !"}
