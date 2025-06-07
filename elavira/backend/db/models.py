# backend/db/models.py

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base # Importer la Base déclarative que nous avons définie

# Modèle de l'utilisateur
class User(Base):
    __tablename__ = "users" # Nom de la table dans la base de données

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False) # Le mot de passe haché
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Exemple de relation : un utilisateur peut avoir plusieurs "documents"
    # documents = relationship("Document", back_populates="owner")

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"

# (Optionnel) Exemple de modèle pour un document, pour illustrer une relation
# class Document(Base):
#     __tablename__ = "documents"
#
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True, nullable=False)
#     content = Column(String)
#     vector_id = Column(String, unique=True, nullable=True) # ID du vecteur dans Chroma/Weaviate
#     owner_id = Column(Integer, ForeignKey("users.id"))
#     created_at = Column(DateTime, server_default=func.now())
#     updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
#
#     owner = relationship("User", back_populates="documents")
#
#     def __repr__(self):
#         return f"<Document(id={self.id}, title='{self.title}')>"