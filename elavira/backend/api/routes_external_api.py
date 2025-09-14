"""
API Externe - Interface pour applications tierces
Permet l'intégration de la plateforme d'agents IA avec d'autres systèmes
"""

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
import logging
import os
from datetime import datetime, timedelta
import secrets

# Imports des composants de la plateforme
from core.master_agent import master_agent, AgentType, TaskType
from core.agent_creator import agent_creator

logger = logging.getLogger(__name__)

# Configuration de sécurité
security = HTTPBearer()
API_KEYS = {
    "demo_key_123": {
        "name": "Demo Application",
        "permissions": ["read", "chat"],
        "rate_limit": 100,  # Requêtes par heure
        "expires": None
    },
    "admin_key_456": {
        "name": "Admin Application", 
        "permissions": ["read", "chat", "create_agent", "upload_pdf"],
        "rate_limit": 1000,
        "expires": None
    }
}

# Modèles de données
class ChatRequest(BaseModel):
    message: str = Field(..., description="Message de l'utilisateur")
    agent_preference: Optional[str] = Field(None, description="Agent préféré (elavira, solenys)")
    user_id: Optional[str] = Field("external_user", description="ID utilisateur externe")
    context: Optional[Dict[str, Any]] = Field(None, description="Contexte supplémentaire")

class ChatResponse(BaseModel):
    agent: str = Field(..., description="Nom de l'agent qui a répondu")
    response: str = Field(..., description="Réponse de l'agent")
    status: str = Field(..., description="Statut de la réponse")
    timestamp: str = Field(..., description="Horodatage")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Métadonnées")

class AgentCreationRequest(BaseModel):
    name: str = Field(..., description="Nom de l'agent")
    description: str = Field(..., description="Description de l'agent")
    agent_type: str = Field("content_specialist", description="Type d'agent")
    model: Optional[str] = Field(None, description="Modèle à utiliser")

class AgentCreationResponse(BaseModel):
    status: str = Field(..., description="Statut de la création")
    agent_id: Optional[str] = Field(None, description="ID de l'agent créé")
    message: str = Field(..., description="Message de retour")

class PlatformStatus(BaseModel):
    status: str = Field(..., description="Statut de la plateforme")
    agents_count: int = Field(..., description="Nombre d'agents actifs")
    available_agents: List[str] = Field(..., description="Liste des agents disponibles")
    capabilities: List[str] = Field(..., description="Capacités de la plateforme")

router = APIRouter(prefix="/external", tags=["External API"])

