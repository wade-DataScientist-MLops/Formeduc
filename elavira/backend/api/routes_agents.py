from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json
import uuid
from datetime import datetime
import os

router = APIRouter(prefix="/api/agents", tags=["Agents"])

# Modèles de données
class AgentConfig(BaseModel):
    name: str
    role: str
    description: str
    model: str
    timeout: int = 30000
    temperature: float = 0.6
    maxTokens: int = 400
    topK: int = 40
    topP: float = 0.9
    repetitionPenalty: float = 1.0
    stopWords: str = "User:\nÉlève:\nAssistant:"
    systemPrompt: str
    tools: Dict[str, bool]
    knowledgePacks: Dict[str, bool]

class AgentResponse(BaseModel):
    id: str
    name: str
    role: str
    description: str
    model: str
    status: str
    createdAt: str
    config: Dict[str, Any]

# Stockage des agents (en production, utiliser une base de données)
agents_db = {}

@router.post("/create", response_model=AgentResponse)
async def create_agent(agent_config: AgentConfig):
    """Créer un nouvel agent avec configuration complète"""
    try:
        # Générer un ID unique
        agent_id = str(uuid.uuid4())
        
        # Créer la configuration de l'agent
        agent_data = {
            "id": agent_id,
            "name": agent_config.name,
            "role": agent_config.role,
            "description": agent_config.description,
            "model": agent_config.model,
            "status": "Active",
            "createdAt": datetime.now().isoformat(),
            "config": {
                "timeout": agent_config.timeout,
                "temperature": agent_config.temperature,
                "maxTokens": agent_config.maxTokens,
                "topK": agent_config.topK,
                "topP": agent_config.topP,
                "repetitionPenalty": agent_config.repetitionPenalty,
                "stopWords": agent_config.stopWords,
                "systemPrompt": agent_config.systemPrompt,
                "tools": agent_config.tools,
                "knowledgePacks": agent_config.knowledgePacks
            }
        }
        
        # Sauvegarder l'agent
        agents_db[agent_id] = agent_data
        
        # Créer le fichier de configuration de l'agent
        await save_agent_config(agent_id, agent_data)
        
        # Initialiser les outils de l'agent
        await initialize_agent_tools(agent_id, agent_config)
        
        return AgentResponse(**agent_data)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la création de l'agent: {str(e)}")

@router.get("/", response_model=List[AgentResponse])
async def list_agents():
    """Lister tous les agents créés"""
    return list(agents_db.values())

@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: str):
    """Récupérer un agent spécifique"""
    if agent_id not in agents_db:
        raise HTTPException(status_code=404, detail="Agent non trouvé")
    
    return agents_db[agent_id]

@router.put("/{agent_id}", response_model=AgentResponse)
async def update_agent(agent_id: str, agent_config: AgentConfig):
    """Mettre à jour un agent existant"""
    if agent_id not in agents_db:
        raise HTTPException(status_code=404, detail="Agent non trouvé")
    
    try:
        # Mettre à jour les données
        agents_db[agent_id].update({
            "name": agent_config.name,
            "role": agent_config.role,
            "description": agent_config.description,
            "model": agent_config.model,
            "config": {
                "timeout": agent_config.timeout,
                "temperature": agent_config.temperature,
                "maxTokens": agent_config.maxTokens,
                "topK": agent_config.topK,
                "topP": agent_config.topP,
                "repetitionPenalty": agent_config.repetitionPenalty,
                "stopWords": agent_config.stopWords,
                "systemPrompt": agent_config.systemPrompt,
                "tools": agent_config.tools,
                "knowledgePacks": agent_config.knowledgePacks
            }
        })
        
        # Sauvegarder la configuration mise à jour
        await save_agent_config(agent_id, agents_db[agent_id])
        
        return agents_db[agent_id]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la mise à jour: {str(e)}")

