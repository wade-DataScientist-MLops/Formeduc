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
  margin-left: 260px;
  background: white;
  border-radius: 20px 0 0 20px;
  box-shadow: -2px 0 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
`;

const ToggleSidebarButton = styled.button`
  position: fixed;
  top: 20px;
  left: 20px;
  z-index: 1000;
  padding: 10px;
  background: #f093fb;
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
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
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
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
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
    background: #f093fb;
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
    border-color: #f093fb;
  }
`;

const SendButton = styled.button`
  padding: 15px 25px;
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
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

const SubjectTabs = styled.div`
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
  flex-wrap: wrap;
`;

const SubjectTab = styled.button`
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
  padding: 6px 12px;
  border-radius: 16px;
  font-size: 11px;
  cursor: pointer;
  transition: all 0.2s ease;
  
  &:hover {
    background: rgba(255, 255, 255, 0.25);
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

export const SolenysChatInterface: React.FC = () => {
  const { state, dispatch } = useApp();
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState('');
  const [isThinking, setIsThinking] = useState(false);
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [activeConversationId, setActiveConversationId] = useState<string | null>(null);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const quickActions = [
    "Aide en mathématiques",
    "Problèmes de physique",
    "Questions de chimie",
    "Français et littérature",
    "Histoire du Québec",
    "Géographie"
  ];

  const subjects = [
    "Mathématiques", "Physique", "Chimie", "Biologie", 
    "Français", "Histoire", "Géographie", "Anglais"
  ];

  useEffect(() => {
    loadChatHistory();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const loadChatHistory = async () => {
    try {
      const history = await chatAPI.getHistory('solenys', state.logged_in_user || 'Guest');
      // Filtrer seulement les messages de Solenys
      const solenysMessages = history.filter(msg => 
        msg.user_id === 'Solenys Assistant' || msg.user_id === state.logged_in_user || msg.user_id === 'Vous'
      );
      setMessages(solenysMessages);
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
        agent: 'solenys'
      });

      setMessages(prev => [...prev, response]);
    } catch (error) {
      console.error('Erreur lors de l\'envoi du message:', error);
      const errorMessage: Message = {
        id: Date.now().toString(),
        text: 'Désolé, je rencontre des difficultés techniques. Veuillez réessayer.',
        user_id: 'Solenys Assistant',
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

  const handleSubjectClick = (subject: string) => {
    handleSendMessage(`J'ai besoin d'aide en ${subject.toLowerCase()}`);
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
      agent: 'Solenys'
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
    <ChatContainer>
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

      <MainContent>
        <ChatHeader>
          <BackButton onClick={handleBackToAgents}>
            ← Retour aux agents
          </BackButton>
          <AgentAvatar>👨‍🏫</AgentAvatar>
          <AgentInfo>
            <AgentName>Solenys</AgentName>
            <AgentRole>Professeur québécois</AgentRole>
            <AgentDescription>
              Votre professeur spécialisé dans l'enseignement secondaire selon le programme PFEQ du Québec
            </AgentDescription>
          </AgentInfo>
        </ChatHeader>

      <MessagesContainer>
        <SubjectTabs>
          {subjects.map((subject, index) => (
            <SubjectTab
              key={index}
              onClick={() => handleSubjectClick(subject)}
              disabled={isThinking}
            >
              {subject}
            </SubjectTab>
          ))}
        </SubjectTabs>

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
          <MessageBubble key={message.id} isUser={message.user_id !== 'Solenys Assistant'}>
            {message.text}
            <MessageTime isUser={message.user_id !== 'Solenys Assistant'}>
              {new Date(message.timestamp).toLocaleTimeString()}
            </MessageTime>
          </MessageBubble>
        ))}

        {isThinking && (
          <ThinkingIndicator>
            <span>Solenys réfléchit</span>
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
            placeholder="Posez votre question à Solenys..."
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
  );
};
