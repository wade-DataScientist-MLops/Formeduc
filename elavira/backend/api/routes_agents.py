from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import uuid

from db.database import get_db
from db.models import Agent as AgentModel
from db.schemas import AgentCreate, AgentUpdate, AgentResponse
from core.auth import get_current_user

router = APIRouter()

@router.get("/agents", response_model=List[AgentResponse])
async def get_agents(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = False,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Récupérer la liste des agents"""
    query = db.query(AgentModel)
    
    if active_only:
        query = query.filter(AgentModel.is_active == True)
    
    agents = query.offset(skip).limit(limit).all()
    return agents

@router.get("/agents/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Récupérer un agent par son ID"""
    agent = db.query(AgentModel).filter(AgentModel.id == agent_id).first()
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agent non trouvé")
    
    return agent

@router.post("/agents", response_model=AgentResponse)
async def create_agent(
    agent_data: AgentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Créer un nouvel agent"""
    
    # Vérifier que le nom est unique
    existing_agent = db.query(AgentModel).filter(
        AgentModel.name.ilike(agent_data.name)
    ).first()
    
    if existing_agent:
        raise HTTPException(
            status_code=400, 
            detail="Un agent avec ce nom existe déjà"
        )
    
    # Créer l'agent
    agent = AgentModel(
        id=f"agent-{uuid.uuid4().hex[:8]}",
        name=agent_data.name,
        role=agent_data.role,
        specialty=agent_data.specialty,
        description=agent_data.description,
        prompt=agent_data.prompt,
        model=agent_data.model,
        avatar=agent_data.avatar,
        color=agent_data.color,
        knowledge_base=agent_data.knowledge_base,
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    db.add(agent)
    db.commit()
    db.refresh(agent)
    
    return agent

@router.put("/agents/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: str,
    agent_data: AgentUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Mettre à jour un agent"""
    
    agent = db.query(AgentModel).filter(AgentModel.id == agent_id).first()
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agent non trouvé")
    
    # Vérifier que le nom est unique (si modifié)
    if agent_data.name and agent_data.name != agent.name:
        existing_agent = db.query(AgentModel).filter(
            AgentModel.name.ilike(agent_data.name),
            AgentModel.id != agent_id
        ).first()
        
        if existing_agent:
            raise HTTPException(
                status_code=400, 
                detail="Un agent avec ce nom existe déjà"
            )
    
    # Mettre à jour les champs fournis
    update_data = agent_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(agent, field, value)
    
    agent.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(agent)
    
    return agent

@router.delete("/agents/{agent_id}")
async def delete_agent(
    agent_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Supprimer un agent"""
    
    agent = db.query(AgentModel).filter(AgentModel.id == agent_id).first()
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agent non trouvé")
    
    db.delete(agent)
    db.commit()
    
    return {"message": "Agent supprimé avec succès"}

@router.patch("/agents/{agent_id}/toggle")
async def toggle_agent_status(
    agent_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Activer/Désactiver un agent"""
    
    agent = db.query(AgentModel).filter(AgentModel.id == agent_id).first()
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agent non trouvé")
    
    agent.is_active = not agent.is_active
    agent.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(agent)
    
    return {
        "message": f"Agent {'activé' if agent.is_active else 'désactivé'} avec succès",
        "is_active": agent.is_active
    }

@router.get("/agents/templates")
async def get_agent_templates():
    """Récupérer les templates d'agents disponibles"""
    # Retourner les templates prédéfinis
    templates = [
        {
            "id": "teaching",
            "name": "Professeur/Enseignant",
            "category": "Éducation",
            "description": "Agent spécialisé dans l'enseignement et l'éducation",
            "default_prompt": "Tu es un professeur expérimenté et bienveillant...",
            "default_model": "llama3.2:1b",
            "default_avatar": "👨‍🏫",
            "default_color": "#3b82f6"
        },
        {
            "id": "technical_support",
            "name": "Support Technique",
            "category": "Technique",
            "description": "Agent spécialisé dans le support technique",
            "default_prompt": "Tu es un expert en support technique...",
            "default_model": "llama3.2:1b",
            "default_avatar": "🔧",
            "default_color": "#10b981"
        },
        {
            "id": "administrative",
            "name": "Assistant Administratif",
            "category": "Administration",
            "description": "Agent spécialisé dans les tâches administratives",
            "default_prompt": "Tu es un assistant administratif professionnel...",
            "default_model": "llama3.2:1b",
            "default_avatar": "📋",
            "default_color": "#8b5cf6"
        },
        {
            "id": "customer_service",
            "name": "Service Client",
            "category": "Commercial",
            "description": "Agent spécialisé dans le service client",
            "default_prompt": "Tu es un agent de service client professionnel...",
            "default_model": "llama3.2:1b",
            "default_avatar": "🎧",
            "default_color": "#f59e0b"
        }
    ]
    
    return templates