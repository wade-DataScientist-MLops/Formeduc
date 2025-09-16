import React, { useState, useEffect, useRef } from 'react';
import styled from 'styled-components';
import { useApp } from '../../context/AppContext';
import { chatAPI } from '../../services/api';
import { Message } from '../../types';
import { ChatHistorySidebar } from './ChatHistorySidebar';

const ChatContainer = styled.div`
  display: flex;
  height: 100vh;
  background: #f0f2f5;
  font-family: 'Segoe UI', sans-serif;
`;

const MainContent = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
`;

const ToggleSidebarButton = styled.button`
  position: fixed;
  top: 20px;
  left: 20px;
  z-index: 1000;
  padding: 10px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  font-size: 1.2rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  transition: transform 0.2s ease;

  &:hover {
    transform: scale(1.1);
  }
`;

const ChatHeader = styled.div`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 20px 30px;
  display: flex;
  align-items: center;
  gap: 15px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
`;

const BackButton = styled.button`
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  
  &:hover {
    background: rgba(255, 255, 255, 0.3);
    transform: translateY(-1px);
  }
`;

const AgentAvatar = styled.div`
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #8b5cf6 0%, #a855f7 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
`;

const AgentInfo = styled.div`
  flex: 1;
`;

const AgentName = styled.h2`
  margin: 0;
  font-size: 24px;
  font-weight: 700;
  color: white;
`;

const AgentRole = styled.p`
  margin: 4px 0 0 0;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 500;
`;

const AgentDescription = styled.p`
  margin: 8px 0 0 0;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.7);
  line-height: 1.4;
`;

const MessagesContainer = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: #f8f9fa;
  display: flex;
  flex-direction: column;
  gap: 15px;
`;

const MessageBubble = styled.div<{ isUser: boolean }>`
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 18px;
  word-wrap: break-word;
  line-height: 1.4;
  
  ${props => props.isUser ? `
    background: #667eea;
    color: white;
    align-self: flex-end;
    border-bottom-right-radius: 4px;
  ` : `
    background: white;
    color: #333;
    align-self: flex-start;
    border-bottom-left-radius: 4px;
    border: 1px solid #e1e8ed;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  `}
`;

const MessageTime = styled.div<{ isUser: boolean }>`
  font-size: 11px;
  color: ${props => props.isUser ? 'rgba(255, 255, 255, 0.8)' : '#666'};
  margin-top: 4px;
  text-align: ${props => props.isUser ? 'right' : 'left'};
`;

const InputContainer = styled.div`
  padding: 20px 30px;
  background: white;
  border-top: 1px solid #e1e8ed;
  display: flex;
  gap: 15px;
  align-items: center;
`;

const MessageInput = styled.input`
  flex: 1;
  padding: 15px 20px;
  border: 2px solid #e1e8ed;
  border-radius: 25px;
  font-size: 1rem;
  outline: none;
  transition: border-color 0.3s ease;

  &:focus {
    border-color: #667eea;
  }
`;

const SendButton = styled.button`
  padding: 15px 25px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 25px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s ease;

  &:hover {
    transform: translateY(-2px);
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }
`;

const ThinkingIndicator = styled.div`
  display: flex;
  align-items: center;
  gap: 8px;
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
  font-style: italic;
`;

const Dot = styled.div`
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.7);
  animation: pulse 1.4s infinite ease-in-out;
  
  &:nth-child(1) { animation-delay: -0.32s; }
  &:nth-child(2) { animation-delay: -0.16s; }
  
  @keyframes pulse {
    0%, 80%, 100% { transform: scale(0); }
    40% { transform: scale(1); }
  }
`;

const QuickActions = styled.div`
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
  flex-wrap: wrap;
`;

const QuickActionButton = styled.button`
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  
  &:hover {
    background: rgba(255, 255, 255, 0.3);
    transform: translateY(-1px);
  }
