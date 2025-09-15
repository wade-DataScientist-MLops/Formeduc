import React, { useEffect, useRef, useCallback } from 'react';
import styled from 'styled-components';
import { useApp } from '../../context/AppContext';
import { chatAPI } from '../../services/api';
import { Message, Conversation } from '../../types';
import { MessageBubble } from './MessageBubble';
import { MessageInput } from './MessageInput';
import { AgentSelector } from './AgentSelector';
import { SuggestedPrompts } from './SuggestedPrompts';
import { AssistantShowcase } from './AssistantShowcase';
import { ChatHistorySidebar } from './ChatHistorySidebar';

const ChatContainer = styled.div`
  display: flex;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  font-family: 'Segoe UI', sans-serif;
`;

const MainContent = styled.div`
  display: flex;
  flex-direction: column;
  flex: 1;
  margin-left: 260px; /* Width of sidebar */
`;

const ChatHeader = styled.div`
  background: white;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const HeaderLeft = styled.div`
  display: flex;
  align-items: center;
  gap: 20px;
`;

const HeaderRight = styled.div`
  display: flex;
  align-items: center;
  gap: 15px;
`;

const Title = styled.h1`
  color: #2c3e50;
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
`;

const UserInfo = styled.div`
  color: #34495e;
  font-size: 0.9rem;
`;

const LogoutButton = styled.button`
  padding: 8px 16px;
  background: #e53e3e;
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.3s ease;

  &:hover {
    background: #c53030;
    transform: translateY(-1px);
  }
`;

const MessagesContainer = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 15px;
  background: #f8f9fa;
`;

const EmptyState = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #a0aec0;
  text-align: center;
`;

const EmptyStateIcon = styled.div`
  font-size: 4rem;
  margin-bottom: 20px;
`;

const EmptyStateText = styled.p`
  font-size: 1.1rem;
  margin: 0;
`;

const ThinkingIndicator = styled.div`
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 15px 20px;
  background: #e1f0ff;
  border-radius: 20px;
  margin-left: auto;
  margin-right: 20px;
  max-width: fit-content;
  animation: pulse 1.5s infinite;

  @keyframes pulse {
    0% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.02); opacity: 0.9; }
    100% { transform: scale(1); opacity: 1; }
  }
`;

const TranscribingIndicator = styled.div`
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 15px 20px;
  background: #f0f0f0;
  border-radius: 20px;
  margin-right: auto;
  margin-left: 20px;
  max-width: fit-content;
  animation: pulse 1.5s infinite;
`;

const InputContainer = styled.div`
  background: white;
  padding: 20px;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
