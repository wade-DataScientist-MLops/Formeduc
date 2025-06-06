
from pydantic import BaseModel

class AgentBase(BaseModel):
    id: str
    name: str

class AgentCreate(AgentBase):
    pass

class AgentOut(AgentBase):
    class Config:
        orm_mode = True
