"""
Gestionnaire d'agents dynamiques
Permet de créer, stocker et utiliser des agents personnalisés
"""

import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime

class AgentManager:
    def __init__(self, agents_file: str = "agents.json"):
        self.agents_file = agents_file
        self.agents = self.load_agents()
    
    def load_agents(self) -> Dict[str, Dict]:
        """Charge les agents depuis le fichier JSON"""
        if os.path.exists(self.agents_file):
            try:
                with open(self.agents_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Erreur lors du chargement des agents: {e}")
                return {}
        return {}
    
    def save_agents(self):
        """Sauvegarde les agents dans le fichier JSON"""
        try:
            with open(self.agents_file, 'w', encoding='utf-8') as f:
                json.dump(self.agents, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des agents: {e}")
    
    def create_agent(self, agent_data: Dict[str, Any]) -> str:
        """Crée un nouvel agent"""
        agent_id = agent_data.get('id', f"agent_{len(self.agents) + 1}")
        
        # Données par défaut
        agent = {
            "id": agent_id,
            "name": agent_data.get('name', 'Agent'),
            "role": agent_data.get('role', 'Assistant'),
            "description": agent_data.get('description', ''),
            "model": agent_data.get('model', 'qwen2.5:7b'),
            "system_prompt": agent_data.get('systemPrompt', 'You are a helpful assistant'),
            "timeout": agent_data.get('timeout', 30000),
            "temperature": agent_data.get('temperature', 0.6),
            "max_tokens": agent_data.get('maxTokens', 400),
            "top_k": agent_data.get('topK', 40),
            "top_p": agent_data.get('topP', 0.9),
            "repetition_penalty": agent_data.get('repetitionPenalty', 1.0),
            "stop_words": agent_data.get('stopWords', "User:\nAssistant:"),
            "tools": agent_data.get('tools', {}),
            "knowledge_packs": agent_data.get('knowledgePacks', {}),
            "created_at": datetime.now().isoformat(),
            "status": "active"
        }
        
        self.agents[agent_id] = agent
        self.save_agents()
        return agent_id
    
    def get_agent(self, agent_id: str) -> Optional[Dict]:
        """Récupère un agent par son ID"""
        return self.agents.get(agent_id)
    
    def get_all_agents(self) -> List[Dict]:
        """Récupère tous les agents"""
        return list(self.agents.values())
    
    def update_agent(self, agent_id: str, updates: Dict[str, Any]) -> bool:
        """Met à jour un agent"""
        if agent_id in self.agents:
            self.agents[agent_id].update(updates)
            self.save_agents()
            return True
        return False
    
    def delete_agent(self, agent_id: str) -> bool:
        """Supprime un agent"""
        if agent_id in self.agents:
            del self.agents[agent_id]
            self.save_agents()
            return True
        return False
    
    def generate_response(self, agent_id: str, message: str, context: str = "") -> str:
        """Génère une réponse pour un agent spécifique"""
        agent = self.get_agent(agent_id)
        if not agent:
            return "Agent non trouvé."
        
        # Construire le prompt système
        system_prompt = agent.get('system_prompt', 'You are a helpful assistant')
        
        # Ajouter le contexte si disponible
        if context:
            system_prompt += f"\n\nContexte: {context}"
        
        # Utiliser Ollama pour générer la réponse
        try:
            from core.llm_loader import ollama_generate
            
            response = ollama_generate(
                prompt=message,
                system_prompt=system_prompt,
                model=agent.get('model', 'qwen2.5:7b'),
                temperature=agent.get('temperature', 0.6),
                max_tokens=agent.get('max_tokens', 400)
            )
            
            return response
        except Exception as e:
            print(f"Erreur lors de la génération de réponse: {e}")
            return "Désolé, je ne peux pas répondre pour le moment."

# Instance globale
agent_manager = AgentManager()
