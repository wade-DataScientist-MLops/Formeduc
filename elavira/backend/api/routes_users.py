# backend/api/routes_users.py

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from passlib.context import CryptContext # Pour le hachage de mot de passe
from typing import Dict

# Crée une instance de APIRouter pour les routes des utilisateurs
router = APIRouter(
    prefix="/users", # Toutes les routes ici commenceront par /users
    tags=["Users"]   # Pour l'organisation dans la documentation Swagger/OpenAPI
)

# --- Configuration du hachage de mot de passe ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# --- Modèles Pydantic pour les utilisateurs ---
class UserCreate(BaseModel):
    username: str
    password: str

class UserInDB(BaseModel):
    username: str
    hashed_password: str

class Token(BaseModel): # Pour la réponse de connexion (sans JWT pour l'instant)
    access_token: str
    token_type: str

# --- Simulation d'une base de données d'utilisateurs (en mémoire) ---
# Cette approche n'est PAS persistante et sera effacée à chaque redémarrage du serveur.
# Pour la persistance, nous utiliserons une vraie base de données plus tard.
fake_users_db: Dict[str, UserInDB] = {}

# --- Routes des utilisateurs ---

@router.get("/")
async def read_users_status():
    """
    Endpoint de test pour vérifier que les routes utilisateurs fonctionnent.
    """
    return {"message": "Users routes are working!", "status": "active"}

@router.post("/register/", response_model=UserCreate, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate):
    """
    Enregistre un nouvel utilisateur.
    """
    if user.username in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le nom d'utilisateur existe déjà."
        )
    hashed_password = get_password_hash(user.password)
    fake_users_db[user.username] = UserInDB(username=user.username, hashed_password=hashed_password)
    return user # Retourne le username sans le mot de passe haché

@router.post("/login/", response_model=Token)
async def login_for_access_token(user: UserCreate): # Utilise le même modèle pour l'entrée de login
    """
    Connecte un utilisateur et retourne un token (simulation).
    """
    db_user = fake_users_db.get(user.username)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nom d'utilisateur ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Pour l'instant, nous retournons un token bidon.
    # Plus tard, ce sera un JWT réel.
    return {"access_token": "fake-access-token", "token_type": "bearer"}

# @router.get("/me/")
# async def read_users_me():
#     """
#     Endpoint pour récupérer l'utilisateur connecté (requiert authentification).
#     Sera implémenté avec JWT dans une étape ultérieure.
#     """
#     return {"username": "current_user"} # Placeholder