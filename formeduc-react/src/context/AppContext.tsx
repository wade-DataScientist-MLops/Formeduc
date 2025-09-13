import React, { createContext, useContext, useReducer, ReactNode } from 'react';
import { AppState, Message, AgentType } from '../types';

interface AppContextType {
  state: AppState;
  dispatch: React.Dispatch<AppAction>;
}

type AppAction =
  | { type: 'SET_PAGE'; payload: 'auth' | 'chat' | 'agents' }
  | { type: 'SET_MESSAGES'; payload: Message[] }
  | { type: 'ADD_MESSAGE'; payload: Message }
  | { type: 'SET_ACCESS_TOKEN'; payload: string | null }
  | { type: 'SET_LOGGED_IN_USER'; payload: string | null }
  | { type: 'SET_SELECTED_AGENT'; payload: AgentType }
  | { type: 'SET_TRANSCRIBING'; payload: boolean }
  | { type: 'SET_THINKING'; payload: boolean }
  | { type: 'SET_LAST_SUGGESTED_PROMPTS'; payload: string[] }
  | { type: 'SET_DISPLAY_SUGGESTIONS'; payload: boolean }
  | { type: 'SET_MESSAGE_INPUT'; payload: string }
  | { type: 'SET_AUDIO_ENABLED'; payload: boolean }
  | { type: 'LOGOUT' };

const initialState: AppState = {
  page: 'auth',
  messages: [],
  access_token: localStorage.getItem('access_token'),
  logged_in_user: localStorage.getItem('logged_in_user'),
  selected_agent_id: 'agent-001',
  transcribing: false,
  thinking: false,
  last_suggested_prompts: [],
  display_suggestions: false,
  message_input: '',
  audio_enabled: true,
};

function appReducer(state: AppState, action: AppAction): AppState {
  switch (action.type) {
    case 'SET_PAGE':
      return { ...state, page: action.payload };
    case 'SET_MESSAGES':
      return { ...state, messages: action.payload };
    case 'ADD_MESSAGE':
      return { ...state, messages: [...state.messages, action.payload] };
    case 'SET_ACCESS_TOKEN':
      return { ...state, access_token: action.payload };
    case 'SET_LOGGED_IN_USER':
      return { ...state, logged_in_user: action.payload };
    case 'SET_SELECTED_AGENT':
      return { ...state, selected_agent_id: action.payload };
    case 'SET_TRANSCRIBING':
      return { ...state, transcribing: action.payload };
    case 'SET_THINKING':
      return { ...state, thinking: action.payload };
    case 'SET_LAST_SUGGESTED_PROMPTS':
      return { ...state, last_suggested_prompts: action.payload };
    case 'SET_DISPLAY_SUGGESTIONS':
      return { ...state, display_suggestions: action.payload };
    case 'SET_MESSAGE_INPUT':
      return { ...state, message_input: action.payload };
    case 'SET_AUDIO_ENABLED':
      return { ...state, audio_enabled: action.payload };
    case 'LOGOUT':
      localStorage.removeItem('access_token');
      localStorage.removeItem('logged_in_user');
      return {
        ...initialState,
        page: 'auth',
        access_token: null,
        logged_in_user: null,
      };
    default:
      return state;
  }
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export function AppProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(appReducer, initialState);

  return (
    <AppContext.Provider value={{ state, dispatch }}>
      {children}
    </AppContext.Provider>
  );
}

export function useApp() {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
}

