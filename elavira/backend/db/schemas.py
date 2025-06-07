
# backend/db/schemas.py

from pydantic import BaseModel, EmailStr
from typing import Optional
import datetime

# Schéma de base pour un utilisateur
class UserBase(BaseModel):
    email: EmailStr
    username: str

# Schéma pour la création d'un nouvel utilisateur (inclut le mot de passe)
class UserCreate(UserBase):
    password: str

# Schéma pour la mise à jour d'un utilisateur (tous les champs sont optionnels)
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None

# Schéma pour un utilisateur tel qu'il sera retourné par l'API
# (n'inclut pas le mot de passe pour des raisons de sécurité)
class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True # Permet à Pydantic de lire les données d'un objet ORM SQLAlchemy