"""
Créateur d'agents - Gestion de la création et configuration des agents
Support pour l'intégration de documents PDFs comme base de connaissances
"""

import os
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import json

# Imports pour le traitement des PDFs
try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    logging.warning("PyPDF2 non disponible - support PDF limité")

try:
    from sentence_transformers import SentenceTransformer
    import chromadb
    EMBEDDING_AVAILABLE = True
except ImportError:
    EMBEDDING_AVAILABLE = False
    logging.warning("SentenceTransformer/ChromaDB non disponible")

logger = logging.getLogger(__name__)

class AgentCreator:
    """
    Créateur d'agents responsable de :
    - Création de nouveaux agents
    - Intégration de documents PDFs
    - Configuration des bases de connaissances
    - Génération de configurations d'agents
    """
    
    def __init__(self):
        self.agents_config_dir = "config/agents"
        self.knowledge_base_dir = "knowledge_bases"
        self.templates_dir = "templates/agents"
        
        # Créer les répertoires si nécessaire
        os.makedirs(self.agents_config_dir, exist_ok=True)
        os.makedirs(self.knowledge_base_dir, exist_ok=True)
        os.makedirs(self.templates_dir, exist_ok=True)
        
        # Modèles de base disponibles
        self.available_models = [
            "qwen2:1.5b",
            "llama3.2:1b", 
            "llama3.2:3b",
            "qwen2.5:7b"
        ]
        
        # Types d'agents prédéfinis
        self.agent_templates = {
            "academic_teacher": {
                "name": "Professeur Académique",
                "description": "Agent spécialisé dans l'enseignement académique",
                "capabilities": ["teaching", "academic_support", "curriculum"],
                "system_prompt": "Tu es un professeur expérimenté. Tu expliques clairement, guides étape par étape et évalues la compréhension.",
                "model": "llama3.2:1b",
                "knowledge_types": ["curriculum", "textbooks", "exercises"]
            },
            "content_specialist": {
                "name": "Spécialiste Contenu",
                "description": "Agent spécialisé dans un domaine de contenu spécifique",
                "capabilities": ["content_expertise", "information_retrieval"],
                "system_prompt": "Tu es un expert dans ton domaine. Tu fournis des informations précises et pertinentes.",
                "model": "qwen2:1.5b",
                "knowledge_types": ["documents", "manuals", "procedures"]
            },
            "customer_support": {
                "name": "Support Client",
                "description": "Agent de support client et assistance",
                "capabilities": ["customer_support", "troubleshooting", "guidance"],
                "system_prompt": "Tu es un agent de support client. Tu es serviable, patient et résous les problèmes efficacement.",
                "model": "qwen2:1.5b",
                "knowledge_types": ["faq", "procedures", "product_info"]
            }
        }
    
    def create_agent_from_pdf(self, 
                            agent_name: str,
                            agent_description: str,
                            pdf_path: str,
                            agent_type: str = "content_specialist",
                            model: str = None) -> Dict[str, Any]:
        """
        Crée un nouvel agent à partir d'un document PDF
        """
        try:
            # Validation des paramètres
            if not os.path.exists(pdf_path):
                raise FileNotFoundError(f"Fichier PDF non trouvé: {pdf_path}")
            
            if agent_type not in self.agent_templates:
                raise ValueError(f"Type d'agent non supporté: {agent_type}")
            
            # Extraction du contenu PDF
            pdf_content = self._extract_pdf_content(pdf_path)
            if not pdf_content:
                raise ValueError("Impossible d'extraire le contenu du PDF")
            
            # Génération de la configuration d'agent
            agent_config = self._generate_agent_config(
                name=agent_name,
                description=agent_description,
                agent_type=agent_type,
                model=model,
                knowledge_content=pdf_content
            )
            
            # Sauvegarde de la configuration
            config_file = self._save_agent_config(agent_config)
            
            # Création de la base de connaissances
            knowledge_base_id = self._create_knowledge_base(
                agent_name=agent_name,
                content=pdf_content
            )
            
            # Mise à jour de la configuration avec l'ID de la base de connaissances
            agent_config["knowledge_base_id"] = knowledge_base_id
            self._save_agent_config(agent_config)
            
            logger.info(f"Agent créé avec succès: {agent_name}")
            
            return {
                "status": "success",
                "agent_id": agent_config["id"],
                "agent_name": agent_name,
                "config_file": config_file,
                "knowledge_base_id": knowledge_base_id,
                "message": f"Agent '{agent_name}' créé avec succès"
            }
            
        except Exception as e:
            logger.error(f"Erreur création agent: {str(e)}")
            return {
                "status": "error",
                "message": f"Erreur lors de la création de l'agent: {str(e)}"
            }
    
    def _extract_pdf_content(self, pdf_path: str) -> str:
        """Extrait le contenu textuel d'un PDF"""
        if not PDF_AVAILABLE:
            logger.warning("PyPDF2 non disponible - extraction PDF impossible")
            return ""
        
        try:
            content = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num, page in enumerate(pdf_reader.pages):
                    page_text = page.extract_text()
                    content += f"\n--- Page {page_num + 1} ---\n"
                    content += page_text
                    content += "\n"
            
            logger.info(f"Contenu PDF extrait: {len(content)} caractères")
            return content
            
        except Exception as e:
            logger.error(f"Erreur extraction PDF: {str(e)}")
            return ""
    
    def _generate_agent_config(self, 
                             name: str,
                             description: str,
                             agent_type: str,
                             model: Optional[str],
                             knowledge_content: str) -> Dict[str, Any]:
        """Génère la configuration d'un agent"""
        
        template = self.agent_templates[agent_type]
        
        # Sélection du modèle
        if not model:
            model = template["model"]
        
        if model not in self.available_models:
            model = self.available_models[0]  # Modèle par défaut
        
        # Génération d'un ID unique
        agent_id = f"agent_{name.lower().replace(' ', '_')}_{int(datetime.utcnow().timestamp())}"
        
        config = {
            "id": agent_id,
            "name": name,
            "description": description,
            "type": agent_type,
            "status": "active",
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "model": model,
            "capabilities": template["capabilities"],
            "system_prompt": template["system_prompt"],
            "knowledge_types": template["knowledge_types"],
            "metadata": {
                "template": agent_type,
                "knowledge_size": len(knowledge_content),
                "creator": "agent_creator"
            }
        }
        
        return config
    
    def _save_agent_config(self, config: Dict[str, Any]) -> str:
        """Sauvegarde la configuration d'un agent"""
        config_file = os.path.join(self.agents_config_dir, f"{config['id']}.json")
        
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        return config_file
    
    def _create_knowledge_base(self, agent_name: str, content: str) -> str:
        """Crée une base de connaissances pour l'agent"""
        if not EMBEDDING_AVAILABLE:
            logger.warning("ChromaDB non disponible - base de connaissances non créée")
            return ""
        
        try:
            # TODO: Implémenter la création de base de connaissances avec ChromaDB
            # Pour l'instant, on sauvegarde juste le contenu
            kb_file = os.path.join(self.knowledge_base_dir, f"{agent_name.lower().replace(' ', '_')}_kb.txt")
            
            with open(kb_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"Base de connaissances créée: {kb_file}")
            return kb_file
            
        except Exception as e:
            logger.error(f"Erreur création base de connaissances: {str(e)}")
            return ""
    
    def list_available_templates(self) -> Dict[str, Any]:
        """Liste les templates d'agents disponibles"""
        return {
            "templates": self.agent_templates,
            "available_models": self.available_models,
            "pdf_support": PDF_AVAILABLE,
            "embedding_support": EMBEDDING_AVAILABLE
        }
    
    def get_agent_config(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Récupère la configuration d'un agent"""
        config_file = os.path.join(self.agents_config_dir, f"{agent_id}.json")
        
        if not os.path.exists(config_file):
            return None
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Erreur lecture config agent: {str(e)}")
            return None
    
    def list_created_agents(self) -> List[Dict[str, Any]]:
        """Liste tous les agents créés"""
        agents = []
        
        for filename in os.listdir(self.agents_config_dir):
            if filename.endswith('.json'):
                agent_id = filename[:-5]  # Enlever .json
                config = self.get_agent_config(agent_id)
                if config:
                    agents.append({
                        "id": config["id"],
                        "name": config["name"],
                        "description": config["description"],
                        "type": config["type"],
                        "status": config["status"],
                        "created_at": config["created_at"]
                    })
        
        return agents

# Instance globale du Créateur d'agents
agent_creator = AgentCreator()