@router.delete("/{agent_id}")
async def delete_agent(agent_id: str):
    """Supprimer un agent"""
    if agent_id not in agents_db:
        raise HTTPException(status_code=404, detail="Agent non trouvé")
    
    try:
        # Supprimer l'agent de la base de données
        del agents_db[agent_id]
        
        # Supprimer les fichiers de configuration
        await delete_agent_config(agent_id)
        
        return {"message": "Agent supprimé avec succès"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la suppression: {str(e)}")

@router.post("/{agent_id}/upload")
async def upload_document(agent_id: str, file: UploadFile = File(...)):
    """Télécharger un document pour l'indexation RAG d'un agent"""
    if agent_id not in agents_db:
        raise HTTPException(status_code=404, detail="Agent non trouvé")
    
    try:
        # Créer le dossier de l'agent s'il n'existe pas
        agent_dir = f"agents/{agent_id}/documents"
        os.makedirs(agent_dir, exist_ok=True)
        
        # Sauvegarder le fichier
        file_path = os.path.join(agent_dir, file.filename)
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Indexer le document pour le RAG
        await index_document_for_agent(agent_id, file_path)
        
        return {"message": f"Document {file.filename} téléchargé et indexé avec succès"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du téléchargement: {str(e)}")

@router.post("/{agent_id}/chat")
async def chat_with_agent(agent_id: str, message: str, user_id: str = "default"):
    """Chatter avec un agent spécifique"""
    if agent_id not in agents_db:
        raise HTTPException(status_code=404, detail="Agent non trouvé")
    
    try:
        agent_data = agents_db[agent_id]
        
        # Utiliser la logique de génération appropriée selon la configuration
        response = await generate_agent_response(agent_data, message, user_id)
        
        return {
            "id": str(uuid.uuid4()),
            "text": response,
            "user_id": f"{agent_data['name']} Assistant",
            "timestamp": datetime.now().isoformat(),
            "agent_id": agent_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération: {str(e)}")

# Fonctions utilitaires
async def save_agent_config(agent_id: str, agent_data: dict):
    """Sauvegarder la configuration d'un agent dans un fichier"""
    config_dir = f"agents/{agent_id}"
    os.makedirs(config_dir, exist_ok=True)
    
    config_path = os.path.join(config_dir, "config.json")
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(agent_data, f, indent=2, ensure_ascii=False)

async def delete_agent_config(agent_id: str):
    """Supprimer les fichiers de configuration d'un agent"""
    import shutil
    agent_dir = f"agents/{agent_id}"
    if os.path.exists(agent_dir):
        shutil.rmtree(agent_dir)

async def initialize_agent_tools(agent_id: str, agent_config: AgentConfig):
    """Initialiser les outils d'un agent selon sa configuration"""
    # Créer le dossier des outils
    tools_dir = f"agents/{agent_id}/tools"
    os.makedirs(tools_dir, exist_ok=True)
    
    # Créer les fichiers de configuration pour chaque outil activé
    for tool, enabled in agent_config.tools.items():
        if enabled:
            tool_config = {
                "name": tool,
                "enabled": True,
                "config": {}
            }
            
            tool_path = os.path.join(tools_dir, f"{tool}.json")
            with open(tool_path, "w", encoding="utf-8") as f:
                json.dump(tool_config, f, indent=2)

async def index_document_for_agent(agent_id: str, file_path: str):
    """Indexer un document pour le RAG d'un agent"""
    try:
        from core.chroma_client import collection, embedder
        
        # Lire le contenu du fichier
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Créer l'embedding
        embedding = embedder.encode(content)
        
        # Ajouter au ChromaDB avec l'ID de l'agent
        collection.add(
            documents=[content],
            embeddings=[embedding.tolist()],
            metadatas=[{
                "agent_id": agent_id,
                "filename": os.path.basename(file_path),
                "timestamp": datetime.now().isoformat()
            }],
            ids=[f"{agent_id}_{os.path.basename(file_path)}_{uuid.uuid4()}"]
        )
        
    except Exception as e:
        print(f"Erreur lors de l'indexation: {e}")

async def generate_agent_response(agent_data: dict, message: str, user_id: str):
    """Générer une réponse avec un agent configuré"""
    try:
        from core.llm_loader import ollama_generate
        
        # Construire le prompt avec la configuration de l'agent
        system_prompt = agent_data["config"]["systemPrompt"]
        
        full_prompt = f"""
{system_prompt}

Question de l'utilisateur: {message}

Réponse:
"""
        
        # Générer la réponse avec Ollama
        response = ollama_generate(full_prompt, model=agent_data["model"])
        
        return response
        
    except Exception as e:
        return f"Désolé, je rencontre des difficultés techniques: {str(e)}"