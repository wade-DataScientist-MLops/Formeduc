import axios from 'axios';
import { AuthResponse, Message, MessageCreate, TranscribeResponse } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://104.254.182.118:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Intercepteur pour ajouter le token d'authentification
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authAPI = {
  login: async (username: string, password: string): Promise<AuthResponse> => {
    const response = await api.post<AuthResponse>('/users/login/', { username, password });
    return response.data;
  },

  register: async (username: string, password: string): Promise<void> => {
    await api.post('/users/register/', { username, password });
  },

  getCurrentUser: async (): Promise<{ username: string }> => {
    const response = await api.get<{ username: string }>('/users/me/');
    return response.data;
  },
};

export const chatAPI = {
  sendMessage: async (message: MessageCreate & { agent?: string }): Promise<Message> => {
    const response = await api.post<Message>('/chat/send_message/', message);
    return response.data;
  },

  getHistory: async (agent_id: string, user_id: string): Promise<Message[]> => {
    const response = await api.get<Message[]>(`/chat/history/?agent_id=${agent_id}&user_id=${user_id}`);
    return response.data;
  },

  transcribeAudio: async (audioFile: File): Promise<TranscribeResponse> => {
    const formData = new FormData();
    formData.append('audio_file', audioFile);
    const response = await api.post<TranscribeResponse>('/chat/transcribe_audio/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
};

export const solenysAPI = {
  query: async (query: string): Promise<{ answer: string }> => {
    const response = await api.get<{ answer: string }>('/solenys/solenys_query', {
      params: { q: query },
    });
    return response.data;
  },
};

export default api;
