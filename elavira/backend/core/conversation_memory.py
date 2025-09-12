#!/usr/bin/env python3
"""
Système de mémoire des conversations pour les assistants
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class ConversationMemory:
    def __init__(self, memory_file: str = "/app/conversation_memory.json"):
        self.memory_file = memory_file
        self.memories = self._load_memories()
    
    def _load_memories(self) -> Dict:
        """Charge les mémoires depuis le fichier"""
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Erreur lors du chargement de la mémoire: {e}")
        return {}
    
    def _save_memories(self):
        """Sauvegarde les mémoires dans le fichier"""
        try:
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.memories, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde de la mémoire: {e}")
    
    def add_message(self, user_id: str, agent_id: str, message: str, response: str):
        """Ajoute un message à la mémoire de conversation"""
        conversation_key = f"{user_id}_{agent_id}"
        
        if conversation_key not in self.memories:
            self.memories[conversation_key] = {
                "user_id": user_id,
                "agent_id": agent_id,
                "messages": [],
                "last_updated": datetime.now().isoformat()
            }
        
        self.memories[conversation_key]["messages"].append({
            "timestamp": datetime.now().isoformat(),
            "user_message": message,
            "assistant_response": response
        })
        
        # Garder seulement les 10 derniers messages
        if len(self.memories[conversation_key]["messages"]) > 10:
            self.memories[conversation_key]["messages"] = self.memories[conversation_key]["messages"][-10:]
        
        self.memories[conversation_key]["last_updated"] = datetime.now().isoformat()
        self._save_memories()
    
    def get_conversation_context(self, user_id: str, agent_id: str, max_messages: int = 3) -> str:
        """Récupère le contexte de conversation récent"""
        conversation_key = f"{user_id}_{agent_id}"
        
        if conversation_key not in self.memories:
            return ""
        
        messages = self.memories[conversation_key]["messages"]
        recent_messages = messages[-max_messages:] if len(messages) > max_messages else messages
        
        context_parts = []
        for msg in recent_messages:
            context_parts.append(f"Utilisateur: {msg['user_message']}")
            context_parts.append(f"Assistant: {msg['assistant_response']}")
        
        return "\n".join(context_parts)
    
    def clear_old_conversations(self, days: int = 7):
        """Supprime les conversations anciennes"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        for key in list(self.memories.keys()):
            try:
                last_updated = datetime.fromisoformat(self.memories[key]["last_updated"])
                if last_updated < cutoff_date:
                    del self.memories[key]
            except:
                # Si erreur de parsing, supprimer la conversation
                del self.memories[key]
        
        self._save_memories()

# Instance globale
conversation_memory = ConversationMemory()

def add_to_memory(user_id: str, agent_id: str, message: str, response: str):
    """Fonction utilitaire pour ajouter à la mémoire"""
    conversation_memory.add_message(user_id, agent_id, message, response)

def get_conversation_context(user_id: str, agent_id: str, max_messages: int = 3) -> str:
    """Fonction utilitaire pour récupérer le contexte"""
    return conversation_memory.get_conversation_context(user_id, agent_id, max_messages)
