import React from 'react';
import styled from 'styled-components';
import { AgentCard } from './AgentCard';
import { useApp } from '../../context/AppContext';
import { AgentType } from '../../types';

const DashboardContainer = styled.div`
  display: flex;
  height: 100vh;
  background: #f8fafc;
`;

const Sidebar = styled.div`
  width: 250px;
  background: #1e293b;
  color: white;
  padding: 20px;
  display: flex;
  flex-direction: column;
`;

const Logo = styled.div`
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 30px;
  color: #3b82f6;
`;

const NavItem = styled.div<{ active?: boolean }>`
  padding: 12px 16px;
  margin: 4px 0;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 12px;
  background: ${props => props.active ? '#3b82f6' : 'transparent'};
  transition: background 0.2s;

  &:hover {
    background: ${props => props.active ? '#3b82f6' : '#334155'};
  }
`;

const MainContent = styled.div`
  flex: 1;
  padding: 30px;
  overflow-y: auto;
`;

const Header = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
`;

const Title = styled.h1`
  font-size: 2rem;
  color: #1e293b;
  margin: 0;
`;

const Subtitle = styled.p`
  color: #64748b;
  margin: 8px 0 0 0;
`;

const SearchBar = styled.input`
  padding: 12px 16px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  width: 300px;
  font-size: 14px;

  &:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }
`;

const NewAgentButton = styled.button`
  background: #3b82f6;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;

  &:hover {
    background: #2563eb;
  }
`;

const AgentsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 24px;
`;

const agents = [
  {
    id: 'elavira',
    name: 'Elavira',
    type: 'Assistant Formeduc',
    description: 'Spécialiste en formations de secourisme et éducation. Aide avec les programmes RSGE, PSC1, SST et formations en ligne.',
    capabilities: ['qwen2.5:7b', 'rag.search', 'rag.answer', 'voice.tts', 'voice.stt'],
    avatar: '/images/elavira-real.png',
    createdAt: '2024-09-12',
    knowledgePacks: 3
  },
  {
    id: 'solenys',
    name: 'Solenys',
    type: 'Professeur PFEQ',
    description: 'Professeur spécialisé dans le programme de secondaire du Québec (PFEQ). Aide avec les mathématiques, sciences et français.',
    capabilities: ['llama3.2:1b', 'rag.search', 'rag.answer', 'math.evaluate', 'voice.tts'],
    avatar: '/images/solenys-banner.svg',
    createdAt: '2024-09-12',
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
    <DashboardContainer>
      <Sidebar>
        <Logo>Elavira</Logo>
        <NavItem active>
          <span>📊</span>
          Dashboard
        </NavItem>
        <NavItem active>
          <span>🤖</span>
          Agents
        </NavItem>
        <NavItem>
          <span>💬</span>
          Chat
        </NavItem>
        <NavItem>
          <span>🔗</span>
          Multi-Agents
        </NavItem>
        <NavItem>
          <span>📚</span>
          Connaissances
        </NavItem>
        <NavItem>
          <span>📄</span>
          Workflows
        </NavItem>
        <NavItem>
          <span>📋</span>
          Logs
        </NavItem>
        <NavItem>
          <span>⚙️</span>
          Paramètres
        </NavItem>
      </Sidebar>

      <MainContent>
        <Header>
          <div>
            <Title>Agents</Title>
            <Subtitle>Gérez vos agents IA spécialisés</Subtitle>
          </div>
          <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
            <SearchBar placeholder="Rechercher..." />
            <NewAgentButton>
              <span>+</span>
              Nouvel agent
            </NewAgentButton>
          </div>
        </Header>

        <AgentsGrid>
          {agents.map(agent => (
            <AgentCard 
              key={agent.id} 
              agent={agent} 
              onChatClick={() => handleChatClick(agent.id)}
            />
          ))}
        </AgentsGrid>
      </MainContent>
    </DashboardContainer>
  );
};
