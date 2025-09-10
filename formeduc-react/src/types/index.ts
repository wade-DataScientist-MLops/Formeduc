// Types pour l'application Formeduc React

export interface User {
  username: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface Message {
  id: string;
  text: string;
  user_id: string;
  timestamp: string;
  audio_base64?: string;
  suggested_prompts?: string[];
}

export interface MessageCreate {
  text: string;
  user_id: string;
  agent_id: string;
}

export interface TranscribeResponse {
  transcribed_text: string;
}

export type AgentType = 'agent-001' | 'agent-002';

export interface AppState {
  page: 'auth' | 'chat';
  messages: Message[];
  access_token: string | null;
  logged_in_user: string | null;
  selected_agent_id: AgentType;
  transcribing: boolean;
  thinking: boolean;
  last_suggested_prompts: string[];
  display_suggestions: boolean;
  message_input: string;
  audio_enabled: boolean;
}

