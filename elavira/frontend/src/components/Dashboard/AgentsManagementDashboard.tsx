import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { useApp } from '../../context/AppContext';
import { AgentType } from '../../types';
import SimpleAgentCreator from '../AgentCreator/SimpleAgentCreator';

const DashboardContainer = styled.div`
  min-height: 100vh;
  background: #ffffff;
  padding: 24px;
`;

const DashboardHeader = styled.div`
  margin-bottom: 32px;
`;

const DashboardTitle = styled.h1`
  font-size: 32px;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 8px 0;
`;

const DashboardSubtitle = styled.p`
  font-size: 16px;
  color: #6b7280;
  margin: 0;
`;

const DashboardActions = styled.div`
  display: flex;
  justify-content: flex-end;
  margin-bottom: 32px;
`;

const AddAgentButton = styled.button`
  background: #3b82f6;
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
    background: #2563eb;
    transform: translateY(-1px);
  }
`;

const AgentsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 24px;
`;

const AgentCard = styled.div`
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
  transition: all 0.2s ease;

  &:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    transform: translateY(-2px);
  }
`;

const AgentHeader = styled.div`
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
`;

const AgentIcon = styled.div`
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: linear-gradient(135deg, #8b5cf6 0%, #a855f7 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 24px;
  overflow: hidden;
`;

const AgentIconImage = styled.img`
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 12px;
`;

const AgentInfo = styled.div`
  flex: 1;
`;

const AgentName = styled.h3`
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 4px 0;
`;

const AgentRole = styled.p`
  font-size: 14px;
  color: #6b7280;
  margin: 0;
  font-weight: 500;
`;

const AgentDescription = styled.p`
  font-size: 14px;
  color: #4b5563;
  line-height: 1.5;
  margin: 0 0 16px 0;
`;

const CapabilitiesContainer = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 16px;
`;

const CapabilityTag = styled.span`
  background: #f1f5f9;
  color: #475569;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
  border: 1px solid #e2e8f0;
`;

const AgentFooter = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
`;

const CreationDate = styled.span`
  font-size: 12px;
  color: #6b7280;
`;

const KnowledgePacks = styled.span`
  font-size: 12px;
  color: #6b7280;
`;

const AgentActions = styled.div`
  display: flex;
  gap: 8px;
`;

const ActionButton = styled.button<{ variant: 'primary' | 'secondary' | 'danger' }>`
  flex: 1;
  padding: 8px 12px;
  border: none;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  
  ${props => {
    switch (props.variant) {
      case 'primary':
        return `
          background: #3b82f6;
          color: white;
          &:hover {
            background: #2563eb;
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


export const AgentsManagementDashboard: React.FC = () => {
  const { dispatch } = useApp();
  const [selectedAgent, setSelectedAgent] = useState<string | null>(null);
  const [isCreatorOpen, setIsCreatorOpen] = useState(false);
  
  // Agents par défaut
  const defaultAgents = [
    {
      id: 'elavira',
      name: 'Elavira',
      role: 'Spécialiste Formeduc',
      description: 'Spécialiste des formations professionnelles Formeduc : secourisme, premiers soins, SST et formations en entreprise.',
      capabilities: ['Formations professionnelles', 'Secourisme', 'Premiers soins', 'SST', 'Formations entreprise'],
      status: 'Active',
      createdAt: '2025-09-14',
      knowledgePacks: 3
    },
    {
      id: 'solenys',
      name: 'Solenys',
      role: 'Professeur québécois',
      description: 'Professeur spécialisé dans l\'enseignement secondaire selon le programme PFEQ du Québec.',
      capabilities: ['Mathématiques', 'Sciences', 'Français', 'Programme PFEQ', 'Enseignement secondaire'],
      status: 'Active',
      createdAt: '2025-09-14',
      knowledgePacks: 2
    }
  ];

  // État pour les agents (par défaut + créés dynamiquement)
  const [agents, setAgents] = useState<any[]>(defaultAgents);
  const [loading, setLoading] = useState(false);

  // Charger les agents depuis l'API au montage du composant
  useEffect(() => {
    loadAgents();
  }, []);

  const loadAgents = async () => {
    try {
      setLoading(true);
      // Charger les agents créés depuis l'API
      const response = await fetch('http://104.254.182.118:8000/api/agents/');
      if (response.ok) {
        const createdAgents = await response.json();
        // Combiner les agents par défaut avec les agents créés
        setAgents([...defaultAgents, ...createdAgents]);
      }
    } catch (error) {
      console.error('Erreur lors du chargement des agents:', error);
      // En cas d'erreur, garder seulement les agents par défaut
      setAgents(defaultAgents);
    } finally {
      setLoading(false);
    }
  };

  const handleAgentSelect = (agentId: string) => {
    dispatch({ type: 'SET_SELECTED_AGENT', payload: agentId as AgentType });
    dispatch({ type: 'SET_PAGE', payload: 'chat' });
  };

  const handleEditAgent = (agentId: string) => {
    // TODO: Ouvrir modal d'édition
    console.log('Éditer agent:', agentId);
  };

  const handleDeleteAgent = (agentId: string) => {
    // TODO: Confirmer suppression
    console.log('Supprimer agent:', agentId);
  };

  const handleAgentCreated = (newAgent: any) => {
    // Recharger tous les agents depuis l'API
    loadAgents();
    console.log('Nouvel agent créé:', newAgent);
  };

  return (
    <DashboardContainer>
      <DashboardHeader>
        <DashboardTitle>Agents</DashboardTitle>
        <DashboardSubtitle>Gérez vos agents IA spécialisés</DashboardSubtitle>
      </DashboardHeader>

      <DashboardActions>
        <AddAgentButton onClick={() => {
          alert('Bouton principal cliqué !'); // Test du bouton principal
          console.log('Bouton cliqué, ouverture du modal...');
          setIsCreatorOpen(true);
        }}>
          <span>+</span>
          Créer un agent
        </AddAgentButton>
      </DashboardActions>


      <AgentsGrid>
        {Array.isArray(agents) ? agents.map((agent) => (
          <AgentCard
            key={agent.id}
            onClick={() => handleAgentSelect(agent.id)}
          >
            <AgentHeader>
              <AgentIcon>
                {agent.id === 'solenys' ? (
                  <AgentIconImage 
                    src="/avatars/solenys.svg" 
                    alt="Solenys"
                    onError={(e) => {
                      // Fallback vers l'emoji si l'image ne charge pas
                      const target = e.target as HTMLImageElement;
                      target.style.display = 'none';
                      const parent = target.parentElement;
                      if (parent) {
                        parent.innerHTML = '👨‍🏫';
                      }
                    }}
                  />
                ) : agent.id === 'elavira' ? '🎓' : '🤖'}
              </AgentIcon>
              <AgentInfo>
                <AgentName>{agent.name}</AgentName>
                <AgentRole>{agent.role}</AgentRole>
              </AgentInfo>
            </AgentHeader>

            <AgentDescription>{agent.description}</AgentDescription>

            <CapabilitiesContainer>
              {agent.capabilities.map((capability: string, index: number) => (
                <CapabilityTag key={index}>{capability}</CapabilityTag>
              ))}
            </CapabilitiesContainer>

            <AgentFooter>
              <CreationDate>Créé le {agent.createdAt}</CreationDate>
              {agent.knowledgePacks > 0 && (
                <KnowledgePacks>{agent.knowledgePacks} pack(s) de connaissances</KnowledgePacks>
              )}
            </AgentFooter>

            <AgentActions>
              <ActionButton 
                variant="primary" 
                onClick={(e) => {
                  e.stopPropagation();
                  handleAgentSelect(agent.id);
                }}
              >
                Chat
              </ActionButton>
              <ActionButton 
                variant="secondary"
                onClick={(e) => {
                  e.stopPropagation();
                  handleEditAgent(agent.id);
                }}
              >
                Modifier
              </ActionButton>
              <ActionButton 
                variant="danger"
                onClick={(e) => {
                  e.stopPropagation();
                  handleDeleteAgent(agent.id);
                }}
              >
                Supprimer
              </ActionButton>
            </AgentActions>
          </AgentCard>
        )) : null}
      </AgentsGrid>

      <SimpleAgentCreator
        isOpen={isCreatorOpen}
        onClose={() => {
          console.log('Fermeture du modal...');
          setIsCreatorOpen(false);
        }}
        onAgentCreated={handleAgentCreated}
      />
    </DashboardContainer>
  );
};
