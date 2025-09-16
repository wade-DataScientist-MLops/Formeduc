import React from 'react';
import styled from 'styled-components';

const SelectorContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background: #f7f7f8;
  padding: 40px;
`;

const Title = styled.h1`
  font-size: 32px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 16px 0;
  text-align: center;
`;

const Subtitle = styled.p`
  font-size: 18px;
  color: #6b7280;
  margin: 0 0 48px 0;
  text-align: center;
  max-width: 600px;
`;

const AgentsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
  max-width: 800px;
  width: 100%;
`;

const AgentCard = styled.div<{ color: string }>`
  background: white;
  border-radius: 16px;
  padding: 32px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);

  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
    border-color: ${props => props.color};
  }
`;

const AgentAvatar = styled.div<{ color: string }>`
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: ${props => props.color};
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 36px;
  margin: 0 auto 20px auto;
  color: white;
  font-weight: bold;
`;

const AgentName = styled.h3`
  font-size: 24px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 12px 0;
`;

const AgentDescription = styled.p`
  font-size: 16px;
  color: #6b7280;
  margin: 0 0 20px 0;
  line-height: 1.5;
`;

const AgentFeatures = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
`;

const FeatureTag = styled.span`
  background: #f3f4f6;
  color: #374151;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
`;

const StartButton = styled.button<{ color: string }>`
  background: ${props => props.color};
  color: white;
  border: none;
  border-radius: 12px;
  padding: 12px 24px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  margin-top: 20px;

  &:hover {
    opacity: 0.9;
    transform: translateY(-1px);
  }
`;

interface Agent {
  id: string;
  name: string;
  description: string;
  avatar: string;
  color: string;
  features: string[];
}

const agents: Agent[] = [
  {
    id: 'elavira',
    name: 'Elavira',
    description: 'Votre éducatrice spécialisée en secourisme et formations Formeduc. Elle vous accompagne dans l\'apprentissage des gestes de premiers secours.',
    avatar: '👩‍🏫',
    color: '#88c0d0',
    features: ['Secourisme', 'PSC1', 'Formations', 'Premiers secours']
  },
  {
    id: 'solenys',
    name: 'Solenys',
    description: 'Professeur québécois spécialisé dans l\'enseignement secondaire selon le programme PFEQ. Il vous aide dans toutes les matières scolaires.',
    avatar: '🤖',
    color: '#f093fb',
    features: ['Mathématiques', 'Sciences', 'Français', 'PFEQ']
  }
];

interface AgentSelectorProps {
  onAgentSelect: (agentId: string) => void;
}

export const AgentSelector: React.FC<AgentSelectorProps> = ({ onAgentSelect }) => {
  return (
    <SelectorContainer>
      <Title>Choisissez votre assistant</Title>
      <Subtitle>
        Sélectionnez l'assistant qui correspond le mieux à vos besoins d'apprentissage
      </Subtitle>
      
      <AgentsGrid>
        {agents.map((agent) => (
          <AgentCard
            key={agent.id}
            color={agent.color}
            onClick={() => onAgentSelect(agent.id)}
          >
            <AgentAvatar color={agent.color}>
              {agent.avatar}
            </AgentAvatar>
            <AgentName>{agent.name}</AgentName>
            <AgentDescription>{agent.description}</AgentDescription>
            <AgentFeatures>
              {agent.features.map((feature, index) => (
                <FeatureTag key={index}>{feature}</FeatureTag>
              ))}
            </AgentFeatures>
            <StartButton color={agent.color}>
              Commencer à discuter
            </StartButton>
          </AgentCard>
        ))}
      </AgentsGrid>
    </SelectorContainer>
  );
};