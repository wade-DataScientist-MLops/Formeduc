"""
Routes pour la gestion des agents
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
from core.agent_manager import agent_manager

router = APIRouter(prefix="/api/agents", tags=["Agents"])

class AgentCreate(BaseModel):
    name: str
    role: str
    description: str
    model: str = "qwen2.5:7b"
    systemPrompt: str = "You are a helpful assistant"
    timeout: int = 30000
    temperature: float = 0.6
    maxTokens: int = 400
    topK: int = 40
    topP: float = 0.9
    repetitionPenalty: float = 1.0
    stopWords: str = "User:\nAssistant:"
    tools: Dict[str, Any] = {}
    knowledgePacks: Dict[str, Any] = {}

class AgentResponse(BaseModel):
    id: str
    name: str
    role: str
    description: str
    model: str
    status: str
    created_at: str

@router.post("/create", response_model=AgentResponse)
async def create_agent(agent_data: AgentCreate):
    """Crée un nouvel agent"""
    try:
        # Convertir en dictionnaire
        agent_dict = agent_data.dict()
        
        # Générer un ID unique
        agent_id = f"agent_{len(agent_manager.agents) + 1}_{agent_data.name.lower().replace(' ', '_')}"
        agent_dict['id'] = agent_id
        
        # Créer l'agent
        created_id = agent_manager.create_agent(agent_dict)
        
        # Récupérer l'agent créé
        agent = agent_manager.get_agent(created_id)
        
        if not agent:
            raise HTTPException(status_code=500, detail="Erreur lors de la création de l'agent")
        
        return AgentResponse(
            id=agent['id'],
            name=agent['name'],
            role=agent['role'],
            description=agent['description'],
            model=agent['model'],
            status=agent['status'],
            created_at=agent['created_at']
        )
        
    except Exception as e:
        print(f"Erreur lors de la création de l'agent: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la création de l'agent: {str(e)}")

@router.get("/", response_model=List[AgentResponse])
async def get_all_agents():
    """Récupère tous les agents"""
    try:
        agents = agent_manager.get_all_agents()
        return [
            AgentResponse(
                id=agent['id'],
                name=agent['name'],
                role=agent['role'],
                description=agent['description'],
                model=agent['model'],
                status=agent['status'],
                created_at=agent['created_at']
            )
            for agent in agents
        ]
    except Exception as e:
        print(f"Erreur lors de la récupération des agents: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des agents: {str(e)}")

@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: str):
    """Récupère un agent par son ID"""
    try:
        agent = agent_manager.get_agent(agent_id)
        if not agent:
            raise HTTPException(status_code=404, detail="Agent non trouvé")
        
        return AgentResponse(
            id=agent['id'],
            name=agent['name'],
            role=agent['role'],
            description=agent['description'],
            model=agent['model'],
            status=agent['status'],
            created_at=agent['created_at']
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erreur lors de la récupération de l'agent: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération de l'agent: {str(e)}")

@router.delete("/{agent_id}")
async def delete_agent(agent_id: str):
    """Supprime un agent"""
    try:
        success = agent_manager.delete_agent(agent_id)
        if not success:
            raise HTTPException(status_code=404, detail="Agent non trouvé")
        
        return {"message": "Agent supprimé avec succès"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erreur lors de la suppression de l'agent: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la suppression de l'agent: {str(e)}")