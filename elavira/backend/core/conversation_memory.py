# Fichier: backend/core/conversation_memory.py

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json
import os

# Stockage en mémoire des conversations (en production, utiliser Redis ou DB)
conversations: Dict[str, List[Dict]] = {}

def get_conversation_context(user_id: str, agent_id: str, max_messages: int = 5) -> str:
    """
    Récupère le contexte de conversation pour un utilisateur et un agent.
    """
    conversation_key = f"{user_id}_{agent_id}"
    
    if conversation_key not in conversations:
        return ""
    
    # Récupérer les derniers messages
    recent_messages = conversations[conversation_key][-max_messages:]
    
    context = ""
    for msg in recent_messages:
        role = "Utilisateur" if msg["role"] == "user" else "Assistant"
        context += f"{role}: {msg['content']}\n"
    
    return context

def add_message(user_id: str, agent_id: str, role: str, content: str):
    """
    Ajoute un message à la conversation.
    """
    conversation_key = f"{user_id}_{agent_id}"
    
    if conversation_key not in conversations:
        conversations[conversation_key] = []
    
    message = {
        "role": role,
        "content": content,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    conversations[conversation_key].append(message)
    
    # Limiter à 20 messages par conversation
    if len(conversations[conversation_key]) > 20:
        conversations[conversation_key] = conversations[conversation_key][-20:]

def clear_conversation(user_id: str, agent_id: str):
    """
    Efface la conversation d'un utilisateur avec un agent.
    """
    conversation_key = f"{user_id}_{agent_id}"
    if conversation_key in conversations:
        del conversations[conversation_key]

def get_conversation_stats() -> Dict:
    """
    Retourne les statistiques des conversations.
    """
    return {
        "total_conversations": len(conversations),
        "total_messages": sum(len(conv) for conv in conversations.values()),
        "active_conversations": list(conversations.keys())
    }