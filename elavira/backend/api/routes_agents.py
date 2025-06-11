# backend/api/routes_agents.py

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Dict, Optional

# Crée une instance de APIRouter pour les routes des agents
router = APIRouter(
    prefix="/agents", # Toutes les routes ici commenceront par /agents
    tags=["Agents"]   # Pour l'organisation dans la documentation Swagger/OpenAPI
)

# --- Modèle Pydantic pour un Agent ---
class Agent(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    status: str = "active" # ex: active, inactive, busy

# --- Simulation d'une base de données d'agents (en mémoire) ---
# Cette approche n'est PAS persistante et sera effacée à chaque redémarrage du serveur.
fake_agents_db: Dict[str, Agent] = {
    "agent-001": Agent(id="agent-001", name="Elavira Assistant", description="Un assistant généraliste pour les requêtes courantes."),
    "agent-002": Agent(id="agent-002", name="Fact Checker Bot", description="Vérifie les faits et les sources d'information."),
    "agent-003": Agent(id="agent-003", name="Code Generator", description="Génère des extraits de code dans divers langages.", status="inactive"),
}

# --- Routes des Agents ---

@router.get("/", response_model=List[Agent])
async def get_all_agents():
    """
    Retourne la liste de tous les agents disponibles.
    """
    return list(fake_agents_db.values())

@router.get("/{agent_id}", response_model=Agent)
async def get_agent_by_id(agent_id: str):
    """
    Retourne les détails d'un agent spécifique par son ID.
    """
    agent = fake_agents_db.get(agent_id)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent avec l'ID '{agent_id}' introuvable."
        )
    return agent

@router.post("/interact/{agent_id}")
async def interact_with_agent(agent_id: str, message: Dict[str, str]):
    """
    Simule une interaction avec un agent spécifique.
    """
    agent = fake_agents_db.get(agent_id)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent avec l'ID '{agent_id}' introuvable."
        )
    if agent.status == "inactive":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"L'agent '{agent.name}' est inactif et ne peut pas interagir."
        )

    # Logique d'interaction simulée
    user_message = message.get("text", "Pas de message fourni.")
    if agent_id == "agent-001":
        response_text = f"Elavira Assistant a reçu votre message : '{user_message}'. Comment puis-je vous aider davantage ?"
    elif agent_id == "agent-002":
        response_text = f"Fact Checker Bot analyse votre requête : '{user_message}'. Veuillez patienter."
    else:
        response_text = f"L'agent {agent.name} a reçu : '{user_message}'. Réponse générique."

    return {"agent_id": agent_id, "agent_name": agent.name, "response": response_text}

# Vous pouvez ajouter d'autres routes ici (ex: créer un agent, mettre à jour un agent, etc.)