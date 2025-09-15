import React, { useState, useEffect, useRef } from 'react';
import styled from 'styled-components';
import { useApp } from '../../context/AppContext';
import { chatAPI } from '../../services/api';
import { Message } from '../../types';

const ChatContainer = styled.div`
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
`;

const ChatHeader = styled.div`
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  padding: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  gap: 16px;
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
  display: flex;
  flex-direction: column;
  gap: 16px;
`;

const MessageBubble = styled.div<{ isUser: boolean }>`
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 18px;
  word-wrap: break-word;
  line-height: 1.4;
  
  ${props => props.isUser ? `
    background: rgba(255, 255, 255, 0.9);
    color: #333;
    align-self: flex-end;
    border-bottom-right-radius: 4px;
  ` : `
    background: rgba(255, 255, 255, 0.15);
    color: white;
    align-self: flex-start;
    border-bottom-left-radius: 4px;
    backdrop-filter: blur(10px);
  `}
`;

const MessageTime = styled.div<{ isUser: boolean }>`
  font-size: 11px;
  color: ${props => props.isUser ? '#666' : 'rgba(255, 255, 255, 0.6)'};
  margin-top: 4px;
  text-align: ${props => props.isUser ? 'right' : 'left'};
`;

const InputContainer = styled.div`
  padding: 20px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-top: 1px solid rgba(255, 255, 255, 0.2);
`;

const InputWrapper = styled.div`
  display: flex;
  gap: 12px;
  align-items: flex-end;
`;

const MessageInput = styled.textarea`
  flex: 1;
  background: rgba(255, 255, 255, 0.9);
  border: none;
  border-radius: 20px;
  padding: 12px 16px;
  font-size: 14px;
  color: #333;
  resize: none;
  min-height: 44px;
  max-height: 120px;
  
  &::placeholder {
    color: #999;
  }
  
  &:focus {
    outline: none;
    box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.3);
  }
`;

const SendButton = styled.button`
  background: linear-gradient(135deg, #8b5cf6 0%, #a855f7 100%);
  border: none;
  border-radius: 50%;
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  cursor: pointer;
  transition: all 0.2s ease;
  
  &:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4);
  }
  
  &:disabled {
    opacity: 0.5;
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

export const ElaviraChatInterface: React.FC = () => {
  const { state, dispatch } = useApp();
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState('');
  const [isThinking, setIsThinking] = useState(false);
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
      setMessages(history);
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

  return (
    <ChatContainer>
      <ChatHeader>
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
        <InputWrapper>
          <MessageInput
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Posez votre question sur les formations FormEduc..."
            disabled={isThinking}
          />
          <SendButton
            onClick={() => handleSendMessage(inputText)}
            disabled={!inputText.trim() || isThinking}
          >
            ➤
          </SendButton>
        </InputWrapper>
      </InputContainer>
    </ChatContainer>
  );
};
