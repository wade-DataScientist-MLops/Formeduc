import React, { useState } from 'react';
import styled from 'styled-components';
import { useApp } from '../../context/AppContext';
import { AgentType } from '../../types';

const DashboardContainer = styled.div`
  min-height: 100vh;
  background: #f8fafc;
  padding: 30px;
`;

const DashboardHeader = styled.div`
  margin-bottom: 40px;
`;

const DashboardTitle = styled.h1`
  font-size: 36px;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 8px 0;
`;

const DashboardSubtitle = styled.p`
  font-size: 18px;
  color: #6b7280;
  margin: 0;
`;

const DashboardActions = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
`;

const SearchContainer = styled.div`
  position: relative;
  width: 400px;
`;

const SearchInput = styled.input`
  width: 100%;
  padding: 12px 16px 12px 44px;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  font-size: 14px;
  background: white;
  transition: all 0.2s ease;

  &:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }

  &::placeholder {
    color: #9ca3af;
  }
`;

const SearchIcon = styled.div`
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  color: #9ca3af;
  font-size: 16px;
`;

const AddAgentButton = styled.button`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 8px;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
  }
`;

const AgentsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 24px;
`;

const AgentCard = styled.div<{ isSelected?: boolean }>`
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 2px solid ${props => props.isSelected ? '#667eea' : '#e5e7eb'};
  transition: all 0.2s ease;
  cursor: pointer;
  position: relative;

  &:hover {
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    transform: translateY(-2px);
    border-color: #667eea;
  }
`;

const AgentHeader = styled.div`
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
`;

const AgentAvatar = styled.div<{ backgroundImage?: string }>`
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: ${props => props.backgroundImage ? `url(${props.backgroundImage})` : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'};
  background-size: cover;
  background-position: center;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 24px;
  font-weight: 700;
  border: 3px solid white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
`;

const AgentInfo = styled.div`
  flex: 1;
`;

const AgentName = styled.h3`
  font-size: 20px;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 4px 0;
`;

const AgentRole = styled.p`
  font-size: 14px;
  color: #6b7280;
  margin: 0;
  font-weight: 500;
`;

const AgentStatus = styled.div<{ status: string }>`
  position: absolute;
  top: 20px;
  right: 20px;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  background: ${props => props.status === 'Active' ? '#dcfce7' : '#fef3c7'};
  color: ${props => props.status === 'Active' ? '#166534' : '#92400e'};
`;

const AgentDescription = styled.p`
  font-size: 14px;
  color: #4b5563;
  line-height: 1.6;
  margin: 0 0 16px 0;
`;

const CapabilitiesContainer = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 20px;
`;

const CapabilityTag = styled.span`
  background: #f3f4f6;
  color: #374151;
  padding: 4px 8px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 500;
`;

const AgentStats = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 12px 0;
  border-top: 1px solid #e5e7eb;
  border-bottom: 1px solid #e5e7eb;
`;

const StatItem = styled.div`
  text-align: center;
`;

const StatValue = styled.div`
  font-size: 18px;
  font-weight: 700;
  color: #1f2937;
`;

const StatLabel = styled.div`
  font-size: 12px;
  color: #6b7280;
  font-weight: 500;
`;

const AgentActions = styled.div`
  display: flex;
  gap: 8px;
`;

const ActionButton = styled.button<{ variant: 'primary' | 'secondary' | 'danger' }>`
  flex: 1;
  padding: 10px 16px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  
  ${props => {
    switch (props.variant) {
      case 'primary':
        return `
          background: #667eea;
          color: white;
          &:hover {
            background: #5a67d8;
            transform: translateY(-1px);
          }
        `;
      case 'secondary':
        return `
          background: #f3f4f6;
          color: #374151;
          &:hover {
            background: #e5e7eb;
          }
        `;
      case 'danger':
        return `
          background: #fef2f2;
          color: #dc2626;
          &:hover {
            background: #fee2e2;
          }
        `;
    }
  }}
`;

const SelectedAgentInfo = styled.div`
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 2px solid #667eea;
  margin-bottom: 30px;
`;

const SelectedAgentTitle = styled.h3`
  font-size: 18px;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 16px 0;
  display: flex;
  align-items: center;
  gap: 8px;
`;

const StartChatButton = styled.button`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 16px 32px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0 auto;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
  }
`;

const agents = [
  {
    id: 'elavira',
    name: 'Elavira',
    role: 'Spécialiste Formeduc',
    description: 'Professionnelle de la santé et de l\'éducation, Elavira vous accompagne dans vos formations de secourisme avec expertise et vigilance.',
    capabilities: ['Formations certifiantes', 'Secourisme adapté', 'Prévention des risques', 'Accompagnement personnalisé'],
    status: 'Active',
    avatar: '/images/elavira-real.png',
    createdAt: '2024-09-01',
    knowledgePacks: 3,
    conversations: 127,
    rating: 4.8
  },
  {
    id: 'solenys',
    name: 'Solenys',
    role: 'Professeur Académique',
    description: 'Professeur québécois spécialisé dans l\'enseignement secondaire selon le programme PFEQ. Guide pédagogique pour mathématiques, sciences et français.',
    capabilities: ['PFEQ Curriculum', 'Mathématiques', 'Sciences', 'Français'],
    status: 'Active',
    avatar: '/images/solenys-banner.svg',
    createdAt: '2024-09-05',
    knowledgePacks: 2,
    conversations: 89,
    rating: 4.6
  }
];

