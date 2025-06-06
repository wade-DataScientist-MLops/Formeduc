from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Agent
from schemas import AgentCreate, AgentOut

router = APIRouter(prefix="/agents", tags=["Agents"])

@router.get("/", response_model=list[AgentOut])
def list_agents(db: Session = Depends(get_db)):
    return db.query(Agent).all()

@router.post("/", response_model=AgentOut)
def create_agent(agent: AgentCreate, db: Session = Depends(get_db)):
    db_agent = db.query(Agent).filter(Agent.id == agent.id).first()
    if db_agent:
        raise HTTPException(status_code=400, detail="Agent already exists")
    new_agent = Agent(id=agent.id, name=agent.name)
    db.add(new_agent)
    db.commit()
    db.refresh(new_agent)
    return new_agent
