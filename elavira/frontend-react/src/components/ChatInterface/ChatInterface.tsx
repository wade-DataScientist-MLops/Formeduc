import React, { useRef, useEffect } from 'react';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';

const ChatContainer = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 400px;
  border: 1px solid #e0e0e0;
  border-radius: 15px;
  overflow: hidden;
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

const Message = styled(motion.div)<{ $isUser: boolean }>`
  display: flex;
  justify-content: ${props => props.$isUser ? 'flex-end' : 'flex-start'};
  margin-bottom: 10px;
`;

const MessageBubble = styled.div<{ $isUser: boolean }>`
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 18px;
  background: ${props => props.$isUser ? '#007bff' : '#e9ecef'};
  color: ${props => props.$isUser ? 'white' : '#333'};
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: relative;
`;

const MessageHeader = styled.div`
  font-weight: 600;
  font-size: 12px;
  margin-bottom: 5px;
  opacity: 0.8;
`;

const MessageText = styled.div`
  line-height: 1.4;
  word-wrap: break-word;
`;

const MessageTime = styled.div`
  font-size: 10px;
  opacity: 0.6;
  margin-top: 5px;
`;

const AudioPlayer = styled.audio`
  width: 100%;
  margin-top: 8px;
`;

const EmptyState = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #6c757d;
  text-align: center;
`;

const EmptyIcon = styled.div`
  font-size: 48px;
  margin-bottom: 16px;
`;

const EmptyText = styled.p`
  font-size: 16px;
  margin: 0;
`;

interface Message {
  id: string;
  text: string;
  user_id: string;
  timestamp: string;
  audio_base64?: string;
}

interface ChatInterfaceProps {
  messages: Message[];
  selectedAgent: 'elavira' | 'solenys';
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({ messages, selectedAgent }) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const formatTime = (timestamp: string) => {
    try {
      const date = new Date(timestamp);
      return date.toLocaleTimeString('fr-FR', { 
        hour: '2-digit', 
        minute: '2-digit' 
      });
    } catch {
      return timestamp;
    }
  };

  const isUserMessage = (userId: string) => {
    return userId === 'Vous';
  };

  const getAgentEmoji = (userId: string) => {
    if (userId === 'Elavira Assistant') return '🏥';
    if (userId === 'Solenys Assistant') return '🎓';
    return '🤖';
  };

  return (
    <ChatContainer>
      <MessagesContainer>
        {messages.length === 0 ? (
          <EmptyState>
            <EmptyIcon>💬</EmptyIcon>
            <EmptyText>
              Commencez une conversation avec {selectedAgent === 'elavira' ? 'Elavira' : 'Solenys'} !
              <br />
              Utilisez l'interface vocale ci-dessus.
            </EmptyText>
          </EmptyState>
        ) : (
          <AnimatePresence>
            {messages.map((message) => (
              <Message
                key={message.id}
                $isUser={isUserMessage(message.user_id)}
                initial={{ opacity: 0, y: 20, scale: 0.9 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, y: -20, scale: 0.9 }}
                transition={{ duration: 0.3 }}
              >
                <MessageBubble $isUser={isUserMessage(message.user_id)}>
                  <MessageHeader>
                    {getAgentEmoji(message.user_id)} {message.user_id}
                  </MessageHeader>
                  <MessageText>{message.text}</MessageText>
                  <MessageTime>{formatTime(message.timestamp)}</MessageTime>
                  
                  {message.audio_base64 && (
                    <AudioPlayer
                      controls
                      autoPlay
                      src={`data:audio/wav;base64,${message.audio_base64}`}
                    />
                  )}
                </MessageBubble>
              </Message>
            ))}
          </AnimatePresence>
        )}
        <div ref={messagesEndRef} />
      </MessagesContainer>
    </ChatContainer>
  );
};

export default ChatInterface;
