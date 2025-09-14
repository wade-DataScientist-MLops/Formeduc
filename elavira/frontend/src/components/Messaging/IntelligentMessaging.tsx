import React, { useState } from 'react';
import styled from 'styled-components';
import { useApp } from '../../context/AppContext';
import { AgentType } from '../../types';

const MessagingContainer = styled.div`
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  flex-direction: column;
`;

const Header = styled.header`
  background: white;
  padding: 20px 30px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
`;

const HeaderLeft = styled.div`
  display: flex;
  align-items: center;
  gap: 15px;
`;

const HeaderIcon = styled.div`
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 20px;
`;

const HeaderTitle = styled.h1`
  font-size: 24px;
  font-weight: 700;
  color: #1f2937;
  margin: 0;
`;

const AssistantSelector = styled.div`
  display: flex;
  align-items: center;
  gap: 10px;
`;

const SelectorLabel = styled.span`
  font-size: 14px;
  color: #6b7280;
  font-weight: 500;
`;

const AssistantDropdown = styled.div`
  display: flex;
  align-items: center;
  gap: 8px;
  background: #f3f4f6;
  padding: 8px 12px;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover {
    background: #e5e7eb;
  }
`;

const AssistantAvatar = styled.div`
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 12px;
  font-weight: 600;
`;

const AssistantName = styled.span`
  font-size: 14px;
  color: #374151;
  font-weight: 600;
`;

const AssistantType = styled.span`
  font-size: 12px;
  color: #6b7280;
`;

const MainContent = styled.main`
  flex: 1;
  padding: 40px 30px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
`;

const WelcomeSection = styled.div`
  text-align: center;
  margin-bottom: 40px;
`;

const WelcomeTitle = styled.h2`
  font-size: 32px;
  font-weight: 700;
  color: white;
  margin: 0 0 16px 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
`;

const WelcomeSubtitle = styled.p`
  font-size: 18px;
  color: rgba(255, 255, 255, 0.9);
  margin: 0;
  font-weight: 300;
`;

const HistoryMessage = styled.div`
  display: flex;
  align-items: center;
  gap: 12px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  padding: 16px 20px;
  border-radius: 20px;
  margin-bottom: 30px;
  color: rgba(255, 255, 255, 0.9);
  font-size: 14px;
`;

const HistoryIcon = styled.div`
  font-size: 20px;
`;

const AgentsCarousel = styled.div`
  width: 100%;
  max-width: 800px;
  position: relative;
`;

const CarouselContainer = styled.div`
  display: flex;
  gap: 20px;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  padding: 20px 0;
  
  &::-webkit-scrollbar {
    display: none;
  }
`;

const AgentCard = styled.div<{ isActive?: boolean }>`
  min-width: 350px;
  height: 400px;
  border-radius: 20px;
  background: ${props => props.isActive ? 'rgba(255, 255, 255, 0.95)' : 'rgba(255, 255, 255, 0.1)'};
  backdrop-filter: blur(10px);
  border: 2px solid ${props => props.isActive ? 'rgba(255, 255, 255, 0.3)' : 'rgba(255, 255, 255, 0.2)'};
  padding: 30px;
  display: flex;
  flex-direction: column;
  cursor: pointer;
  transition: all 0.3s ease;
  scroll-snap-align: center;
  position: relative;
  overflow: hidden;

  &:hover {
    transform: translateY(-5px);
    background: rgba(255, 255, 255, 0.95);
    border-color: rgba(255, 255, 255, 0.4);
  }
`;

const AgentBackground = styled.div<{ backgroundImage?: string }>`
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: ${props => props.backgroundImage ? `url(${props.backgroundImage})` : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'};
  background-size: cover;
  background-position: center;
  opacity: 0.8;
  z-index: -1;
`;

const AgentGradient = styled.div`
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.9) 0%, rgba(118, 75, 162, 0.9) 100%);
  z-index: -1;
`;

const AgentName = styled.h3`
  font-size: 24px;
  font-weight: 700;
  color: white;
  margin: 0 0 8px 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
`;

const AgentRole = styled.p`
  font-size: 16px;
  color: rgba(255, 255, 255, 0.9);
  margin: 0 0 20px 0;
  font-weight: 500;
`;

const AgentDescription = styled.p`
  font-size: 14px;
  color: rgba(255, 255, 255, 0.9);
  line-height: 1.6;
  margin: 0 0 20px 0;
  flex: 1;
`;

const CapabilitiesContainer = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: auto;
`;

const CapabilityTag = styled.span`
  background: rgba(255, 255, 255, 0.2);
  color: white;
  padding: 6px 12px;
  border-radius: 15px;
  font-size: 12px;
  font-weight: 500;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
`;

const ChatInputContainer = styled.div`
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: white;
  padding: 20px 30px;
  box-shadow: 0 -2px 20px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 15px;
`;

const ChatInput = styled.input`
  flex: 1;
  padding: 15px 20px;
  border: 2px solid #e5e7eb;
  border-radius: 25px;
  font-size: 16px;
  outline: none;
  transition: all 0.2s ease;

  &:focus {
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }

  &::placeholder {
    color: #9ca3af;
  }
