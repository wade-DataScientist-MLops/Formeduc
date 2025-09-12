import React, { useState } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import VoiceInterface from './components/VoiceInterface/VoiceInterface';
import AgentSelector from './components/AgentSelector/AgentSelector';
import ChatInterface from './components/ChatInterface/ChatInterface';
import { useVoiceChat } from './hooks/useVoiceChat';

const AppContainer = styled.div`
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  flex-direction: column;
`;

const Header = styled(motion.header)`
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  padding: 20px;
  text-align: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
`;

const Title = styled.h1`
  color: white;
  font-size: 2.5rem;
  margin: 0;
  font-weight: 700;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
`;

const Subtitle = styled.p`
  color: rgba(255, 255, 255, 0.8);
  font-size: 1.2rem;
  margin: 10px 0 0 0;
`;

const MainContent = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 20px;
  gap: 20px;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
`;

const VoiceSection = styled(motion.section)`
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.2);
`;

const ChatSection = styled(motion.section)`
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  flex: 1;
  display: flex;
  flex-direction: column;
`;

const ErrorMessage = styled(motion.div)`
  background: #ff4757;
  color: white;
  padding: 15px;
  border-radius: 10px;
  margin: 10px 0;
  text-align: center;
`;

function App() {
  const [selectedAgent, setSelectedAgent] = useState<'elavira' | 'solenys'>('elavira');
  const [messages, setMessages] = useState<Array<{
    id: string;
    text: string;
    user_id: string;
    timestamp: string;
    audio_base64?: string;
  }>>([]);
  
  const { 
    isProcessing, 
    error, 
    sendVoiceMessage, 
    clearError 
  } = useVoiceChat();

  const handleVoiceMessage = async (message: string) => {
    try {
      const response = await sendVoiceMessage(message, selectedAgent);
      
      // Ajouter le message utilisateur
      const userMessage = {
        id: Date.now().toString() + '_user',
        text: message,
        user_id: 'Vous',
        timestamp: new Date().toISOString()
      };
      
      setMessages(prev => [...prev, userMessage]);
      
      // Ajouter la réponse de l'agent
      if (response) {
        const agentMessage = {
          id: Date.now().toString() + '_agent',
          text: response.text || 'Réponse reçue',
          user_id: selectedAgent === 'elavira' ? 'Elavira Assistant' : 'Solenys Assistant',
          timestamp: new Date().toISOString(),
          audio_base64: response.audio_base64
        };
        
        setMessages(prev => [...prev, agentMessage]);
      }
    } catch (err) {
      console.error('Erreur envoi message vocal:', err);
    }
  };

  const handleVoiceResponse = (audioBlob: Blob) => {
    // Jouer l'audio de réponse
    const audioUrl = URL.createObjectURL(audioBlob);
    const audio = new Audio(audioUrl);
    audio.play();
    
    audio.onended = () => {
      URL.revokeObjectURL(audioUrl);
    };
  };

  return (
    <AppContainer>
      <Header
        initial={{ opacity: 0, y: -50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
      >
        <Title>🎤 Elavira Voice Assistant</Title>
        <Subtitle>Parlez avec vos assistants IA spécialisés</Subtitle>
      </Header>

      <MainContent>
        <VoiceSection
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          <AgentSelector
            selectedAgent={selectedAgent}
            onAgentChange={setSelectedAgent}
          />
          
          <VoiceInterface
            onVoiceMessage={handleVoiceMessage}
            onVoiceResponse={handleVoiceResponse}
            isProcessing={isProcessing}
          />
          
          {error && (
            <ErrorMessage
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
            >
              {error}
              <button 
                onClick={clearError}
                style={{ 
                  marginLeft: '10px', 
                  background: 'none', 
                  border: 'none', 
                  color: 'white', 
                  cursor: 'pointer' 
                }}
              >
                ✕
              </button>
            </ErrorMessage>
          )}
        </VoiceSection>

        <ChatSection
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
        >
          <ChatInterface
            messages={messages}
            selectedAgent={selectedAgent}
          />
        </ChatSection>
      </MainContent>
    </AppContainer>
  );
}

export default App;
