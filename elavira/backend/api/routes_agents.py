# backend/api/routes_agents.py

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Dict, Optional
import requests # Assurez-vous que requests est importé pour les appels API à Ollama
import json # Pour gérer les JSON

# Crée une instance de APIRouter pour les routes des agents
router = APIRouter(
    prefix="/agents",
    tags=["Agents"]
)

# --- Modèle Pydantic pour un Agent ---
class Agent(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    status: str = "active"

# --- Simulation d'une base de données d'agents (en mémoire) ---
fake_agents_db: Dict[str, Agent] = {
    "agent-001": Agent(id="agent-001", name="Elavira Assistant", description="Un assistant généraliste utilisant Ollama."),
    "agent-002": Agent(id="agent-002", name="Fact Checker Bot", description="Vérifie les faits et les sources d'information."),
    "agent-003": Agent(id="agent-003", name="Code Generator", description="Génère des extraits de code dans divers langages.", status="inactive"),
}

# --- Fonction pour appeler un modèle Ollama ---
async def call_ollama_model(prompt: str, model_name: str = "llama2"):
    ollama_url = "http://localhost:11434/api/generate" # URL par défaut d'Ollama
    headers = {"Content-Type": "application/json"}
    data = {
        "model": model_name,
        "prompt": prompt,
        "stream": False # Nous voulons la réponse complète d'un coup
    }
    try:
        response = requests.post(ollama_url, headers=headers, data=json.dumps(data))
        response.raise_for_status() # Lève une exception pour les erreurs HTTP
        result = response.json()
        return result.get("response", "Aucune réponse d'Ollama.")
    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Impossible de se connecter au service Ollama. Assurez-vous qu'il est en cours d'exécution sur http://localhost:11434."
        )
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'appel à Ollama : {e}"
        )

# --- Routes des Agents ---

@router.get("/", response_model=List[Agent])
async def get_all_agents():
    return list(fake_agents_db.values())

@router.get("/{agent_id}", response_model=Agent)
async def get_agent_by_id(agent_id: str):
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
    Interagit avec un agent spécifique, en utilisant Ollama pour l'agent-001.
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

    user_message = message.get("text", "Pas de message fourni.")
    agent_response = ""

    if agent_id == "agent-001":
        # Appel à Ollama pour Elavira Assistant
        try:
            ollama_response = await call_ollama_model(user_message, model_name="llama2") # Utilisez le modèle que vous avez téléchargé
            agent_response = f"Réponse d'Elavira (via Ollama) : {ollama_response}"
        except HTTPException as e:
            raise e # Relève l'erreur si la connexion à Ollama a échoué
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Une erreur inattendue est survenue lors de l'appel à Ollama : {e}"
            )
    elif agent_id == "agent-002":
        agent_response = f"Fact Checker Bot analyse votre requête : '{user_message}'. Réponse simulée."
    else:
        agent_response = f"L'agent {agent.name} a reçu : '{user_message}'. Réponse générique simulée."

    return {"agent_id": agent_id, "agent_name": agent.name, "response": agent_response}