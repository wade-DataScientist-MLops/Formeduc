import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { useApp } from '../../context/AppContext';
import { ChatHistorySidebar } from './ChatHistorySidebar';
import { AgentLogs } from '../Logs/AgentLogs';
import { useAgentLogs } from '../../hooks/useAgentLogs';

const ChatContainer = styled.div`
  display: flex;
  height: calc(100vh - 128px);
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  position: relative;
`;

const ToggleSidebarButton = styled.button`
  position: absolute;
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

const MainContent = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  background: white;
  overflow: hidden;
`;

const ChatHeader = styled.div`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 20px 30px;
  display: flex;
  align-items: center;
  gap: 15px;
  border-radius: 10px 10px 0 0;
`;

const BackButton = styled.button`
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 20px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background 0.2s ease;

  &:hover {
    background: rgba(255, 255, 255, 0.3);
  }
`;

const AgentAvatar = styled.div`
  width: 50px;
  height: 50px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
`;

const AgentInfo = styled.div`
  flex: 1;
`;

const AgentName = styled.h2`
  margin: 0;
  font-size: 1.3rem;
  font-weight: 600;
`;

const AgentRole = styled.p`
  margin: 5px 0 0 0;
  font-size: 0.9rem;
  opacity: 0.9;
`;

const AgentDescription = styled.p`
  margin: 5px 0 0 0;
  font-size: 0.8rem;
  opacity: 0.8;
`;

const MessagesContainer = styled.div`
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 15px;
`;

const MessageBubble = styled.div<{ isUser: boolean }>`
  max-width: 70%;
  padding: 15px 20px;
  border-radius: 20px;
  word-wrap: break-word;
  align-self: ${props => props.isUser ? 'flex-end' : 'flex-start'};
  background: ${props => props.isUser ? '#667eea' : '#f1f3f4'};
  color: ${props => props.isUser ? 'white' : '#333'};
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
`;

const MessageTime = styled.div`
  font-size: 0.7rem;
  opacity: 0.7;
  margin-top: 5px;
`;

const InputContainer = styled.div`
  padding: 20px;
  background: #f8f9fa;
  border-top: 1px solid #e9ecef;
  display: flex;
  gap: 10px;
  align-items: center;
`;

const MessageInput = styled.input`
  flex: 1;
  padding: 12px 20px;
  border: 2px solid #e9ecef;
  border-radius: 25px;
  font-size: 1rem;
  outline: none;
  transition: border-color 0.2s ease;

  &:focus {
    border-color: #667eea;
  }
`;

const SendButton = styled.button`
  padding: 12px 24px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: background 0.2s ease;

  &:hover {
    background: #5a6fd8;
  }

  &:disabled {
    background: #ccc;
    cursor: not-allowed;
  }
`;

const ThinkingIndicator = styled.div`
  display: flex;
  align-items: center;
  gap: 5px;
  color: #666;
  font-style: italic;
`;

const Dot = styled.div`
  width: 8px;
  height: 8px;
  background: #667eea;
  border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out both;

  &:nth-child(1) { animation-delay: -0.32s; }
  &:nth-child(2) { animation-delay: -0.16s; }

  @keyframes bounce {
    0%, 80%, 100% { transform: scale(0); }
    40% { transform: scale(1); }
  }
`;

const QuickActions = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 10px;
`;

const QuickActionButton = styled.button`
  padding: 8px 16px;
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
  border: 1px solid #667eea;
  border-radius: 20px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s ease;

  &:hover {
    background: #667eea;
    color: white;
  }
