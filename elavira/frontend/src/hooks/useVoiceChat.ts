import { useState, useCallback } from 'react';
import { sendMessage } from '../services/api';

interface VoiceChatState {
  isProcessing: boolean;
  error: string | null;
  lastMessage: string | null;
  lastAudioResponse: Blob | null;
}

export const useVoiceChat = () => {
  const [state, setState] = useState<VoiceChatState>({
    isProcessing: false,
    error: null,
    lastMessage: null,
    lastAudioResponse: null
  });

  const sendVoiceMessage = useCallback(async (
    message: string, 
    agentId: string = 'elavira'
  ) => {
    setState(prev => ({ ...prev, isProcessing: true, error: null }));

    try {
      // Envoyer le message à l'API
      const response = await sendMessage({
        text: message,
        user_id: 'voice_user',
        agent_id: agentId
      });

      setState(prev => ({
        ...prev,
        isProcessing: false,
        lastMessage: response.text,
        error: null
      }));

      // Si l'API retourne de l'audio, le convertir en Blob
      if (response.audio_base64) {
        try {
          // Décoder l'audio base64
          const audioData = atob(response.audio_base64);
          const audioArray = new Uint8Array(audioData.length);
          for (let i = 0; i < audioData.length; i++) {
            audioArray[i] = audioData.charCodeAt(i);
          }
          
          const audioBlob = new Blob([audioArray], { type: 'audio/wav' });
          
          setState(prev => ({
            ...prev,
            lastAudioResponse: audioBlob
          }));

          return audioBlob;
        } catch (audioError) {
          console.error('Erreur décodage audio:', audioError);
          setState(prev => ({
            ...prev,
            error: 'Erreur de décodage audio'
          }));
        }
      }

      return null;
    } catch (error) {
      console.error('Erreur envoi message vocal:', error);
      setState(prev => ({
        ...prev,
        isProcessing: false,
        error: error instanceof Error ? error.message : 'Erreur inconnue'
      }));
      return null;
    }
  }, []);

  const clearError = useCallback(() => {
    setState(prev => ({ ...prev, error: null }));
  }, []);

  const reset = useCallback(() => {
    setState({
      isProcessing: false,
      error: null,
      lastMessage: null,
      lastAudioResponse: null
    });
  }, []);

  return {
    ...state,
    sendVoiceMessage,
    clearError,
    reset
  };
};
