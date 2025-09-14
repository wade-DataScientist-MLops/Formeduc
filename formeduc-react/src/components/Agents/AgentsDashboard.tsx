import React from 'react';
import styled from 'styled-components';
import { AgentCard, Agent } from './AgentCard';
import { useApp } from '../../context/AppContext';
import { AgentType } from '../../types';

const PageContainer = styled.div`
  background: #ffffff;
  min-height: calc(100vh - 64px);
`;

const PageHeader = styled.div`
  margin-bottom: 32px;
`;

const PageTitle = styled.h1`
  font-size: 32px;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 8px 0;
`;

const PageSubtitle = styled.p`
  font-size: 16px;
  color: #6b7280;
  margin: 0;
`;

const HeaderActions = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
`;

const AddAgentButton = styled.button`
  background: #667eea;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 8px;

  &:hover {
    background: #5a67d8;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
  }
`;

const AgentsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 24px;
`;

const agents: Agent[] = [
  {
    id: 'elavira',
    name: 'Elavira',
    avatar: '/images/elavira-real.png',
    description: 'Votre éducatrice spécialisée en secourisme et formations Formeduc.',
    capabilities: ['Formeduc Content', 'Secourisme', 'Pédagogie', 'Support'],
    status: 'Active',
    createdAt: '2024-09-01',
    knowledgePacks: 3
  },
  {
    id: 'solenys',
    name: 'Solenys',
    avatar: '/images/solenys-banner.svg',
    description: 'Professeur académique pour les élèves du secondaire (PFEQ Québec).',
    capabilities: ['PFEQ Curriculum', 'Mathématiques', 'Sciences', 'Français'],
    status: 'Active',
    createdAt: '2024-09-05',
    knowledgePacks: 2
  }
];

export const AgentsDashboard: React.FC = () => {
  const { dispatch } = useApp();

  const handleChatClick = (agentId: string) => {
    dispatch({ type: 'SET_SELECTED_AGENT', payload: agentId as AgentType });
    dispatch({ type: 'SET_PAGE', payload: 'chat' });
  };

  return (
    <PageContainer>
      <PageHeader>
        <PageTitle>Agents</PageTitle>
        <PageSubtitle>Gérez vos agents IA spécialisés</PageSubtitle>
      </PageHeader>

      <HeaderActions>
        <div />
        <AddAgentButton>
          <span>+</span>
          Nouvel agent
        </AddAgentButton>
      </HeaderActions>

      <AgentsGrid>
        {agents.map((agent) => (
          <AgentCard
            key={agent.id}
            agent={agent}
            onChatClick={() => handleChatClick(agent.id)}
          />
        ))}
      </AgentsGrid>
    </PageContainer>
  );
};