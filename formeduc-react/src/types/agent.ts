export interface Agent {
  id: string;
  name: string;
  role: string;
  specialty: string;
  description: string;
  prompt: string;
  model: string;
  avatar: string;
  color: string;
  knowledgeBase: string;
  isActive: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface AgentTemplate {
  id: string;
  name: string;
  category: string;
  description: string;
  defaultPrompt: string;
  defaultModel: string;
  defaultAvatar: string;
  defaultColor: string;
  suggestedKnowledgeBase: string;
  fields: AgentField[];
}

export interface AgentField {
  name: string;
  type: 'text' | 'textarea' | 'select' | 'multiselect';
  label: string;
  placeholder?: string;
  required: boolean;
  options?: string[];
  defaultValue?: string;
}

export interface CreateAgentRequest {
  name: string;
  role: string;
  specialty: string;
  description: string;
  prompt: string;
  model: string;
  avatar: string;
  color: string;
  knowledgeBase: string;
  templateId?: string;
}

export interface UpdateAgentRequest extends Partial<CreateAgentRequest> {
  id: string;
  isActive?: boolean;
}
