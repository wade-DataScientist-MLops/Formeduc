import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { Agent, CreateAgentRequest, UpdateAgentRequest } from '../../types/agent';
import { AgentCreator } from './AgentCreator';
import { AgentCard } from './AgentCard';
import { agentsAPI } from '../../services/api';

const Container = styled.div`
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
`;

const Header = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 2px solid #e1e8ed;
`;

const Title = styled.h1`
  color: #2c3e50;
  font-size: 2rem;
  font-weight: 600;
  margin: 0;
`;

const CreateButton = styled.button`
  padding: 12px 24px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;

  &:hover {
    background: #2e6bb4;
    transform: translateY(-1px);
  }
`;

const AgentsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
`;

const EmptyState = styled.div`
  text-align: center;
  padding: 60px 20px;
  color: #6c757d;
`;

const EmptyIcon = styled.div`
  font-size: 4rem;
  margin-bottom: 20px;
`;

const EmptyText = styled.p`
  font-size: 1.1rem;
  margin-bottom: 20px;
`;

const EmptyButton = styled.button`
  padding: 12px 24px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;

  &:hover {
    background: #2e6bb4;
    transform: translateY(-1px);
  }
`;

interface AgentManagerProps {
  onAgentSelect?: (agent: Agent) => void;
  selectedAgentId?: string;
}