`;

interface Conversation {
  id: string;
  title: string;
  lastMessage: string;
  timestamp: string;
  agent: string;
}

export const ElaviraChatInterface: React.FC = () => {
  const { state, dispatch } = useApp();
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState('');
  const [isThinking, setIsThinking] = useState(false);
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [activeConversationId, setActiveConversationId] = useState<string | null>(null);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const quickActions = [
    "Quelles formations proposez-vous ?",
    "Prix des formations",
    "Certifications reconnues",
    "Formations en ligne",
    "Secourisme petite enfance",
    "Formations RSG/RSGE"
  ];

  useEffect(() => {
    loadChatHistory();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const loadChatHistory = async () => {
    try {
      const history = await chatAPI.getHistory('elavira', state.logged_in_user || 'Guest');
      // Filtrer seulement les messages d'Elavira
      const elaviraMessages = history.filter(msg => 
        msg.user_id === 'Elavira Assistant' || msg.user_id === state.logged_in_user || msg.user_id === 'Vous'
      );
      setMessages(elaviraMessages);
    } catch (error) {
      console.error('Erreur lors du chargement de l\'historique:', error);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async (text: string) => {
    if (!text.trim() || isThinking) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: text.trim(),
      user_id: state.logged_in_user || 'Vous',
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsThinking(true);

    try {
      const response = await chatAPI.sendMessage({
        text: text.trim(),
        user_id: state.logged_in_user || 'Guest',
        agent: 'elavira'
      });

      setMessages(prev => [...prev, response]);
    } catch (error) {
      console.error('Erreur lors de l\'envoi du message:', error);
      const errorMessage: Message = {
        id: Date.now().toString(),
        text: 'Désolé, je rencontre des difficultés techniques. Veuillez réessayer.',
        user_id: 'Elavira Assistant',
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsThinking(false);
    }
  };

  const handleQuickAction = (action: string) => {
    handleSendMessage(action);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage(inputText);
    }
  };

  const handleNewChat = () => {
    const newConversation: Conversation = {
      id: `conv_${Date.now()}`,
      title: 'Nouvelle conversation',
      lastMessage: '',
      timestamp: new Date().toISOString(),
      agent: 'Elavira'
    };
    setConversations(prev => [newConversation, ...prev]);
    setActiveConversationId(newConversation.id);
    setMessages([]);
  };

  const handleConversationSelect = (conversationId: string) => {
    setActiveConversationId(conversationId);
    // Charger les messages de cette conversation
    // Pour l'instant, on vide les messages
    setMessages([]);
  };

  const handleBackToAgents = () => {
    dispatch({ type: 'SET_PAGE', payload: 'agents' });
  };

  return (
    <div style={{ height: '100%', display: 'flex', flexDirection: 'column', position: 'relative', marginTop: '20px' }}>
      <ChatContainer style={{ height: 'calc(100% - 20px)', position: 'relative' }}>
        <ToggleSidebarButton onClick={() => setSidebarOpen(!sidebarOpen)}>
          ☰
        </ToggleSidebarButton>
        
        {sidebarOpen && (
          <ChatHistorySidebar
            conversations={conversations}
            activeConversationId={activeConversationId || undefined}
            onConversationSelect={handleConversationSelect}
            onNewChat={handleNewChat}
          />
        )}

        <MainContent style={{ height: '100%' }}>
        <ChatHeader>
          <BackButton onClick={handleBackToAgents}>
            ← Retour aux agents
          </BackButton>
          <AgentAvatar>🎓</AgentAvatar>
          <AgentInfo>
            <AgentName>Elavira</AgentName>
            <AgentRole>Spécialiste FormEduc</AgentRole>
            <AgentDescription>
              Votre assistante pour les formations professionnelles : secourisme, RSG, RSGE et plus
            </AgentDescription>
          </AgentInfo>
        </ChatHeader>

      <MessagesContainer>
        <QuickActions>
          {quickActions.map((action, index) => (
            <QuickActionButton
              key={index}
              onClick={() => handleQuickAction(action)}
              disabled={isThinking}
            >
              {action}
            </QuickActionButton>
          ))}
        </QuickActions>

        {messages.map((message) => (
          <MessageBubble key={message.id} isUser={message.user_id !== 'Elavira Assistant'}>
            {message.text}
            <MessageTime isUser={message.user_id !== 'Elavira Assistant'}>
              {new Date(message.timestamp).toLocaleTimeString()}
            </MessageTime>
          </MessageBubble>
        ))}

        {isThinking && (
          <ThinkingIndicator>
            <span>Elavira réfléchit</span>
            <Dot />
            <Dot />
            <Dot />
          </ThinkingIndicator>
        )}

        <div ref={messagesEndRef} />
      </MessagesContainer>

        <InputContainer>
          <MessageInput
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Posez votre question à Elavira..."
            disabled={isThinking}
          />
          <SendButton
            onClick={() => handleSendMessage(inputText)}
            disabled={!inputText.trim() || isThinking}
          >
            Envoyer
          </SendButton>
        </InputContainer>
      </MainContent>
    </ChatContainer>
    </div>
  );
};
