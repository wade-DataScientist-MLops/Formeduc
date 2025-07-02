# backend/api/routes_users.py

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from passlib.context import CryptContext
from typing import Dict
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer

# Router FastAPI
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# --- Sécurité & config JWT ---
SECRET_KEY = "une_clef_ultra_secrete_a_changer"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 pour lecture du token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login/")

# --- Models Pydantic ---
class UserCreate(BaseModel):
    username: str
    password: str

class UserInDB(BaseModel):
    username: str
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# --- Base simulée ---
fake_users_db: Dict[str, UserInDB] = {}

# --- Fonctions Auth ---
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_user(username: str):
    return fake_users_db.get(username)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token invalide")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalide")

    user = get_user(username)
    if user is None:
        raise HTTPException(status_code=401, detail="Utilisateur non trouvé")
    return user

# --- ROUTES ---

@router.get("/")
async def read_users_status():
    return {"message": "Users routes are working!", "status": "active"}

@router.post("/register/", response_model=UserCreate, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="Nom d'utilisateur déjà pris")
    
    hashed_password = get_password_hash(user.password)
    fake_users_db[user.username] = UserInDB(
        username=user.username,
        hashed_password=hashed_password
    )
    return user

@router.post("/login/", response_model=Token)
async def login_for_access_token(user: UserCreate):
    db_user = get_user(user.username)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Nom d'utilisateur ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me/")
async def read_users_me(current_user: UserInDB = Depends(get_current_user)):
    return {"username": current_user.username}
