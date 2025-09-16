import React, { useState, useRef } from 'react';
import styled from 'styled-components';

const InputContainer = styled.div`
  display: flex;
  gap: 10px;
  align-items: center;
  background: white;
  border-radius: 25px;
  padding: 10px 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
`;

const TextInput = styled.input`
  flex: 1;
  border: none;
  outline: none;
  font-size: 16px;
  padding: 10px 0;
  background: transparent;

  &::placeholder {
    color: #a0aec0;
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
`;

const Button = styled.button<{ variant?: 'primary' | 'secondary' | 'danger' }>`
  width: 45px;
  height: 45px;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  transition: all 0.3s ease;
  background: ${props => {
    switch (props.variant) {
      case 'primary': return 'linear-gradient(135deg, #3b82f6, #2e6bb4)';
      case 'danger': return 'linear-gradient(135deg, #e53e3e, #c53030)';
      default: return 'linear-gradient(135deg, #68d391, #48bb78)';
    }
  }};
  color: white;

  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }
`;

const AudioButton = styled(Button)<{ isRecording?: boolean }>`
  background: ${props => props.isRecording 
    ? 'linear-gradient(135deg, #e53e3e, #c53030)' 
    : 'linear-gradient(135deg, #68d391, #48bb78)'
  };
`;

const AudioToggleButton = styled(Button)`
  background: ${props => props.disabled 
    ? 'linear-gradient(135deg, #a0a0a0, #808080)' 
    : 'linear-gradient(135deg, #f093fb, #f5576c)'
  };
`;

interface MessageInputProps {
  onSendMessage: (message: string) => void;
  onTranscribeAudio?: (audioFile: File) => void;
  disabled?: boolean;
  audioEnabled?: boolean;
  onToggleAudio?: () => void;
  placeholder?: string;
}

export const MessageInput: React.FC<MessageInputProps> = ({
  onSendMessage,
  onTranscribeAudio,
  disabled = false,
  audioEnabled = false,
  onToggleAudio,
  placeholder = "Tapez votre message..."
}) => {
  const [message, setMessage] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  const handleSend = () => {
    if (message.trim() && !disabled) {
      onSendMessage(message);
      setMessage('');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
        const audioFile = new File([audioBlob], 'audio.wav', { type: 'audio/wav' });
        onTranscribeAudio?.(audioFile);
        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorder.start();
      setIsRecording(true);
    } catch (error) {
      console.error('Erreur lors de l\'accès au microphone:', error);
      alert('Impossible d\'accéder au microphone. Vérifiez les permissions.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const handleMicClick = () => {
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  };

  return (
    <InputContainer>
      <TextInput
        type="text"
        placeholder={placeholder}
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyPress={handleKeyPress}
        disabled={disabled}
      />
      
      <AudioButton
        onClick={handleMicClick}
        disabled={disabled}
        isRecording={isRecording}
        title={isRecording ? 'Arrêter l\'enregistrement' : 'Enregistrer un message vocal'}
      >
        {isRecording ? '⏹️' : '🎙️'}
      </AudioButton>
      
      <Button
        onClick={handleSend}
        disabled={disabled || !message.trim()}
        variant="primary"
        title="Envoyer le message"
      >
        🚀
      </Button>
      
      <AudioToggleButton
        onClick={onToggleAudio}
        disabled={disabled}
        title={audioEnabled ? 'Désactiver l\'audio' : 'Activer l\'audio'}
      >
        {audioEnabled ? '🔊' : '🔇'}
      </AudioToggleButton>
    </InputContainer>
  );
};

