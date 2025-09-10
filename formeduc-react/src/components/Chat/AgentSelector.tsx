import React from 'react';
import styled from 'styled-components';
import { useApp } from '../../context/AppContext';
import { AgentType } from '../../types';

const SelectorContainer = styled.div`
  display: flex;
  align-items: center;
  gap: 10px;
`;

const Label = styled.label`
  font-weight: 600;
  color: #34495e;
  font-size: 0.9rem;
`;

const Select = styled.select`
  padding: 8px 15px;
  border: 2px solid #e1e8ed;
  border-radius: 20px;
  background: white;
  font-size: 0.9rem;
  color: #2c3e50;
  cursor: pointer;
  transition: all 0.3s ease;

  &:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }

  &:hover {
    border-color: #3b82f6;
  }
`;

const Option = styled.option`
  padding: 10px;
`;

const AgentInfo = styled.div`
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 5px 12px;
  background: #f8f9fa;
  border-radius: 15px;
  font-size: 0.8rem;
  color: #6c757d;
`;

const AgentIcon = styled.span`
  font-size: 1rem;
`;

const agentOptions = [
  { value: 'agent-001', label: 'Elavira', icon: '👩‍🏫', description: 'Formations & Secourisme' },
  { value: 'agent-002', label: 'Solenys', icon: '🤖', description: 'Assistant IA' },
];

export const AgentSelector: React.FC = () => {
  const { state, dispatch } = useApp();

  const handleAgentChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const newAgentId = e.target.value as AgentType;
    if (newAgentId !== state.selected_agent_id) {
      dispatch({ type: 'SET_SELECTED_AGENT', payload: newAgentId });
      dispatch({ type: 'SET_MESSAGES', payload: [] });
      dispatch({ type: 'SET_LAST_SUGGESTED_PROMPTS', payload: [] });
      dispatch({ type: 'SET_DISPLAY_SUGGESTIONS', payload: false });
    }
  };

  const currentAgent = agentOptions.find(agent => agent.value === state.selected_agent_id);

  return (
    <SelectorContainer>
      <Label htmlFor="agent-selector">Assistant :</Label>
      <Select
        id="agent-selector"
        value={state.selected_agent_id}
        onChange={handleAgentChange}
      >
        {agentOptions.map((agent) => (
          <Option key={agent.value} value={agent.value}>
            {agent.icon} {agent.label}
          </Option>
        ))}
      </Select>
      
      {currentAgent && (
        <AgentInfo>
          <AgentIcon>{currentAgent.icon}</AgentIcon>
          <span>{currentAgent.description}</span>
        </AgentInfo>
      )}
    </SelectorContainer>
  );
};

