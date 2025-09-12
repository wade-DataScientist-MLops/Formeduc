import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface MessageRequest {
  text: string;
  user_id: string;
  agent_id: string;
}

export interface MessageResponse {
  id: string;
  text: string;
  user_id: string;
  timestamp: string;
  audio_base64?: string;
  suggested_prompts?: string[];
}

export interface VoiceMessageRequest {
  text: string;
  user_id: string;
  agent_id: 'elavira' | 'solenys';
}

export const sendMessage = async (message: MessageRequest): Promise<MessageResponse> => {
  try {
    const response = await api.post('/chat/send_message/', message);
    return response.data;
  } catch (error) {
    console.error('Erreur envoi message:', error);
    throw error;
  }
};

export const sendVoiceMessage = async (message: VoiceMessageRequest): Promise<MessageResponse> => {
  try {
    const response = await api.post('/chat/send_message/', {
      text: message.text,
      user_id: message.user_id,
      agent_id: message.agent_id
    });
    return response.data;
  } catch (error) {
    console.error('Erreur envoi message vocal:', error);
    throw error;
  }
};

export const getChatHistory = async (agentId: string, userId: string) => {
  try {
    const response = await api.get(`/chat/history/?agent_id=${agentId}&user_id=${userId}`);
    return response.data;
  } catch (error) {
    console.error('Erreur récupération historique:', error);
    throw error;
  }
};

export const transcribeAudio = async (audioBlob: Blob): Promise<string> => {
  try {
    const formData = new FormData();
    formData.append('audio_file', audioBlob, 'audio.wav');
    
    const response = await api.post('/chat/transcribe_audio/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    return response.data.transcription;
  } catch (error) {
    console.error('Erreur transcription audio:', error);
    throw error;
  }
};

export const healthCheck = async () => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    console.error('Erreur health check:', error);
    throw error;
  }
};

export default api;
