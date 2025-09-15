import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { Agent, CreateAgentRequest, UpdateAgentRequest } from '../../types/agent';
import { AgentCreator } from './AgentCreator';
import { AgentCard } from './AgentCard';

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

  const loadAgents = async () => {
    try {
      setLoading(true);
      // TODO: Remplacer par l'appel API réel
      const response = await fetch('/api/agents');
      if (response.ok) {
        const agentsData = await response.json();
        setAgents(agentsData);
      } else {
        // Données par défaut pour le développement
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
      }
    } catch (error) {
      console.error('Erreur lors du chargement des agents:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateAgent = async (agentData: CreateAgentRequest) => {
    try {
      const newAgent: Agent = {
        ...agentData,
        id: `agent-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
        isActive: true,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      };

      // TODO: Remplacer par l'appel API réel
      const response = await fetch('/api/agents', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newAgent),
      });

      if (response.ok) {
        setAgents(prev => [...prev, newAgent]);
        setIsCreatorOpen(false);
      } else {
        throw new Error('Erreur lors de la création de l\'agent');
      }
    } catch (error) {
      console.error('Erreur lors de la création de l\'agent:', error);
      alert('Erreur lors de la création de l\'agent');
    }
  };

  const handleUpdateAgent = async (agentData: UpdateAgentRequest) => {
    try {
      // TODO: Remplacer par l'appel API réel
      const response = await fetch(`/api/agents/${agentData.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(agentData),
      });

      if (response.ok) {
        setAgents(prev => prev.map(agent => 
          agent.id === agentData.id 
            ? { ...agent, ...agentData, updatedAt: new Date().toISOString() }
            : agent
        ));
      } else {
        throw new Error('Erreur lors de la mise à jour de l\'agent');
      }
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
      // TODO: Remplacer par l'appel API réel
      const response = await fetch(`/api/agents/${agentId}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        setAgents(prev => prev.filter(agent => agent.id !== agentId));
      } else {
        throw new Error('Erreur lors de la suppression de l\'agent');
      }
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
