import React, { useEffect, useRef } from 'react';
import styled from 'styled-components';
import { Message } from '../../types';
import { MessageBubble } from './MessageBubble';
import { MessageInput } from './MessageInput';

const ChatContainer = styled.div`
  display: flex;
  height: 100vh;
  background: #f7f7f8;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
`;

const Sidebar = styled.div`
  width: 260px;
  background: #171717;
  color: white;
  display: flex;
  flex-direction: column;
  border-right: 1px solid #2d2d2d;
`;

const SidebarHeader = styled.div`
  padding: 20px;
  border-bottom: 1px solid #2d2d2d;
`;

const NewChatButton = styled.button`
  width: 100%;
  padding: 12px 16px;
  background: transparent;
  border: 1px solid #4d4d4f;
  color: white;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  transition: all 0.2s;

  &:hover {
    background: #2d2d2d;
  }
`;

const ConversationsList = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 8px;
`;

const ConversationItem = styled.div<{ active: boolean }>`
  padding: 12px 16px;
  margin: 4px 0;
  border-radius: 8px;
  cursor: pointer;
  background: ${props => props.active ? '#2d2d2d' : 'transparent'};
  color: ${props => props.active ? 'white' : '#c5c5d2'};
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 12px;

  &:hover {
    background: #2d2d2d;
    color: white;
  }
`;

const ConversationIcon = styled.div`
  width: 20px;
  height: 20px;
  border-radius: 4px;
  background: #4d4d4f;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
`;

const ConversationTitle = styled.div`
  flex: 1;
  font-size: 14px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
`;

const MainContent = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  background: white;
`;

const ChatHeader = styled.div`
  padding: 20px 24px;
  border-bottom: 1px solid #e5e5e5;
  display: flex;
  align-items: center;
  gap: 16px;
  background: white;
`;

const AgentAvatar = styled.div<{ color: string }>`
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: ${props => props.color};
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  color: white;
  font-weight: bold;
`;

const AgentInfo = styled.div`
  flex: 1;
`;

const AgentName = styled.h1`
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #1a1a1a;
`;

const AgentDescription = styled.p`
  margin: 4px 0 0 0;
  font-size: 14px;
  color: #6b7280;
`;

const MessagesContainer = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 20px 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  background: #f7f7f8;
`;

const EmptyState = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #6b7280;
  text-align: center;
`;

const EmptyIcon = styled.div`
  font-size: 48px;
  margin-bottom: 16px;
`;

const EmptyTitle = styled.h3`
  margin: 0 0 8px 0;
  font-size: 18px;
  font-weight: 600;
`;

const EmptyDescription = styled.p`
  margin: 0;
  font-size: 14px;
  max-width: 400px;
`;

const SuggestedPrompts = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 16px;
`;

const PromptButton = styled.button`
  padding: 8px 16px;
  background: white;
  border: 1px solid #e5e5e5;
  border-radius: 20px;
  cursor: pointer;
  font-size: 14px;
  color: #374151;
  transition: all 0.2s;

  &:hover {
    background: #f3f4f6;
    border-color: #d1d5db;
  }
`;

const InputContainer = styled.div`
  padding: 20px 24px;
  background: white;
  border-top: 1px solid #e5e5e5;
`;

interface ModernChatInterfaceProps {
  agent: {
    id: string;
    name: string;
    description: string;
    avatar: string;
    color: string;
  };
  messages: Message[];
  onSendMessage: (text: string) => void;
  conversations: Array<{
    id: string;
    title: string;
    lastMessage: string;
    timestamp: string;
  }>;
  activeConversationId?: string;
  onConversationSelect: (id: string) => void;
  onNewChat: () => void;
  suggestedPrompts?: string[];
}

export const ModernChatInterface: React.FC<ModernChatInterfaceProps> = ({
  agent,
  messages,
  onSendMessage,
  conversations,
  activeConversationId,
  onConversationSelect,
  onNewChat,
  suggestedPrompts = []
}) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handlePromptClick = (prompt: string) => {
    onSendMessage(prompt);
  };

  return (
    <ChatContainer>
      <Sidebar>
        <SidebarHeader>
          <NewChatButton onClick={onNewChat}>
            <span>+</span>
            Nouvelle conversation
          </NewChatButton>
        </SidebarHeader>
        
        <ConversationsList>
          {conversations.map((conversation) => (
            <ConversationItem
              key={conversation.id}
              active={conversation.id === activeConversationId}
              onClick={() => onConversationSelect(conversation.id)}
            >
              <ConversationIcon>
                {agent.avatar}
              </ConversationIcon>
              <ConversationTitle>
                {conversation.title}
              </ConversationTitle>
            </ConversationItem>
          ))}
        </ConversationsList>
      </Sidebar>

      <MainContent>
        <ChatHeader>
          <AgentAvatar color={agent.color}>
            {agent.avatar}
          </AgentAvatar>
          <AgentInfo>
            <AgentName>{agent.name}</AgentName>
            <AgentDescription>{agent.description}</AgentDescription>
          </AgentInfo>
        </ChatHeader>

        <MessagesContainer>
          {messages.length === 0 ? (
            <EmptyState>
              <EmptyIcon>{agent.avatar}</EmptyIcon>
              <EmptyTitle>Bonjour ! Je suis {agent.name}</EmptyTitle>
              <EmptyDescription>
                {agent.description}
              </EmptyDescription>
              
              {suggestedPrompts.length > 0 && (
                <SuggestedPrompts>
                  {suggestedPrompts.map((prompt, index) => (
                    <PromptButton
                      key={index}
                      onClick={() => handlePromptClick(prompt)}
                    >
                      {prompt}
                    </PromptButton>
                  ))}
                </SuggestedPrompts>
              )}
            </EmptyState>
          ) : (
            <>
              {messages.map((message) => (
                <MessageBubble key={message.id} message={message} />
              ))}
              <div ref={messagesEndRef} />
            </>
          )}
        </MessagesContainer>

        <InputContainer>
          <MessageInput
            onSendMessage={onSendMessage}
            placeholder={`Posez votre question à ${agent.name}...`}
          />
        </InputContainer>
      </MainContent>
    </ChatContainer>
  );
};
