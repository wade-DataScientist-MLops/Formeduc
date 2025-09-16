import React, { useState } from 'react';
import styled from 'styled-components';
import { Agent, UpdateAgentRequest } from '../../types/agent';

const Card = styled.div<{ selected: boolean; isActive: boolean }>`
  background: white;
  border: 2px solid ${props => props.selected ? '#3b82f6' : '#e1e8ed'};
  border-radius: 15px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  opacity: ${props => props.isActive ? 1 : 0.6};
  position: relative;

  &:hover {
    border-color: #3b82f6;
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  }
`;

const CardHeader = styled.div`
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 15px;
`;

const Avatar = styled.div<{ color: string }>`
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: ${props => props.color};
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: white;
  flex-shrink: 0;
`;

const AgentInfo = styled.div`
  flex: 1;
  min-width: 0;
`;

const AgentName = styled.h3`
  color: #2c3e50;
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0 0 5px 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
`;

const AgentRole = styled.p`
  color: #6c757d;
  font-size: 0.9rem;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
`;

const StatusBadge = styled.div<{ isActive: boolean }>`
  position: absolute;
  top: 15px;
  right: 15px;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  background: ${props => props.isActive ? '#10b981' : '#ef4444'};
  color: white;
`;

const CardBody = styled.div`
  margin-bottom: 15px;
`;

const Specialty = styled.div`
  color: #3b82f6;
  font-size: 0.85rem;
  font-weight: 600;
  margin-bottom: 10px;
  padding: 4px 8px;
  background: #f0f8ff;
  border-radius: 8px;
  display: inline-block;
`;

const Description = styled.p`
  color: #495057;
  font-size: 0.9rem;
  line-height: 1.4;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
`;

const CardFooter = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 15px;
  border-top: 1px solid #e1e8ed;
`;

const ModelInfo = styled.div`
  color: #6c757d;
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  gap: 5px;
`;

const Actions = styled.div`
  display: flex;
  gap: 8px;
`;

const ActionButton = styled.button<{ variant: 'edit' | 'delete' | 'toggle' }>`
  padding: 6px 10px;
  border: none;
  border-radius: 6px;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.3s ease;

  ${props => {
    switch (props.variant) {
      case 'edit':
        return `
          background: #f8f9fa;
          color: #6c757d;
          border: 1px solid #e1e8ed;
          
          &:hover {
            background: #e9ecef;
            color: #2c3e50;
          }
        `;
      case 'delete':
        return `
          background: #fef2f2;
          color: #ef4444;
          border: 1px solid #fecaca;
          
          &:hover {
            background: #fee2e2;
          }
        `;
      case 'toggle':
        return `
          background: #f0f8ff;
          color: #3b82f6;
          border: 1px solid #b3d9ff;
          
          &:hover {
            background: #e1f0ff;
          }
        `;
    }
  }}
`;

const DropdownMenu = styled.div<{ isOpen: boolean }>`
  position: absolute;
  top: 100%;
  right: 0;
  background: white;
  border: 1px solid #e1e8ed;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  z-index: 10;
  display: ${props => props.isOpen ? 'block' : 'none'};
  min-width: 120px;
`;

const DropdownItem = styled.button`
  width: 100%;
  padding: 8px 12px;
  border: none;
  background: none;
  text-align: left;
  cursor: pointer;
  font-size: 0.85rem;
  color: #2c3e50;
  transition: background 0.2s ease;

  &:hover {
    background: #f8f9fa;
  }

  &:first-child {
    border-radius: 8px 8px 0 0;
  }

  &:last-child {
    border-radius: 0 0 8px 8px;
  }
`;

interface AgentCardProps {
  agent: Agent;
  isSelected: boolean;
  onSelect: () => void;
  onUpdate: (agent: UpdateAgentRequest) => void;
  onDelete: (agentId: string) => void;
  onToggleActive: (agentId: string) => void;
  onChatClick?: () => void;
}

export const AgentCard: React.FC<AgentCardProps> = ({
  agent,
  isSelected,
  onSelect,
  onUpdate,
  onDelete,
  onToggleActive,
  onChatClick
}) => {
  const [showDropdown, setShowDropdown] = useState(false);

  const handleEdit = () => {
    // TODO: Ouvrir le formulaire d'édition
    setShowDropdown(false);
  };

  const handleDelete = () => {
    onDelete(agent.id);
    setShowDropdown(false);
  };

  const handleToggle = () => {
    onToggleActive(agent.id);
    setShowDropdown(false);
  };

  return (
    <Card 
      selected={isSelected} 
      isActive={agent.isActive}
      onClick={onSelect}
    >
      <StatusBadge isActive={agent.isActive}>
        {agent.isActive ? 'Actif' : 'Inactif'}
      </StatusBadge>

      <CardHeader>
        <Avatar color={agent.color}>
          {agent.avatar}
        </Avatar>
        <AgentInfo>
          <AgentName>{agent.name}</AgentName>
          <AgentRole>{agent.role}</AgentRole>
        </AgentInfo>
      </CardHeader>

      <CardBody>
        <Specialty>{agent.specialty}</Specialty>
        <Description>{agent.description}</Description>
      </CardBody>

      <CardFooter>
        <ModelInfo>
          <span>🤖</span>
          <span>{agent.model}</span>
        </ModelInfo>
        
        <Actions>
          <ActionButton
            variant="toggle"
            onClick={(e) => {
              e.stopPropagation();
              handleToggle();
            }}
          >
            {agent.isActive ? 'Désactiver' : 'Activer'}
          </ActionButton>
          
          <ActionButton
            variant="edit"
            onClick={(e) => {
              e.stopPropagation();
              setShowDropdown(!showDropdown);
            }}
          >
            ⋯
          </ActionButton>
        </Actions>

        <DropdownMenu isOpen={showDropdown}>
          <DropdownItem onClick={handleEdit}>
            ✏️ Modifier
          </DropdownItem>
          <DropdownItem onClick={handleDelete}>
            🗑️ Supprimer
          </DropdownItem>
        </DropdownMenu>
      </CardFooter>
    </Card>
  );
};