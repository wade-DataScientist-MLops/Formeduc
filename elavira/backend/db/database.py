
# backend/db/database.py

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer l'URL de la base de données depuis les variables d'environnement
# Assurez-vous d'avoir une variable DATABASE_URL dans votre .env
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set. Please check your .env file.")

# Créer le moteur de la base de données
# echo=True affichera les requêtes SQL générées dans la console (utile pour le débogage)
engine = create_engine(DATABASE_URL, echo=True)

# Créer une fabrique de sessions pour interagir avec la base de données
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base déclarative qui sera héritée par tous vos modèles SQLAlchemy
Base = declarative_base()

# Dépendance pour obtenir une session de base de données
# C'est une fonction génératrice qui fournira une session à chaque requête FastAPI
# et la fermera automatiquement après.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Fonction pour initialiser la base de données (créer les tables)
# Vous appellerez cette fonction au démarrage de l'application ou via un script
def init_db():
    Base.metadata.create_all(bind=engine)
    print("Tables de la base de données créées ou déjà existantes.")