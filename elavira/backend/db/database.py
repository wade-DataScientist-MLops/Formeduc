# backend/db/database.py

# ... (vos imports, par exemple de dotenv, os, sqlalchemy)


# Ancienne ligne pour PostgreSQL :
# engine = create_engine(SQLALCHEMY_DATABASE_URL)

# ... (le reste du code)
# backend/db/database.py

# ... (vos imports, assurez-vous que 'os' et 'create_engine' sont importés)
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# --- DÉBUT DE LA MODIFICATION ICI ---
if SQLALCHEMY_DATABASE_URL and SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    # Pour SQLite, nous devons ajouter connect_args={"check_same_thread": False}
    # car SQLite n'est pas conçu pour l'accès multithread par défaut.
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
elif SQLALCHEMY_DATABASE_URL: # Si c'est autre chose que SQLite (ex: PostgreSQL)
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
else:
    # Gérer le cas où DATABASE_URL n'est pas défini (cela ne devrait pas arriver avec load_dotenv)
    raise ValueError("DATABASE_URL non défini dans le fichier .env")
# --- FIN DE LA MODIFICATION ICI ---

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    # Cette ligne créera les tables dans votre fichier sqlite.db
    Base.metadata.create_all(bind=engine)
    print("Base de données initialisée.")

# ... (le reste de votre code, par exemple, la fonction get_db)