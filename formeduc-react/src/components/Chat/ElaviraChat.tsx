import React, { useState, useEffect } from 'react';
import { useApp } from '../../context/AppContext';
import { ModernChatInterface } from './ModernChatInterface';
import { Message } from '../../types';
import { chatAPI } from '../../services/api';

const ElaviraAgent = {
  id: 'elavira',
  name: 'Elavira',
  description: 'Votre éducatrice spécialisée en secourisme et formations Formeduc',
  avatar: '👩‍🏫',
  color: '#88c0d0'
};

const SuggestedPrompts = [
  'Comment effectuer un massage cardiaque ?',
  'Quelles sont les étapes du secourisme ?',
  'Comment utiliser un défibrillateur ?',
  'Formation PSC1 - que dois-je savoir ?',
  'Gestes de premiers secours pour enfants',
  'Comment gérer une situation d\'urgence ?'
];

export const ElaviraChat: React.FC = () => {
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
        title: 'Formation secourisme',
        lastMessage: 'Comment effectuer un massage cardiaque ?',
        timestamp: '2024-01-15T10:30:00Z'
      },
      {
        id: 'conv-2',
        title: 'Questions PSC1',
        lastMessage: 'Quelles sont les étapes du PSC1 ?',
        timestamp: '2024-01-14T15:45:00Z'
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
        agent: 'elavira'
      });

      setMessages(prev => [...prev, response]);
    } catch (error) {
      console.error('Erreur lors de l\'envoi du message:', error);
      
      // Message d'erreur simulé
      const errorMessage: Message = {
        id: Date.now().toString() + '_error_' + Math.random().toString(36).substr(2, 9),
        text: 'Désolé, je rencontre un problème technique. Veuillez réessayer.',
        user_id: 'Elavira Assistant',
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
      agent={ElaviraAgent}
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
