from sqlalchemy import Column, String
from database import Base

class Agent(Base):
    __tablename__ = "agents"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
