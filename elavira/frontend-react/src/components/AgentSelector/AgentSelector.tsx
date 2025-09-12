import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';

const SelectorContainer = styled.div`
  display: flex;
  gap: 20px;
  justify-content: center;
  margin-bottom: 30px;
`;

const AgentButton = styled(motion.button)<{ $isSelected: boolean }>`
  padding: 15px 30px;
  border: 2px solid ${props => props.$isSelected ? '#2ed573' : 'rgba(255, 255, 255, 0.3)'};
  border-radius: 25px;
  background: ${props => props.$isSelected ? 'rgba(46, 213, 115, 0.2)' : 'rgba(255, 255, 255, 0.1)'};
  color: white;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  
  &:hover {
    background: ${props => props.$isSelected ? 'rgba(46, 213, 115, 0.3)' : 'rgba(255, 255, 255, 0.2)'};
    transform: translateY(-2px);
  }
`;

const AgentInfo = styled.div`
  text-align: center;
  margin-top: 10px;
`;

const AgentName = styled.h3`
  color: white;
  margin: 0 0 5px 0;
  font-size: 18px;
`;

const AgentDescription = styled.p`
  color: rgba(255, 255, 255, 0.8);
  margin: 0;
  font-size: 14px;
`;

interface AgentSelectorProps {
  selectedAgent: 'elavira' | 'solenys';
  onAgentChange: (agent: 'elavira' | 'solenys') => void;
}

const AgentSelector: React.FC<AgentSelectorProps> = ({ selectedAgent, onAgentChange }) => {
  const agents = [
    {
      id: 'elavira' as const,
      name: 'Elavira',
      emoji: '🏥',
      description: 'Spécialiste secourisme Formeduc'
    },
    {
      id: 'solenys' as const,
      name: 'Solenys',
      emoji: '🎓',
      description: 'Professeur PFEQ Québec'
    }
  ];

  return (
    <SelectorContainer>
      {agents.map((agent) => (
        <AgentButton
          key={agent.id}
          $isSelected={selectedAgent === agent.id}
          onClick={() => onAgentChange(agent.id)}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <div>
            <div style={{ fontSize: '24px', marginBottom: '5px' }}>
              {agent.emoji}
            </div>
            <AgentName>{agent.name}</AgentName>
            <AgentDescription>{agent.description}</AgentDescription>
          </div>
        </AgentButton>
      ))}
    </SelectorContainer>
  );
};

export default AgentSelector;