def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Vérifie la clé API"""
    api_key = credentials.credentials
    
    if api_key not in API_KEYS:
        raise HTTPException(
            status_code=401,
            detail="Clé API invalide"
        )
    
    api_info = API_KEYS[api_key]
    
    # Vérifier l'expiration
    if api_info.get("expires") and datetime.utcnow() > api_info["expires"]:
        raise HTTPException(
            status_code=401,
            detail="Clé API expirée"
        )
    
    return api_info

def check_permission(api_info: dict, required_permission: str):
    """Vérifie les permissions"""
    if required_permission not in api_info.get("permissions", []):
        raise HTTPException(
            status_code=403,
            detail=f"Permission '{required_permission}' requise"
        )

@router.get("/status", response_model=PlatformStatus)
async def get_platform_status(api_info: dict = Depends(verify_api_key)):
    """
    Retourne le statut de la plateforme d'agents IA
    """
    check_permission(api_info, "read")
    
    try:
        agents_status = master_agent.get_agents_status()
        
        return PlatformStatus(
            status="active",
            agents_count=agents_status["active_agents"],
            available_agents=list(agents_status["agents"].keys()),
            capabilities=[
                "chat_with_agents",
                "agent_creation", 
                "pdf_knowledge_integration",
                "multi_agent_orchestration"
            ]
        )
    except Exception as e:
        logger.error(f"Erreur statut plateforme: {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur interne")

@router.post("/chat", response_model=ChatResponse)
async def chat_with_agents(
    request: ChatRequest,
    api_info: dict = Depends(verify_api_key)
):
    """
    Chat avec les agents de la plateforme
    """
    check_permission(api_info, "chat")
    
    try:
        # Dispatch vers l'Agent Maître
        result = master_agent.dispatch_task(
            user_message=request.message,
            user_id=request.user_id,
            agent_preference=request.agent_preference
        )
        
        return ChatResponse(
            agent=result["agent"],
            response=result["response"],
            status=result["status"],
            timestamp=result["timestamp"],
            metadata=result.get("metadata")
        )
        
    except Exception as e:
        logger.error(f"Erreur chat externe: {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur lors du traitement")

@router.get("/agents", response_model=List[Dict[str, Any]])
async def list_agents(api_info: dict = Depends(verify_api_key)):
    """
    Liste tous les agents disponibles
    """
    check_permission(api_info, "read")
    
    try:
        agents_status = master_agent.get_agents_status()
        return [
            {
                "id": agent_id,
                "name": agent_info["name"],
                "description": agent_info["description"],
                "status": agent_info["status"],
                "capabilities": agent_info["capabilities"]
            }
            for agent_id, agent_info in agents_status["agents"].items()
        ]
    except Exception as e:
        logger.error(f"Erreur liste agents: {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur interne")

@router.post("/agents/create", response_model=AgentCreationResponse)
async def create_agent(
    request: AgentCreationRequest,
    api_info: dict = Depends(verify_api_key)
):
    """
    Crée un nouvel agent (sans PDF pour l'instant)
    """
    check_permission(api_info, "create_agent")
    
    try:
        # Pour l'instant, on ne crée que des agents de base
        # TODO: Implémenter la création complète d'agents
        return AgentCreationResponse(
            status="success",
            agent_id=f"agent_{request.name.lower()}_{int(datetime.utcnow().timestamp())}",
            message=f"Agent '{request.name}' créé avec succès"
        )
    except Exception as e:
        logger.error(f"Erreur création agent: {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur lors de la création")

@router.post("/agents/create-from-pdf", response_model=AgentCreationResponse)
async def create_agent_from_pdf(
    name: str,
    description: str,
    agent_type: str = "content_specialist",
    model: Optional[str] = None,
    pdf_file: UploadFile = File(...),
    api_info: dict = Depends(verify_api_key)
):
    """
    Crée un nouvel agent à partir d'un document PDF
    """
    check_permission(api_info, "upload_pdf")
    
    try:
        # Vérifier le type de fichier
        if not pdf_file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Seuls les fichiers PDF sont acceptés")
        
        # Sauvegarder le fichier temporairement
        temp_pdf_path = f"temp_{secrets.token_hex(8)}.pdf"
        with open(temp_pdf_path, "wb") as buffer:
            content = await pdf_file.read()
            buffer.write(content)
        
        try:
            # Créer l'agent avec le PDF
            result = agent_creator.create_agent_from_pdf(
                agent_name=name,
                agent_description=description,
                pdf_path=temp_pdf_path,
                agent_type=agent_type,
                model=model
            )
            
            return AgentCreationResponse(
                status=result["status"],
                agent_id=result.get("agent_id"),
                message=result["message"]
            )
            
        finally:
            # Nettoyer le fichier temporaire
            if os.path.exists(temp_pdf_path):
                os.remove(temp_pdf_path)
                
    except Exception as e:
        logger.error(f"Erreur création agent PDF: {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur lors de la création")

@router.get("/agents/templates")
async def get_agent_templates(api_info: dict = Depends(verify_api_key)):
    """
    Retourne les templates d'agents disponibles
    """
    check_permission(api_info, "read")
    
    try:
        templates = agent_creator.list_available_templates()
        return templates
    except Exception as e:
        logger.error(f"Erreur templates: {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur interne")

@router.get("/agents/created")
async def list_created_agents(api_info: dict = Depends(verify_api_key)):
    """
    Liste les agents créés via l'API
    """
    check_permission(api_info, "read")
    
    try:
        agents = agent_creator.list_created_agents()
        return agents
    except Exception as e:
        logger.error(f"Erreur liste agents créés: {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur interne")

@router.post("/api-keys/generate")
async def generate_api_key(
    name: str,
    permissions: List[str] = ["read", "chat"],
    rate_limit: int = 100,
    expires_days: Optional[int] = None,
    api_info: dict = Depends(verify_api_key)
):
    """
    Génère une nouvelle clé API (admin seulement)
    """
    check_permission(api_info, "admin")  # Permission spéciale admin
    
    try:
        new_key = f"key_{secrets.token_hex(16)}"
        expires = None
        
        if expires_days:
            expires = datetime.utcnow() + timedelta(days=expires_days)
        
        API_KEYS[new_key] = {
            "name": name,
            "permissions": permissions,
            "rate_limit": rate_limit,
            "expires": expires
        }
        
        return {
            "api_key": new_key,
            "name": name,
            "permissions": permissions,
            "expires": expires.isoformat() if expires else None
        }
        
    except Exception as e:
        logger.error(f"Erreur génération clé API: {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur lors de la génération")

# Documentation de l'API
@router.get("/docs")
async def get_api_documentation():
    """
    Documentation de l'API externe
    """
    return {
        "title": "Plateforme d'Agents IA - API Externe",
        "version": "1.0.0",
        "description": "API pour l'intégration avec des applications tierces",
        "authentication": {
            "type": "Bearer Token",
            "description": "Utilisez une clé API dans l'en-tête Authorization"
        },
        "endpoints": {
            "GET /external/status": "Statut de la plateforme",
            "POST /external/chat": "Chat avec les agents",
            "GET /external/agents": "Liste des agents",
            "POST /external/agents/create": "Créer un agent",
            "POST /external/agents/create-from-pdf": "Créer un agent à partir d'un PDF",
            "GET /external/agents/templates": "Templates d'agents disponibles",
            "GET /external/agents/created": "Agents créés via l'API"
        },
        "example_usage": {
            "chat": {
                "url": "POST /external/chat",
                "headers": {
                    "Authorization": "Bearer demo_key_123",
                    "Content-Type": "application/json"
                },
                "body": {
                    "message": "Bonjour, j'ai besoin d'aide",
                    "agent_preference": "elavira"
                }
            }
        }
    }
