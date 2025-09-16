import { AgentTemplate } from '../types/agent';

export const agentTemplates: AgentTemplate[] = [
  {
    id: 'teaching',
    name: 'Professeur/Enseignant',
    category: 'Éducation',
    description: 'Agent spécialisé dans l\'enseignement et l\'éducation',
    defaultPrompt: 'Tu es un professeur expérimenté et bienveillant. Tu es là pour aider les étudiants dans leur apprentissage avec patience et expertise.',
    defaultModel: 'llama3.2:1b',
    defaultAvatar: '👨‍🏫',
    defaultColor: '#3b82f6',
    suggestedKnowledgeBase: 'pfeq',
    fields: [
      { name: 'name', type: 'text', label: 'Nom de l\'agent', placeholder: 'Ex: Professeur de Mathématiques', required: true },
      { name: 'specialty', type: 'text', label: 'Spécialité', placeholder: 'Ex: Mathématiques, Physique, Français', required: true },
      { name: 'description', type: 'textarea', label: 'Description', placeholder: 'Description de l\'agent et de son expertise', required: true },
      { name: 'prompt', type: 'textarea', label: 'Prompt personnalisé', placeholder: 'Instructions spécifiques pour l\'agent', required: false },
      { name: 'knowledgeBase', type: 'select', label: 'Base de connaissances', options: ['pfeq', 'formeduc', 'custom'], required: true }
    ]
  },
  {
    id: 'technical_support',
    name: 'Support Technique',
    category: 'Technique',
    description: 'Agent spécialisé dans le support technique et la résolution de problèmes',
    defaultPrompt: 'Tu es un expert en support technique. Tu aides les utilisateurs à résoudre leurs problèmes techniques avec clarté et efficacité.',
    defaultModel: 'llama3.2:1b',
    defaultAvatar: '🔧',
    defaultColor: '#10b981',
    suggestedKnowledgeBase: 'technical',
    fields: [
      { name: 'name', type: 'text', label: 'Nom de l\'agent', placeholder: 'Ex: Assistant Technique', required: true },
      { name: 'specialty', type: 'text', label: 'Spécialité', placeholder: 'Ex: Informatique, Réseaux, Logiciels', required: true },
      { name: 'description', type: 'textarea', label: 'Description', placeholder: 'Description de l\'expertise technique', required: true },
      { name: 'prompt', type: 'textarea', label: 'Prompt personnalisé', placeholder: 'Instructions spécifiques pour l\'agent', required: false },
      { name: 'knowledgeBase', type: 'select', label: 'Base de connaissances', options: ['technical', 'software', 'hardware', 'custom'], required: true }
    ]
  },
  {
    id: 'administrative',
    name: 'Assistant Administratif',
    category: 'Administration',
    description: 'Agent spécialisé dans les tâches administratives et la gestion',
    defaultPrompt: 'Tu es un assistant administratif professionnel. Tu aides avec les procédures, la documentation et l\'organisation.',
    defaultModel: 'llama3.2:1b',
    defaultAvatar: '📋',
    defaultColor: '#8b5cf6',
    suggestedKnowledgeBase: 'administrative',
    fields: [
      { name: 'name', type: 'text', label: 'Nom de l\'agent', placeholder: 'Ex: Assistant RH', required: true },
      { name: 'specialty', type: 'text', label: 'Spécialité', placeholder: 'Ex: RH, Comptabilité, Gestion', required: true },
      { name: 'description', type: 'textarea', label: 'Description', placeholder: 'Description des compétences administratives', required: true },
      { name: 'prompt', type: 'textarea', label: 'Prompt personnalisé', placeholder: 'Instructions spécifiques pour l\'agent', required: false },
      { name: 'knowledgeBase', type: 'select', label: 'Base de connaissances', options: ['administrative', 'hr', 'legal', 'custom'], required: true }
    ]
  },
  {
    id: 'customer_service',
    name: 'Service Client',
    category: 'Commercial',
    description: 'Agent spécialisé dans le service client et la relation client',
    defaultPrompt: 'Tu es un agent de service client professionnel et empathique. Tu aides les clients avec bienveillance et efficacité.',
    defaultModel: 'llama3.2:1b',
    defaultAvatar: '🎧',
    defaultColor: '#f59e0b',
    suggestedKnowledgeBase: 'customer_service',
    fields: [
      { name: 'name', type: 'text', label: 'Nom de l\'agent', placeholder: 'Ex: Conseiller Client', required: true },
      { name: 'specialty', type: 'text', label: 'Spécialité', placeholder: 'Ex: Ventes, Support, Relations', required: true },
      { name: 'description', type: 'textarea', label: 'Description', placeholder: 'Description des compétences en service client', required: true },
      { name: 'prompt', type: 'textarea', label: 'Prompt personnalisé', placeholder: 'Instructions spécifiques pour l\'agent', required: false },
      { name: 'knowledgeBase', type: 'select', label: 'Base de connaissances', options: ['customer_service', 'products', 'policies', 'custom'], required: true }
    ]
  },
  {
    id: 'custom',
    name: 'Agent Personnalisé',
    category: 'Personnalisé',
    description: 'Créer un agent entièrement personnalisé',
    defaultPrompt: 'Tu es un assistant intelligent et utile. Tu adaptes ton aide selon les besoins de l\'utilisateur.',
    defaultModel: 'llama3.2:1b',
    defaultAvatar: '🤖',
    defaultColor: '#6b7280',
    suggestedKnowledgeBase: 'custom',
    fields: [
      { name: 'name', type: 'text', label: 'Nom de l\'agent', placeholder: 'Ex: Mon Assistant', required: true },
      { name: 'role', type: 'text', label: 'Rôle', placeholder: 'Ex: Assistant Personnel', required: true },
      { name: 'specialty', type: 'text', label: 'Spécialité', placeholder: 'Ex: Organisation, Recherche, Créativité', required: true },
      { name: 'description', type: 'textarea', label: 'Description', placeholder: 'Description complète de l\'agent', required: true },
      { name: 'prompt', type: 'textarea', label: 'Prompt personnalisé', placeholder: 'Instructions détaillées pour l\'agent', required: true },
      { name: 'model', type: 'select', label: 'Modèle IA', options: ['llama3.2:1b', 'llama3.2:3b', 'llama3.2:7b'], required: true },
      { name: 'knowledgeBase', type: 'select', label: 'Base de connaissances', options: ['pfeq', 'formeduc', 'technical', 'administrative', 'customer_service', 'custom'], required: true }
    ]
  }
];

export const getTemplateById = (id: string): AgentTemplate | undefined => {
  return agentTemplates.find(template => template.id === id);
};

export const getTemplatesByCategory = (category: string): AgentTemplate[] => {
  return agentTemplates.filter(template => template.category === category);
};

export const getCategories = (): string[] => {
  return Array.from(new Set(agentTemplates.map(template => template.category)));
};
