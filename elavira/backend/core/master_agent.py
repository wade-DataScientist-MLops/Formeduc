"""
Agent Maître - Gestionnaire et dispatching des agents spécialisés
Architecture multi-agents selon le diagramme fourni
"""

from typing import Dict, List, Optional, Any
from enum import Enum
import logging
from datetime import datetime

# Import des agents spécialisés
from .llm_loader import rag_generate as elavira_generate
from .solenys_logic import ask_solenys

logger = logging.getLogger(__name__)

class AgentType(Enum):
    ELAVIRA = "elavira"
    SOLENYS = "solenys"
    MATH = "math"
    FRENCH = "french"
    HR = "hr"

class TaskType(Enum):
    FORMEDUC_CONTENT = "formeduc_content"
    ACADEMIC_TEACHING = "academic_teaching"
    MATH_HELP = "math_help"
    FRENCH_LANGUAGE = "french_language"
    HR_ASSISTANCE = "hr_assistance"
    GENERAL = "general"

class MasterAgent:
    """
    Agent Maître responsable de :
    - Gestion des agents spécialisés
    - Dispatching des tâches
    - Orchestration des réponses
    """
    
    def __init__(self):
        self.agents_registry: Dict[AgentType, Dict[str, Any]] = {
            AgentType.ELAVIRA: {
                "name": "Elavira",
                "description": "Spécialiste Formeduc et secourisme",
                "capabilities": ["formeduc_content", "first_aid", "pedagogy"],
                "status": "active",
                "model": "qwen2:1.5b",
                "knowledge_base": "formeduc_website"
            },
            AgentType.SOLENYS: {
                "name": "Solenys", 
                "description": "Professeur académique PFEQ Québec",
                "capabilities": ["academic_teaching", "math", "science", "french"],
                "status": "active",
                "model": "llama3.2:1b",
                "knowledge_base": "pfeq_curriculum"
            }
        }
        
        self.task_routing: Dict[TaskType, List[AgentType]] = {
            TaskType.FORMEDUC_CONTENT: [AgentType.ELAVIRA],
            TaskType.ACADEMIC_TEACHING: [AgentType.SOLENYS],
            TaskType.MATH_HELP: [AgentType.SOLENYS],
            TaskType.FRENCH_LANGUAGE: [AgentType.SOLENYS],
            TaskType.HR_ASSISTANCE: [],  # Pas encore implémenté
            TaskType.GENERAL: [AgentType.ELAVIRA, AgentType.SOLENYS]
        }
        
        self.conversation_history: Dict[str, List[Dict]] = {}
        
    def analyze_request(self, user_message: str, user_id: str = "default") -> TaskType:
        """
        Analyse la requête utilisateur pour déterminer le type de tâche
        """
        message_lower = user_message.lower()
        
        # Mots-clés pour le routing
        formeduc_keywords = ["formation", "secourisme", "rsge", "formeduc", "cours", "tarif", "prix"]
        academic_keywords = ["math", "mathématiques", "science", "français", "pfeq", "école", "élève", "devoir"]
        math_keywords = ["calcul", "équation", "problème", "exercice", "addition", "soustraction", "multiplication"]
        french_keywords = ["grammaire", "orthographe", "conjugaison", "rédaction", "texte"]
        
        if any(keyword in message_lower for keyword in formeduc_keywords):
            return TaskType.FORMEDUC_CONTENT
        elif any(keyword in message_lower for keyword in math_keywords):
            return TaskType.MATH_HELP
        elif any(keyword in message_lower for keyword in french_keywords):
            return TaskType.FRENCH_LANGUAGE
        elif any(keyword in message_lower for keyword in academic_keywords):
            return TaskType.ACADEMIC_TEACHING
        else:
            return TaskType.GENERAL
    
    def dispatch_task(self, user_message: str, user_id: str = "default", agent_preference: Optional[str] = None) -> Dict[str, Any]:
        """
        Dispatch la tâche vers l'agent approprié
        """
        try:
            # Si un agent est spécifiquement demandé
            if agent_preference:
                if agent_preference == "elavira":
                    return self._handle_elavira_request(user_message, user_id)
                elif agent_preference == "solenys":
                    return self._handle_solenys_request(user_message, user_id)
            
            # Analyse automatique de la requête
            task_type = self.analyze_request(user_message, user_id)
            available_agents = self.task_routing.get(task_type, [AgentType.ELAVIRA])
            
            if not available_agents:
                return self._handle_fallback(user_message, user_id)
            
            # Sélection de l'agent (pour l'instant, on prend le premier)
            selected_agent = available_agents[0]
            
            if selected_agent == AgentType.ELAVIRA:
                return self._handle_elavira_request(user_message, user_id)
            elif selected_agent == AgentType.SOLENYS:
                return self._handle_solenys_request(user_message, user_id)
            else:
                return self._handle_fallback(user_message, user_id)
                
        except Exception as e:
            logger.error(f"Erreur dans le dispatching: {str(e)}")
            return self._handle_error_response(str(e))
    
    def _handle_elavira_request(self, user_message: str, user_id: str) -> Dict[str, Any]:
        """Traite une requête pour Elavira"""
        try:
            response = elavira_generate(
                query=user_message,
                system_persona="Tu es Elavira, spécialiste Formeduc. Réponds de manière professionnelle et serviable.",
                user_id=user_id,
                agent_id="elavira"
            )
            
            return {
                "agent": "Elavira",
                "agent_type": AgentType.ELAVIRA.value,
                "response": response,
                "status": "success",
                "timestamp": datetime.utcnow().isoformat(),
                "metadata": {
                    "model": "qwen2:1.5b",
                    "knowledge_base": "formeduc_website"
                }
            }
        except Exception as e:
            logger.error(f"Erreur Elavira: {str(e)}")
            return self._handle_error_response(str(e))
    
    def _handle_solenys_request(self, user_message: str, user_id: str) -> Dict[str, Any]:
        """Traite une requête pour Solenys"""
        try:
            response = ask_solenys(question=user_message, user_id=user_id)
            
            return {
                "agent": "Solenys",
                "agent_type": AgentType.SOLENYS.value,
                "response": response.get("response", "Désolé, je ne peux pas répondre pour le moment."),
                "status": "success",
                "timestamp": datetime.utcnow().isoformat(),
                "metadata": {
                    "model": "llama3.2:1b",
                    "knowledge_base": "pfeq_curriculum"
                }
            }
        except Exception as e:
            logger.error(f"Erreur Solenys: {str(e)}")
            return self._handle_error_response(str(e))
    
    def _handle_fallback(self, user_message: str, user_id: str) -> Dict[str, Any]:
        """Réponse de fallback quand aucun agent spécialisé n'est disponible"""
        return {
            "agent": "Master Agent",
            "agent_type": "master",
            "response": "Je vais rediriger votre demande vers l'agent le plus approprié. Pouvez-vous préciser votre besoin ?",
            "status": "fallback",
            "timestamp": datetime.utcnow().isoformat(),
            "metadata": {
                "suggestion": "Essayez de mentionner 'formation', 'math', 'français' ou 'secourisme'"
            }
        }
    
    def _handle_error_response(self, error_message: str) -> Dict[str, Any]:
        """Gestion des erreurs"""
        return {
            "agent": "System",
            "agent_type": "error",
            "response": "Une erreur est survenue. Veuillez réessayer.",
            "status": "error",
            "timestamp": datetime.utcnow().isoformat(),
            "metadata": {
                "error": error_message
            }
        }
    
    def get_agents_status(self) -> Dict[str, Any]:
        """Retourne le statut de tous les agents"""
        return {
            "total_agents": len(self.agents_registry),
            "active_agents": len([a for a in self.agents_registry.values() if a["status"] == "active"]),
            "agents": {
                agent_type.value: {
                    "name": agent_info["name"],
                    "description": agent_info["description"],
                    "status": agent_info["status"],
                    "capabilities": agent_info["capabilities"]
                }
                for agent_type, agent_info in self.agents_registry.items()
            }
        }
    
    def register_new_agent(self, agent_type: str, agent_config: Dict[str, Any]) -> bool:
        """Enregistre un nouvel agent (pour l'Agent Creator)"""
        try:
            # TODO: Implémenter l'enregistrement de nouveaux agents
            logger.info(f"Nouvel agent enregistré: {agent_type}")
            return True
        except Exception as e:
            logger.error(f"Erreur enregistrement agent: {str(e)}")
            return False

# Instance globale de l'Agent Maître
master_agent = MasterAgent()