export const AgentsManagementDashboard: React.FC = () => {
  const { dispatch } = useApp();
  const [selectedAgent, setSelectedAgent] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');

  const filteredAgents = agents.filter(agent =>
    agent.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    agent.role.toLowerCase().includes(searchQuery.toLowerCase()) ||
    agent.capabilities.some(cap => cap.toLowerCase().includes(searchQuery.toLowerCase()))
  );

  const handleAgentSelect = (agentId: string) => {
    setSelectedAgent(selectedAgent === agentId ? null : agentId);
  };

  const handleStartChat = () => {
    if (selectedAgent) {
      dispatch({ type: 'SET_SELECTED_AGENT', payload: selectedAgent as AgentType });
      dispatch({ type: 'SET_PAGE', payload: 'chat' });
    }
  };

  const handleEditAgent = (agentId: string) => {
    // TODO: Ouvrir modal d'édition
    console.log('Éditer agent:', agentId);
  };

  const handleDeleteAgent = (agentId: string) => {
    // TODO: Confirmer suppression
    console.log('Supprimer agent:', agentId);
  };

  return (
    <DashboardContainer>
      <DashboardHeader>
        <DashboardTitle>Gestion des Agents IA</DashboardTitle>
        <DashboardSubtitle>Gérez vos assistants intelligents et leurs configurations</DashboardSubtitle>
      </DashboardHeader>

      <DashboardActions>
        <SearchContainer>
          <SearchIcon>🔍</SearchIcon>
          <SearchInput
            type="text"
            placeholder="Rechercher un agent..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </SearchContainer>
        
        <AddAgentButton>
          <span>+</span>
          Nouvel Agent
        </AddAgentButton>
      </DashboardActions>

      {selectedAgent && (
        <SelectedAgentInfo>
          <SelectedAgentTitle>
            🎯 Agent sélectionné: {agents.find(a => a.id === selectedAgent)?.name}
          </SelectedAgentTitle>
          <StartChatButton onClick={handleStartChat}>
            <span>💬</span>
            Commencer la conversation
          </StartChatButton>
        </SelectedAgentInfo>
      )}

      <AgentsGrid>
        {filteredAgents.map((agent) => (
          <AgentCard
            key={agent.id}
            isSelected={selectedAgent === agent.id}
            onClick={() => handleAgentSelect(agent.id)}
          >
            <AgentStatus status={agent.status}>
              {agent.status}
            </AgentStatus>
            
            <AgentHeader>
              <AgentAvatar backgroundImage={agent.avatar}>
                {!agent.avatar && agent.name.charAt(0)}
              </AgentAvatar>
              <AgentInfo>
                <AgentName>{agent.name}</AgentName>
                <AgentRole>{agent.role}</AgentRole>
              </AgentInfo>
            </AgentHeader>

            <AgentDescription>{agent.description}</AgentDescription>

            <CapabilitiesContainer>
              {agent.capabilities.map((capability, index) => (
                <CapabilityTag key={index}>{capability}</CapabilityTag>
              ))}
            </CapabilitiesContainer>

            <AgentStats>
              <StatItem>
                <StatValue>{agent.knowledgePacks}</StatValue>
                <StatLabel>Bases de connaissances</StatLabel>
              </StatItem>
              <StatItem>
                <StatValue>{agent.conversations}</StatValue>
                <StatLabel>Conversations</StatLabel>
              </StatItem>
              <StatItem>
                <StatValue>{agent.rating}</StatValue>
                <StatLabel>Note</StatLabel>
              </StatItem>
            </AgentStats>

            <AgentActions>
              <ActionButton 
                variant="primary" 
                onClick={(e) => {
                  e.stopPropagation();
                  handleAgentSelect(agent.id);
                }}
              >
                💬 Chat
              </ActionButton>
              <ActionButton 
                variant="secondary"
                onClick={(e) => {
                  e.stopPropagation();
                  handleEditAgent(agent.id);
                }}
              >
                ✏️ Modifier
              </ActionButton>
              <ActionButton 
                variant="danger"
                onClick={(e) => {
                  e.stopPropagation();
                  handleDeleteAgent(agent.id);
                }}
              >
                🗑️ Supprimer
              </ActionButton>
            </AgentActions>
          </AgentCard>
        ))}
      </AgentsGrid>
    </DashboardContainer>
  );
};