`;

interface Message {
  id: string;
  content: string;
  isUser: boolean;
  timestamp: Date;
}

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
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [activeConversationId, setActiveConversationId] = useState<string | null>(null);
  const { logs, clearLogs, logRequest, logResponse, logError, logInfo } = useAgentLogs();

  const quickActions = [
    "Prix des formations",
    "Certifications reconnues", 
    "Formations en ligne",
    "Secourisme petite enfance",
    "Formations RSG/RSGE"
  ];

  useEffect(() => {
    loadChatHistory();
  }, []);

  const loadChatHistory = async () => {
    try {
      const response = await fetch('http://104.254.182.118:8000/chat/conversations/');
      if (response.ok) {
        const data = await response.json();
        setConversations(data);
      }
    } catch (error) {
      console.error('Erreur lors du chargement de l\'historique:', error);
    }
  };

  const handleSendMessage = async (text: string) => {
    if (!text.trim() || isThinking) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content: text,
      isUser: true,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsThinking(true);

    // Log de la requête
    logRequest('http://104.254.182.118:8000/chat/send_message/', 'POST', 'Elavira');
    logInfo(`Envoi du message: "${text}"`, 'Elavira');

    try {
      const response = await fetch('http://104.254.182.118:8000/chat/send_message/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: text,
          agent: 'elavira'
        }),
      });

      if (response.ok) {
        const data = await response.json();
        logResponse(response.status, `Réponse reçue (${data.text?.length || 0} caractères)`, 'Elavira');
        
        const assistantMessage: Message = {
          id: (Date.now() + 1).toString(),
          content: data.text || 'Réponse vide',
          isUser: false,
          timestamp: new Date()
        };
        setMessages(prev => [...prev, assistantMessage]);
        logInfo('Message affiché dans l\'interface', 'Elavira');
      } else {
        logResponse(response.status, `Erreur HTTP: ${response.statusText}`, 'Elavira');
        const errorMessage: Message = {
          id: (Date.now() + 1).toString(),
          content: 'Désolé, je rencontre des difficultés techniques. Veuillez réessayer.',
          isUser: false,
          timestamp: new Date()
        };
        setMessages(prev => [...prev, errorMessage]);
      }
    } catch (error) {
      console.error('Erreur lors de l\'envoi du message:', error);
      logError(`Erreur réseau: ${error}`, 'Elavira');
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: 'Désolé, je rencontre des difficultés techniques. Veuillez réessayer.',
        isUser: false,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsThinking(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage(inputText);
    }
  };

  const handleQuickAction = (action: string) => {
    handleSendMessage(action);
  };

  const handleNewChat = () => {
    setMessages([]);
    setActiveConversationId(null);
  };

  const handleConversationSelect = (conversationId: string) => {
    setActiveConversationId(conversationId);
    // Charger les messages de la conversation sélectionnée
    // TODO: Implémenter le chargement des messages
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
          <AgentAvatar>🎓</AgentAvatar>
          <AgentInfo>
            <AgentName>Elavira Assistant</AgentName>
            <AgentRole>Assistante FormEduc</AgentRole>
            <AgentDescription>Votre assistante pour les formations professionnelles</AgentDescription>
          </AgentInfo>
        </ChatHeader>

        <MessagesContainer>
          {messages.length === 0 && (
            <div style={{ textAlign: 'center', marginTop: '50px' }}>
              <h3 style={{ color: '#667eea', marginBottom: '20px' }}>
                Bonjour! 👋 Je suis Elavira, votre assistante FormEduc !
              </h3>
              <p style={{ color: '#666', marginBottom: '20px' }}>
                Je suis là pour vous accompagner dans vos besoins de formation professionnelle.
              </p>
              <QuickActions>
                {quickActions.map((action, index) => (
                  <QuickActionButton
                    key={index}
                    onClick={() => handleQuickAction(action)}
                  >
                    {action}
                  </QuickActionButton>
                ))}
              </QuickActions>
            </div>
          )}

          {messages.map((message) => (
            <MessageBubble key={message.id} isUser={message.isUser}>
              <div>{message.content}</div>
              <MessageTime>
                {message.timestamp.toLocaleTimeString()}
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
        </MessagesContainer>

        <InputContainer>
          <MessageInput
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
      
      <AgentLogs logs={logs} onClearLogs={clearLogs} />
    </ChatContainer>
  );
};