export const AgentManager: React.FC<AgentManagerProps> = ({
  onAgentSelect,
  selectedAgentId
}) => {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [isCreatorOpen, setIsCreatorOpen] = useState(false);
  const [loading, setLoading] = useState(true);

  // Charger les agents depuis l'API
  useEffect(() => {
    loadAgents();
  }, []);

  // Fonction pour convertir les données du backend vers le frontend
  const convertBackendToFrontend = (backendAgent: any): Agent => ({
    id: backendAgent.id,
    name: backendAgent.name,
    role: backendAgent.role,
    specialty: backendAgent.specialty,
    description: backendAgent.description,
    prompt: backendAgent.prompt,
    model: backendAgent.model,
    avatar: backendAgent.avatar,
    color: backendAgent.color,
    knowledgeBase: backendAgent.knowledge_base,
    isActive: backendAgent.is_active,
    createdAt: backendAgent.created_at,
    updatedAt: backendAgent.updated_at
  });

  const loadAgents = async () => {
    try {
      setLoading(true);
      const agentsData = await agentsAPI.getAgents();
      const convertedAgents = agentsData.map(convertBackendToFrontend);
      setAgents(convertedAgents);
    } catch (error) {
      console.error('Erreur lors du chargement des agents:', error);
      // Données par défaut pour le développement en cas d'erreur
      setAgents([
        {
          id: 'agent-001',
          name: 'Elavira',
          role: 'Experte Formations',
          specialty: 'Formations & Secourisme',
          description: 'Professionnelle de la santé et de l\'éducation, Elavira vous accompagne dans vos formations de secourisme avec expertise et bienveillance.',
          prompt: 'Tu es Elavira, experte en formations de secourisme...',
          model: 'llama3.2:1b',
          avatar: '👩‍🏫',
          color: '#88c0d0',
          knowledgeBase: 'formeduc',
          isActive: true,
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString()
        },
        {
          id: 'agent-002',
          name: 'Solenys',
          role: 'Professeur Québécois',
          specialty: 'Enseignement PFEQ',
          description: 'Professeur spécialisé dans l\'enseignement secondaire selon le programme PFEQ du Québec.',
          prompt: 'Tu es Solenys, professeur québécois...',
          model: 'llama3.2:1b',
          avatar: '🤖',
          color: '#f093fb',
          knowledgeBase: 'pfeq',
          isActive: true,
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString()
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateAgent = async (agentData: CreateAgentRequest) => {
    try {
      // Convertir les noms de champs du frontend vers le backend
      const backendData = {
        name: agentData.name,
        role: agentData.role,
        specialty: agentData.specialty,
        description: agentData.description,
        prompt: agentData.prompt,
        model: agentData.model,
        avatar: agentData.avatar,
        color: agentData.color,
        knowledge_base: agentData.knowledgeBase
      };
      
      const createdAgent = await agentsAPI.createAgent(backendData);
      const convertedAgent = convertBackendToFrontend(createdAgent);
      setAgents(prev => [...prev, convertedAgent]);
      setIsCreatorOpen(false);
    } catch (error) {
      console.error('Erreur lors de la création de l\'agent:', error);
      alert('Erreur lors de la création de l\'agent');
    }
  };

  const handleUpdateAgent = async (agentData: UpdateAgentRequest) => {
    try {
      // Convertir les noms de champs du frontend vers le backend
      const backendData: any = {};
      if (agentData.name) backendData.name = agentData.name;
      if (agentData.role) backendData.role = agentData.role;
      if (agentData.specialty) backendData.specialty = agentData.specialty;
      if (agentData.description) backendData.description = agentData.description;
      if (agentData.prompt) backendData.prompt = agentData.prompt;
      if (agentData.model) backendData.model = agentData.model;
      if (agentData.avatar) backendData.avatar = agentData.avatar;
      if (agentData.color) backendData.color = agentData.color;
      if (agentData.knowledgeBase) backendData.knowledge_base = agentData.knowledgeBase;
      if (agentData.isActive !== undefined) backendData.is_active = agentData.isActive;
      
      const updatedAgent = await agentsAPI.updateAgent(agentData.id, backendData);
      const convertedAgent = convertBackendToFrontend(updatedAgent);
      setAgents(prev => prev.map(agent => 
        agent.id === agentData.id ? convertedAgent : agent
      ));
    } catch (error) {
      console.error('Erreur lors de la mise à jour de l\'agent:', error);
      alert('Erreur lors de la mise à jour de l\'agent');
    }
  };

  const handleDeleteAgent = async (agentId: string) => {
    if (!confirm('Êtes-vous sûr de vouloir supprimer cet agent ?')) {
      return;
    }

    try {
      await agentsAPI.deleteAgent(agentId);
      setAgents(prev => prev.filter(agent => agent.id !== agentId));
    } catch (error) {
      console.error('Erreur lors de la suppression de l\'agent:', error);
      alert('Erreur lors de la suppression de l\'agent');
    }
  };

  const handleToggleActive = async (agentId: string) => {
    const agent = agents.find(a => a.id === agentId);
    if (!agent) return;

    await handleUpdateAgent({
      id: agentId,
      isActive: !agent.isActive
    });
  };

  if (loading) {
    return (
      <Container>
        <div style={{ textAlign: 'center', padding: '60px 20px' }}>
          <div style={{ fontSize: '2rem', marginBottom: '20px' }}>⏳</div>
          <p>Chargement des agents...</p>
        </div>
      </Container>
    );
  }

  return (
    <Container>
      <Header>
        <Title>Gestion des Agents</Title>
        <CreateButton onClick={() => setIsCreatorOpen(true)}>
          + Créer un agent
        </CreateButton>
      </Header>

      {agents.length === 0 ? (
        <EmptyState>
          <EmptyIcon>🤖</EmptyIcon>
          <EmptyText>Aucun agent créé pour le moment</EmptyText>
          <EmptyButton onClick={() => setIsCreatorOpen(true)}>
            Créer votre premier agent
          </EmptyButton>
        </EmptyState>
      ) : (
        <AgentsGrid>
          {agents.map(agent => (
            <AgentCard
              key={agent.id}
              agent={agent}
              isSelected={selectedAgentId === agent.id}
              onSelect={() => onAgentSelect?.(agent)}
              onUpdate={handleUpdateAgent}
              onDelete={handleDeleteAgent}
              onToggleActive={handleToggleActive}
            />
          ))}
        </AgentsGrid>
      )}

      <AgentCreator
        isOpen={isCreatorOpen}
        onClose={() => setIsCreatorOpen(false)}
        onSave={handleCreateAgent}
        existingAgents={agents}
      />
    </Container>
  );
};
