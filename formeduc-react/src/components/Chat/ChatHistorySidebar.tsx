import React from 'react';
import styled from 'styled-components';

const SidebarContainer = styled.div`
  width: 260px;
  height: 100vh;
  background: #f8f9fa;
  border-right: 1px solid #e1e8ed;
  display: flex;
  flex-direction: column;
  position: fixed;
  left: 0;
  top: 0;
  z-index: 1000;
  overflow-y: auto;
`;

const SidebarHeader = styled.div`
  padding: 20px;
  border-bottom: 1px solid #e1e8ed;
  background: white;
`;

const NewChatButton = styled.button`
  width: 100%;
  padding: 12px 16px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s ease;
  display: flex;
  align-items: center;
  gap: 8px;

  &:hover {
    background: #2e6bb4;
  }
`;

const HistoryContainer = styled.div`
  flex: 1;
  padding: 16px;
  overflow-y: auto;
`;

const HistoryTitle = styled.h3`
  font-size: 14px;
  font-weight: 600;
  color: #6b7280;
  margin: 0 0 12px 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
`;

const ConversationItem = styled.div<{ isActive: boolean }>`
  padding: 12px 16px;
  margin-bottom: 4px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  background: ${props => props.isActive ? '#e1f0ff' : 'transparent'};
  border: ${props => props.isActive ? '1px solid #3b82f6' : '1px solid transparent'};

  &:hover {
    background: ${props => props.isActive ? '#e1f0ff' : '#f1f5f9'};
  }
`;

const ConversationTitle = styled.div`
  font-size: 14px;
  font-weight: 500;
  color: #2c3e50;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
`;

const ConversationDate = styled.div`
  font-size: 12px;
  color: #6b7280;
`;

const ConversationPreview = styled.div`
  font-size: 12px;
  color: #9ca3af;
  margin-top: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
`;

const EmptyState = styled.div`
  text-align: center;
  padding: 40px 20px;
  color: #6b7280;
`;

const EmptyStateIcon = styled.div`
  font-size: 48px;
  margin-bottom: 16px;
`;

const EmptyStateText = styled.div`
  font-size: 14px;
  line-height: 1.5;
`;

interface Conversation {
  id: string;
  title: string;
  lastMessage: string;
  timestamp: string;
  agent: string;
}

interface ChatHistorySidebarProps {
  conversations: Conversation[];
  activeConversationId?: string;
  onConversationSelect: (conversationId: string) => void;
  onNewChat: () => void;
}

export const ChatHistorySidebar: React.FC<ChatHistorySidebarProps> = ({
  conversations,
  activeConversationId,
  onConversationSelect,
  onNewChat,
}) => {
  const formatDate = (timestamp: string) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffInHours = (now.getTime() - date.getTime()) / (1000 * 60 * 60);

    if (diffInHours < 24) {
      return date.toLocaleTimeString('fr-FR', { 
        hour: '2-digit', 
        minute: '2-digit' 
      });
    } else if (diffInHours < 168) { // 7 days
      return date.toLocaleDateString('fr-FR', { 
        weekday: 'short',
        hour: '2-digit',
        minute: '2-digit'
      });
    } else {
      return date.toLocaleDateString('fr-FR', { 
        day: '2-digit',
        month: '2-digit'
      });
    }
  };

  return (
    <SidebarContainer>
      <SidebarHeader>
        <NewChatButton onClick={onNewChat}>
          <span>+</span>
          <span>Nouvelle conversation</span>
        </NewChatButton>
      </SidebarHeader>
      
      <HistoryContainer>
        <HistoryTitle>Historique</HistoryTitle>
        
        {conversations.length === 0 ? (
          <EmptyState>
            <EmptyStateIcon>💬</EmptyStateIcon>
            <EmptyStateText>
              Aucune conversation<br />
              Commencez une nouvelle discussion !
            </EmptyStateText>
          </EmptyState>
        ) : (
          conversations.map((conversation) => (
            <ConversationItem
              key={conversation.id}
              isActive={conversation.id === activeConversationId}
              onClick={() => onConversationSelect(conversation.id)}
            >
              <ConversationTitle>{conversation.title}</ConversationTitle>
              <ConversationDate>{formatDate(conversation.timestamp)}</ConversationDate>
              <ConversationPreview>{conversation.lastMessage}</ConversationPreview>
            </ConversationItem>
          ))
        )}
      </HistoryContainer>
    </SidebarContainer>
  );
};
