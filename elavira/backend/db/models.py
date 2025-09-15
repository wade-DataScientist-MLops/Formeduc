# backend/db/models.py

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

# Modèle de l'utilisateur
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"

# Modèle des agents
class Agent(Base):
    __tablename__ = "agents"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    role = Column(String, nullable=False)
    specialty = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    prompt = Column(Text, nullable=False)
    model = Column(String, nullable=False, default="llama3.2:1b")
    avatar = Column(String, nullable=False, default="🤖")
    color = Column(String, nullable=False, default="#6b7280")
    knowledge_base = Column(String, nullable=False, default="custom")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Agent(id={self.id}, name='{self.name}')>"

# Modèle des conversations
class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    agent_id = Column(String, ForeignKey("agents.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relations
    agent = relationship("Agent")
    user = relationship("User")
    messages = relationship("Message", back_populates="conversation")

    def __repr__(self):
        return f"<Conversation(id={self.id}, title='{self.title}')>"

# Modèle des messages
class Message(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    user_id = Column(String, nullable=False)  # ID de l'utilisateur ou de l'agent
    agent_id = Column(String, ForeignKey("agents.id"), nullable=True)
    conversation_id = Column(String, ForeignKey("conversations.id"), nullable=True)
    timestamp = Column(DateTime, server_default=func.now())

    # Relations
    agent = relationship("Agent")
    conversation = relationship("Conversation", back_populates="messages")

    def __repr__(self):
        return f"<Message(id={self.id}, user_id='{self.user_id}')>"