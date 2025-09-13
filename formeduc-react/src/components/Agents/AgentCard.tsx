import React from 'react';
import styled from 'styled-components';

const Card = styled.div`
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
  transition: all 0.2s;

  &:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    transform: translateY(-2px);
  }
`;

const CardHeader = styled.div`
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
`;

const Avatar = styled.div<{ src?: string }>`
  width: 60px;
  height: 60px;
  border-radius: 12px;
  background: ${props => props.src ? `url(${props.src})` : '#3b82f6'};
  background-size: cover;
  background-position: center;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: white;
  font-weight: bold;
  border: 2px solid #e2e8f0;
`;

const AgentInfo = styled.div`
  flex: 1;
`;

const AgentName = styled.h3`
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 4px 0;
`;

const AgentType = styled.span`
  background: #e0f2fe;
  color: #0369a1;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 500;
`;

const Description = styled.p`
  color: #64748b;
  font-size: 0.9rem;
  line-height: 1.5;
  margin: 12px 0;
`;

const Capabilities = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin: 12px 0;
`;

const CapabilityTag = styled.span`
  background: #f1f5f9;
  color: #475569;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
`;

const MoreTag = styled.span`
  background: #e2e8f0;
  color: #64748b;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
`;

const Footer = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #e2e8f0;
`;

const CreatedInfo = styled.div`
  font-size: 0.8rem;
  color: #64748b;
`;

const Actions = styled.div`
  display: flex;
  gap: 8px;
`;

const ActionButton = styled.button<{ variant?: 'primary' | 'secondary' | 'danger' }>`
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  border: 1px solid transparent;
  transition: all 0.2s;

  ${props => {
    switch (props.variant) {
      case 'primary':
        return `
          background: #3b82f6;
          color: white;
          &:hover { background: #2563eb; }
        `;
      case 'danger':
        return `
          background: #ef4444;
          color: white;
          &:hover { background: #dc2626; }
        `;
      default:
        return `
          background: white;
          color: #64748b;
          border-color: #e2e8f0;
          &:hover { background: #f8fafc; }
        `;
    }
  }}
`;

interface Agent {
  id: string;
  name: string;
  type: string;
  description: string;
  capabilities: string[];
  avatar: string;
  createdAt: string;
  knowledgePacks: number;
}

interface AgentCardProps {
  agent: Agent;
  onChatClick?: () => void;
}

export const AgentCard: React.FC<AgentCardProps> = ({ agent, onChatClick }) => {
  const visibleCapabilities = agent.capabilities.slice(0, 4);
  const remainingCapabilities = agent.capabilities.length - 4;

  return (
    <Card>
      <CardHeader>
        <Avatar src={agent.avatar}>
          {!agent.avatar && agent.name.charAt(0)}
        </Avatar>
        <AgentInfo>
          <AgentName>{agent.name}</AgentName>
          <AgentType>{agent.type}</AgentType>
        </AgentInfo>
      </CardHeader>

      <Description>{agent.description}</Description>

      <Capabilities>
        {visibleCapabilities.map((capability, index) => (
          <CapabilityTag key={index}>{capability}</CapabilityTag>
        ))}
        {remainingCapabilities > 0 && (
          <MoreTag>+{remainingCapabilities} autres</MoreTag>
        )}
      </Capabilities>

      <Footer>
        <CreatedInfo>
          Créé le {agent.createdAt}
          {agent.knowledgePacks > 0 && (
            <div>{agent.knowledgePacks} pack(s) de connaissances</div>
          )}
        </CreatedInfo>
        <Actions>
          <ActionButton variant="primary" onClick={onChatClick}>
            <span>💬</span>
            Chat
          </ActionButton>
          <ActionButton>
            <span>✏️</span>
            Modifier
          </ActionButton>
          <ActionButton variant="danger">
            <span>🗑️</span>
            Supprimer
          </ActionButton>
        </Actions>
      </Footer>
    </Card>
  );
};
