import React, { useState, useEffect } from 'react';
import { useApp } from '../../context/AppContext';
import { ModernChatInterface } from './ModernChatInterface';
import { Message } from '../../types';
import { chatAPI } from '../../services/api';

const SolenysAgent = {
  id: 'solenys',
  name: 'Solenys',
  description: 'Professeur québécois spécialisé dans l\'enseignement secondaire (PFEQ)',
  avatar: '🤖',
  color: '#f093fb'
};

const SuggestedPrompts = [
  'Aide en mathématiques',
  'Problèmes de physique',
  'Questions de chimie',
  'Français et littérature',
  'Histoire du Québec',
  'Géographie du Canada',
  'Résolution d\'équations',
  'Compréhension de texte',
  'Sciences naturelles',
  'Éducation civique'
];

export const SolenysChat: React.FC = () => {
  const { state, dispatch } = useApp();
  const [messages, setMessages] = useState<Message[]>([]);
  const [conversations, setConversations] = useState<Array<{
    id: string;
    title: string;
    lastMessage: string;
    timestamp: string;
  }>>([]);

  useEffect(() => {
    // Charger les conversations existantes
    loadConversations();
  }, []);

  const loadConversations = async () => {
    // Simuler le chargement des conversations
    setConversations([
      {
        id: 'conv-1',
        title: 'Mathématiques - Algèbre',
        lastMessage: 'Comment résoudre une équation du second degré ?',
        timestamp: '2024-01-15T14:20:00Z'
      },
      {
        id: 'conv-2',
        title: 'Français - Littérature',
        lastMessage: 'Analyse de texte littéraire',
        timestamp: '2024-01-14T09:15:00Z'
      },
      {
        id: 'conv-3',
        title: 'Sciences - Physique',
        lastMessage: 'Mouvement rectiligne uniforme',
        timestamp: '2024-01-13T16:30:00Z'
      }
    ]);
  };

  const handleSendMessage = async (text: string) => {
    if (!text.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString() + '_user_' + Math.random().toString(36).substr(2, 9),
      text: text.trim(),
      user_id: state.logged_in_user || 'Vous',
      timestamp: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);

    try {
      const response = await chatAPI.sendMessage({
        text: text.trim(),
        user_id: state.logged_in_user || 'Guest',
        agent: 'solenys'
      });

      setMessages(prev => [...prev, response]);
    } catch (error) {
      console.error('Erreur lors de l\'envoi du message:', error);
      
      // Message d'erreur simulé
      const errorMessage: Message = {
        id: Date.now().toString() + '_error_' + Math.random().toString(36).substr(2, 9),
        text: 'Désolé, je rencontre un problème technique. Veuillez réessayer.',
        user_id: 'Solenys Assistant',
        timestamp: new Date().toISOString(),
      };
      
      setMessages(prev => [...prev, errorMessage]);
    }
  };

  const handleConversationSelect = (conversationId: string) => {
    // Charger les messages de la conversation sélectionnée
    console.log('Sélection de la conversation:', conversationId);
  };

  const handleNewChat = () => {
    setMessages([]);
    dispatch({ type: 'SET_ACTIVE_CONVERSATION', payload: null });
  };

  return (
    <ModernChatInterface
      agent={SolenysAgent}
      messages={messages}
      onSendMessage={handleSendMessage}
      conversations={conversations}
      activeConversationId={state.active_conversation_id || undefined}
      onConversationSelect={handleConversationSelect}
      onNewChat={handleNewChat}
      suggestedPrompts={SuggestedPrompts}
    />
  );
};
