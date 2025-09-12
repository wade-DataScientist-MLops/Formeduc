import React, { useState, useRef, useEffect } from 'react';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';

const VoiceContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
`;

const VoiceButton = styled(motion.button)<{ $isRecording: boolean; $isPlaying: boolean }>`
  width: 80px;
  height: 80px;
  border-radius: 50%;
  border: none;
  background: ${props => 
    props.$isRecording ? '#ff4757' : 
    props.$isPlaying ? '#2ed573' : 
    '#3742fa'
  };
  color: white;
  font-size: 24px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease;
  
  &:hover {
    transform: scale(1.05);
    box-shadow: 0 12px 35px rgba(0, 0, 0, 0.4);
  }
  
  &:active {
    transform: scale(0.95);
  }
`;

const StatusText = styled(motion.div)`
  color: white;
  font-size: 16px;
  font-weight: 500;
  text-align: center;
  min-height: 24px;
`;

const AudioControls = styled.div`
  display: flex;
  gap: 15px;
  align-items: center;
`;

const ControlButton = styled(motion.button)`
  padding: 10px 20px;
  border: 2px solid white;
  border-radius: 25px;
  background: transparent;
  color: white;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:hover {
    background: white;
    color: #3742fa;
  }
`;

const VolumeSlider = styled.input`
  width: 100px;
  height: 5px;
  border-radius: 5px;
  background: rgba(255, 255, 255, 0.3);
  outline: none;
  
  &::-webkit-slider-thumb {
    appearance: none;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: white;
    cursor: pointer;
  }
`;

const Waveform = styled.div`
  display: flex;
  gap: 3px;
  align-items: center;
  height: 40px;
`;

const WaveBar = styled(motion.div)<{ $delay: number }>`
  width: 4px;
  background: white;
  border-radius: 2px;
  animation-delay: ${props => props.$delay}s;
`;

interface VoiceInterfaceProps {
  onVoiceMessage: (message: string) => void;
  onVoiceResponse?: (audioBlob: Blob) => void;
  isProcessing?: boolean;
}

const VoiceInterface: React.FC<VoiceInterfaceProps> = ({
  onVoiceMessage,
  onVoiceResponse,
  isProcessing = false
}) => {
  const [isRecording, setIsRecording] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [status, setStatus] = useState('Appuyez pour parler');
  const [volume, setVolume] = useState(0.8);
  const [recognition, setRecognition] = useState<SpeechRecognition | null>(null);
  const [audioContext, setAudioContext] = useState<AudioContext | null>(null);
  const [currentAudio, setCurrentAudio] = useState<HTMLAudioElement | null>(null);
  
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  useEffect(() => {
    // Initialiser la reconnaissance vocale
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      const recognitionInstance = new SpeechRecognition();
      
      recognitionInstance.continuous = false;
      recognitionInstance.interimResults = false;
      recognitionInstance.lang = 'fr-FR';
      
      recognitionInstance.onstart = () => {
        setStatus('Écoute en cours...');
        setIsRecording(true);
      };
      
      recognitionInstance.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setStatus(`Message: "${transcript}"`);
        onVoiceMessage(transcript);
      };
      
      recognitionInstance.onerror = (event) => {
        console.error('Erreur de reconnaissance vocale:', event.error);
        setStatus('Erreur de reconnaissance');
        setIsRecording(false);
      };
      
      recognitionInstance.onend = () => {
        setIsRecording(false);
        setStatus('Appuyez pour parler');
      };
      
      setRecognition(recognitionInstance);
    }

    // Initialiser l'audio context
    if ('AudioContext' in window || 'webkitAudioContext' in window) {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      setAudioContext(new AudioContext());
    }

    return () => {
      if (currentAudio) {
        currentAudio.pause();
        currentAudio.currentTime = 0;
      }
    };
  }, [onVoiceMessage, currentAudio]);

  const startRecording = () => {
    if (recognition && !isRecording) {
      recognition.start();
    }
  };

  const stopRecording = () => {
    if (recognition && isRecording) {
      recognition.stop();
    }
  };

  const playAudio = (audioBlob: Blob) => {
    if (currentAudio) {
      currentAudio.pause();
    }

    const audioUrl = URL.createObjectURL(audioBlob);
    const audio = new Audio(audioUrl);
    audio.volume = volume;
    
    audio.onplay = () => setIsPlaying(true);
    audio.onended = () => {
      setIsPlaying(false);
      URL.revokeObjectURL(audioUrl);
    };
    
    audio.onerror = () => {
      setIsPlaying(false);
      setStatus('Erreur de lecture audio');
    };
    
    setCurrentAudio(audio);
    audio.play();
  };

  const stopAudio = () => {
    if (currentAudio) {
      currentAudio.pause();
      currentAudio.currentTime = 0;
      setIsPlaying(false);
    }
  };

  const toggleMute = () => {
    if (currentAudio) {
      currentAudio.muted = !currentAudio.muted;
    }
  };

  // Simuler la réponse vocale (à remplacer par l'API réelle)
  const simulateVoiceResponse = () => {
    if (onVoiceResponse) {
      // Créer un audio de test (à remplacer par l'API TTS)
      const audioBlob = new Blob(['test audio'], { type: 'audio/wav' });
      onVoiceResponse(audioBlob);
    }
  };

  return (
    <VoiceContainer>
      <VoiceButton
        $isRecording={isRecording}
        $isPlaying={isPlaying}
        onClick={isRecording ? stopRecording : startRecording}
        disabled={isProcessing}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        animate={{
          scale: isRecording ? [1, 1.1, 1] : 1,
          rotate: isRecording ? [0, 5, -5, 0] : 0
        }}
        transition={{
          scale: { duration: 0.5, repeat: isRecording ? Infinity : 0 },
          rotate: { duration: 0.5, repeat: isRecording ? Infinity : 0 }
        }}
      >
        {isRecording ? '⏹️' : isPlaying ? '🔊' : '🎤'}
      </VoiceButton>

      <StatusText
        key={status}
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -10 }}
      >
        {status}
      </StatusText>

      {isRecording && (
        <Waveform>
          {[...Array(20)].map((_, i) => (
            <WaveBar
              key={i}
              $delay={i * 0.1}
              initial={{ height: 10 }}
              animate={{ height: [10, 30, 10] }}
              transition={{
                duration: 0.5,
                repeat: Infinity,
                delay: i * 0.1
              }}
            />
          ))}
        </Waveform>
      )}

      <AudioControls>
        <ControlButton
          onClick={stopAudio}
          disabled={!isPlaying}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          ⏹️ Arrêter
        </ControlButton>
        
        <ControlButton
          onClick={toggleMute}
          disabled={!isPlaying}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          🔇 Muet
        </ControlButton>
        
        <ControlButton
          onClick={simulateVoiceResponse}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          🔊 Test TTS
        </ControlButton>
      </AudioControls>

      <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
        <span style={{ color: 'white', fontSize: '14px' }}>Volume:</span>
        <VolumeSlider
          type="range"
          min="0"
          max="1"
          step="0.1"
          value={volume}
          onChange={(e) => setVolume(parseFloat(e.target.value))}
        />
      </div>
    </VoiceContainer>
  );
};

export default VoiceInterface;
