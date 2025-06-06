from fastapi import FastAPI
from database import Base, engine
from routes_agents import router as agents_router

app = FastAPI()

# Création des tables (exécuter une fois au lancement)
Base.metadata.create_all(bind=engine)

app.include_router(agents_router)