`;

const ActionButton = styled.button<{ color: string }>`
  width: 50px;
  height: 50px;
  border: none;
  border-radius: 50%;
  background: ${props => props.color};
  color: white;
  font-size: 18px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;

  &:hover {
    transform: scale(1.1);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  }
`;

const agents = [
  {
    id: 'elavira',
    name: 'Elavira',
    role: 'Experte Formations',
    description: 'Professionnelle de la santé et de l\'éducation, Elavira vous accompagne dans vos formations de secourisme avec expertise et vigilance. Elle porte des lunettes et un stéthoscope, symboles de son professionnalisme.',
    capabilities: ['Formations certifiantes', 'Secourisme adapté', 'Prévention des risques', 'Accompagnement personnalisé'],
    backgroundImage: '/images/elavira-real.png',
    gradient: 'linear-gradient(135deg, rgba(102, 126, 234, 0.9) 0%, rgba(118, 75, 162, 0.9) 100%)'
  },
  {
    id: 'solenys',
    name: 'Solenys',
    role: 'Professeur Académique',
    description: 'Professeur québécois spécialisé dans l\'enseignement secondaire selon le programme PFEQ. Solenys vous guide dans vos apprentissages en mathématiques, sciences et français avec pédagogie et bienveillance.',
    capabilities: ['PFEQ Curriculum', 'Mathématiques', 'Sciences', 'Français'],
    backgroundImage: '/images/solenys-banner.svg',
    gradient: 'linear-gradient(135deg, rgba(118, 75, 162, 0.9) 0%, rgba(102, 126, 234, 0.9) 100%)'
  }
];

export const IntelligentMessaging: React.FC = () => {
  const { dispatch } = useApp();
  const [selectedAgent, setSelectedAgent] = useState('solenys');
  const [message, setMessage] = useState('');

  const handleAgentSelect = (agentId: string) => {
    setSelectedAgent(agentId);
  };

  const handleStartChat = () => {
    dispatch({ type: 'SET_SELECTED_AGENT', payload: selectedAgent as AgentType });
    dispatch({ type: 'SET_PAGE', payload: 'chat' });
  };

  const handleSendMessage = () => {
    if (message.trim()) {
      handleStartChat();
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSendMessage();
    }
  };

  return (
    <MessagingContainer>
      <Header>
        <HeaderLeft>
          <HeaderIcon>💬</HeaderIcon>
          <HeaderTitle>Messagerie intelligente</HeaderTitle>
        </HeaderLeft>
        
        <AssistantSelector>
          <SelectorLabel>Assistant:</SelectorLabel>
          <AssistantDropdown onClick={() => setSelectedAgent(selectedAgent === 'elavira' ? 'solenys' : 'elavira')}>
            <AssistantAvatar>
              {selectedAgent === 'elavira' ? 'E' : 'S'}
            </AssistantAvatar>
            <AssistantName>
              {selectedAgent === 'elavira' ? 'Elavira' : 'Solenys'}
            </AssistantName>
          </AssistantDropdown>
          <AssistantType>Assistant IA</AssistantType>
        </AssistantSelector>
      </Header>

      <MainContent>
        <WelcomeSection>
          <WelcomeTitle>Découvrez nos Assistants Intelligents</WelcomeTitle>
          <WelcomeSubtitle>
            Choisissez l'assistant qui correspond le mieux à vos besoins et commencez votre conversation
          </WelcomeSubtitle>
        </WelcomeSection>

        <HistoryMessage>
          <HistoryIcon>💬</HistoryIcon>
          <span>Aucun message dans l'historique. Commencez la conversation ci-dessous!</span>
        </HistoryMessage>

        <AgentsCarousel>
          <CarouselContainer>
            {agents.map((agent) => (
              <AgentCard
                key={agent.id}
                isActive={selectedAgent === agent.id}
                onClick={() => handleAgentSelect(agent.id)}
              >
                <AgentBackground backgroundImage={agent.backgroundImage} />
                <AgentGradient />
                
                <AgentName>{agent.name}</AgentName>
                <AgentRole>{agent.role}</AgentRole>
                <AgentDescription>{agent.description}</AgentDescription>
                
                <CapabilitiesContainer>
                  {agent.capabilities.map((capability, index) => (
                    <CapabilityTag key={index}>{capability}</CapabilityTag>
                  ))}
                </CapabilitiesContainer>
              </AgentCard>
            ))}
          </CarouselContainer>
        </AgentsCarousel>
      </MainContent>

      <ChatInputContainer>
        <ChatInput
          type="text"
          placeholder="Écrivez votre message ici..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={handleKeyPress}
        />
        <ActionButton color="#10b981" title="Enregistrement vocal">
          🎤
        </ActionButton>
        <ActionButton color="#3b82f6" title="Envoyer" onClick={handleSendMessage}>
          🚀
        </ActionButton>
        <ActionButton color="#ec4899" title="Pièces jointes">
          ➕
        </ActionButton>
        <ActionButton color="#ec4899" title="Profil">
          👤
        </ActionButton>
      </ChatInputContainer>
    </MessagingContainer>
  );
};
