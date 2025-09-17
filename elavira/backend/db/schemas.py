from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Schémas pour les agents
class AgentBase(BaseModel):
    name: str
    role: str
    specialty: str
    description: str
    prompt: str
    model: str
    avatar: str
    color: str
    knowledge_base: str

class AgentCreate(BaseModel):
    name: str
    role: str
    description: str
    prompt: str
    model: str
    specialty: Optional[str] = "Assistant"
    avatar: Optional[str] = "🤖"
    color: Optional[str] = "#3b82f6"
    knowledge_base: Optional[str] = "general"

class AgentUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    specialty: Optional[str] = None
    description: Optional[str] = None
    prompt: Optional[str] = None
    model: Optional[str] = None
    avatar: Optional[str] = None
    color: Optional[str] = None
    knowledge_base: Optional[str] = None
    is_active: Optional[bool] = None

class AgentResponse(AgentBase):
    id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Schémas pour les conversations
class ConversationBase(BaseModel):
    title: str
    agent_id: str

class ConversationCreate(ConversationBase):
    pass

class ConversationUpdate(BaseModel):
    title: Optional[str] = None
    agent_id: Optional[str] = None

class ConversationResponse(ConversationBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Schémas pour les messages
class MessageBase(BaseModel):
    text: str
    user_id: str
    agent_id: Optional[str] = None

class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    id: str
    timestamp: datetime
    conversation_id: Optional[str] = None

    class Config:
        from_attributes = True