import React from 'react';
import { useApp } from '../../context/AppContext';
import { ElaviraChatInterface } from './ElaviraChatInterface';
import { SolenysChatInterface } from './SolenysChatInterface';
import { GenericAgentChatInterface } from './GenericAgentChatInterface';

export const AgentChatRouter: React.FC = () => {
  const { state } = useApp();
  const { selected_agent_id } = state;

  // Agents prédéfinis avec leurs interfaces spécialisées
  if (selected_agent_id === 'elavira') {
    return <ElaviraChatInterface />;
  }

  if (selected_agent_id === 'solenys') {
    return <SolenysChatInterface />;
  }

  // Pour les agents créés dynamiquement, utiliser l'interface générique
  // Récupérer les informations de l'agent depuis le contexte ou l'API
  const agentInfo = getAgentInfo(selected_agent_id);

  return (
    <GenericAgentChatInterface
      agentId={selected_agent_id}
      agentName={agentInfo.name}
      agentRole={agentInfo.role}
      agentDescription={agentInfo.description}
    />
  );
};

// Fonction pour récupérer les informations de l'agent
const getAgentInfo = (agentId: string) => {
  // Par défaut, retourner des informations génériques
  const defaultInfo = {
    name: 'Assistant IA',
    role: 'Assistant intelligent',
    description: 'Votre assistant personnel pour vous aider dans vos tâches.'
  };

  // Si c'est un agent créé, on pourrait récupérer ses informations depuis l'API
  // Pour l'instant, on retourne les informations par défaut
  if (agentId.startsWith('agent_')) {
    return {
      name: agentId.replace('agent_', '').replace(/_/g, ' '),
      role: 'Assistant personnalisé',
      description: 'Un assistant créé spécialement pour vous.'
    };
  }

  return defaultInfo;
};