`;

export const ChatInterface: React.FC = () => {
  const { state, dispatch } = useApp();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadChatHistory = useCallback(async () => {
    try {
      const messages = await chatAPI.getHistory(
        state.selected_agent_id,
        state.logged_in_user || 'Guest'
      );
      dispatch({ type: 'SET_MESSAGES', payload: messages });
    } catch (error) {
      console.error('Erreur lors du chargement de l\'historique:', error);
    }
  }, [state.selected_agent_id, state.logged_in_user, dispatch]);

  useEffect(() => {
    scrollToBottom();
  }, [state.messages]);

  useEffect(() => {
    if (state.logged_in_user && state.access_token) {
      loadChatHistory();
    }
  }, [loadChatHistory, state.access_token, state.logged_in_user]);

  const handleSendMessage = async (text: string) => {
    if (!text.trim() || state.thinking || state.transcribing) return;

    const userMessage: Message = {
      id: Date.now().toString() + '_user_' + Math.random().toString(36).substr(2, 9),
      text: text.trim(),
      user_id: state.logged_in_user || 'Vous',
      timestamp: new Date().toISOString(),
    };

    dispatch({ type: 'ADD_MESSAGE', payload: userMessage });
    dispatch({ type: 'SET_MESSAGE_INPUT', payload: '' });
    dispatch({ type: 'SET_THINKING', payload: true });

    try {
      let response: Message;

      // Utiliser l'API unifiée avec l'agent spécifié
      response = await chatAPI.sendMessage({
        text: text.trim(),
        user_id: state.logged_in_user || 'Guest',
        agent: state.selected_agent_id, // Envoyer l'agent sélectionné
      });

      dispatch({ type: 'ADD_MESSAGE', payload: response });
      
      // Sauvegarder la conversation
      const updatedMessages = [...state.messages, userMessage, response];
      const conversation = createConversationFromMessages(updatedMessages);
      
      if (state.active_conversation_id) {
        // Mettre à jour la conversation existante
        dispatch({ type: 'UPDATE_CONVERSATION', payload: conversation });
      } else {
        // Créer une nouvelle conversation
        dispatch({ type: 'ADD_CONVERSATION', payload: conversation });
        dispatch({ type: 'SET_ACTIVE_CONVERSATION', payload: conversation.id });
      }
      
      if (response.suggested_prompts) {
        dispatch({ type: 'SET_LAST_SUGGESTED_PROMPTS', payload: response.suggested_prompts });
      }
    } catch (error) {
      console.error('Erreur lors de l\'envoi du message:', error);
      const errorMessage: Message = {
        id: Date.now().toString() + '_error_' + Math.random().toString(36).substr(2, 9),
        text: 'Désolé, une erreur s\'est produite. Veuillez réessayer.',
        user_id: 'Assistant',
        timestamp: new Date().toISOString(),
      };
      dispatch({ type: 'ADD_MESSAGE', payload: errorMessage });
    } finally {
      dispatch({ type: 'SET_THINKING', payload: false });
    }
  };

  const handleTranscribeAudio = async (audioFile: File) => {
    dispatch({ type: 'SET_TRANSCRIBING', payload: true });

    try {
      const response = await chatAPI.transcribeAudio(audioFile);
      if (response.transcribed_text) {
        await handleSendMessage(response.transcribed_text);
      }
    } catch (error) {
      console.error('Erreur lors de la transcription:', error);
    } finally {
      dispatch({ type: 'SET_TRANSCRIBING', payload: false });
    }
  };

  const handleLogout = () => {
    dispatch({ type: 'LOGOUT' });
  };

  const handleSuggestedPromptClick = (prompt: string) => {
    dispatch({ type: 'SET_MESSAGE_INPUT', payload: prompt });
    dispatch({ type: 'SET_DISPLAY_SUGGESTIONS', payload: false });
  };

  const handleNewChat = () => {
    dispatch({ type: 'SET_MESSAGES', payload: [] });
    dispatch({ type: 'SET_ACTIVE_CONVERSATION', payload: null });
    dispatch({ type: 'SET_LAST_SUGGESTED_PROMPTS', payload: [] });
    dispatch({ type: 'SET_DISPLAY_SUGGESTIONS', payload: false });
  };

  const handleConversationSelect = (conversationId: string) => {
    const conversation = state.conversations.find(c => c.id === conversationId);
    if (conversation) {
      dispatch({ type: 'SET_MESSAGES', payload: conversation.messages });
      dispatch({ type: 'SET_ACTIVE_CONVERSATION', payload: conversationId });
    }
  };

  const createConversationFromMessages = (messages: Message[]): Conversation => {
    const firstUserMessage = messages.find(m => !m.user_id.includes('Assistant'));
    const lastMessage = messages[messages.length - 1];
    
    return {
      id: `conv_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      title: firstUserMessage?.text.slice(0, 50) + '...' || 'Nouvelle conversation',
      lastMessage: lastMessage?.text.slice(0, 100) + '...' || '',
      timestamp: lastMessage?.timestamp || new Date().toISOString(),
      agent: state.selected_agent_id,
      messages: messages,
    };
  };

  return (
    <ChatContainer>
      {state.sidebar_open && (
        <ChatHistorySidebar
          conversations={state.conversations}
          activeConversationId={state.active_conversation_id}
          onConversationSelect={handleConversationSelect}
          onNewChat={handleNewChat}
        />
      )}
      
      <MainContent>
        <ChatHeader>
          <HeaderLeft>
            <Title>Messagerie intelligente 💬</Title>
            <AgentSelector />
          </HeaderLeft>
          <HeaderRight>
            <UserInfo>Connecté en tant que <strong>{state.logged_in_user}</strong></UserInfo>
            <LogoutButton onClick={handleLogout}>
              Se déconnecter
            </LogoutButton>
          </HeaderRight>
        </ChatHeader>

      <MessagesContainer>
        {state.messages.length === 0 && !state.thinking && !state.transcribing ? (
          <>
            <EmptyState>
              <EmptyStateIcon>💬</EmptyStateIcon>
              <EmptyStateText>
                Aucun message dans l'historique. Commencez la conversation ci-dessous !
              </EmptyStateText>
            </EmptyState>
            <AssistantShowcase />
          </>
        ) : (
          <>
            {state.messages.map((message) => (
              <MessageBubble key={message.id} message={message} />
            ))}
            
            {state.thinking && (
              <ThinkingIndicator>
                <span>⏳</span>
                <span>Réflexion en cours...</span>
              </ThinkingIndicator>
            )}
            
            {state.transcribing && (
              <TranscribingIndicator>
                <span>🎙️</span>
                <span>Transcription en cours...</span>
              </TranscribingIndicator>
            )}
          </>
        )}
        <div ref={messagesEndRef} />
      </MessagesContainer>

      {state.last_suggested_prompts.length > 0 && !state.display_suggestions && (
        <SuggestedPrompts
          prompts={state.last_suggested_prompts}
          onPromptClick={handleSuggestedPromptClick}
          onShowSuggestions={() => dispatch({ type: 'SET_DISPLAY_SUGGESTIONS', payload: true })}
        />
      )}

      {state.display_suggestions && state.last_suggested_prompts.length > 0 && (
        <SuggestedPrompts
          prompts={state.last_suggested_prompts}
          onPromptClick={handleSuggestedPromptClick}
          onShowSuggestions={() => dispatch({ type: 'SET_DISPLAY_SUGGESTIONS', payload: false })}
          showAll={true}
        />
      )}

        <InputContainer>
          <MessageInput
            onSendMessage={handleSendMessage}
            onTranscribeAudio={handleTranscribeAudio}
            disabled={state.thinking || state.transcribing}
            audioEnabled={state.audio_enabled}
            onToggleAudio={() => dispatch({ type: 'SET_AUDIO_ENABLED', payload: !state.audio_enabled })}
          />
        </InputContainer>
      </MainContent>
    </ChatContainer>
  );
};
