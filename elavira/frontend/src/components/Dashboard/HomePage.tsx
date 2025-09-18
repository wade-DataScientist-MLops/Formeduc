import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { useApp } from '../../context/AppContext';

const HomeContainer = styled.div`
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  overflow-x: hidden;
`;

const HeroSection = styled.section`
  padding: 120px 0 80px;
  text-align: center;
  position: relative;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000"><defs><radialGradient id="a" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="rgba(255,255,255,0.1)"/><stop offset="100%" stop-color="rgba(255,255,255,0)"/></radialGradient></defs><circle cx="200" cy="200" r="100" fill="url(%23a)"/><circle cx="800" cy="300" r="150" fill="url(%23a)"/><circle cx="400" cy="700" r="120" fill="url(%23a)"/></svg>');
    opacity: 0.3;
  }
`;

const HeroContent = styled.div`
  position: relative;
  z-index: 2;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
`;

const Badge = styled.div`
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  padding: 8px 16px;
  border-radius: 50px;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 24px;
  border: 1px solid rgba(255, 255, 255, 0.3);
`;

const StarIcon = styled.span`
  color: #ffd700;
  font-size: 16px;
`;

const MainTitle = styled.h1`
  font-size: clamp(2.5rem, 5vw, 4rem);
  font-weight: 800;
  line-height: 1.1;
  margin-bottom: 24px;
  background: linear-gradient(135deg, #ffffff 0%, #e0e7ff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
`;

const Subtitle = styled.p`
  font-size: clamp(1.1rem, 2vw, 1.4rem);
  line-height: 1.6;
  margin-bottom: 40px;
  opacity: 0.9;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
`;

const StatsContainer = styled.div`
  display: flex;
  justify-content: center;
  gap: 60px;
  margin-bottom: 50px;
  flex-wrap: wrap;
`;

const StatItem = styled.div`
  text-align: center;
`;

const StatNumber = styled.div`
  font-size: 2.5rem;
  font-weight: 800;
  color: #ffd700;
  margin-bottom: 8px;
`;

const StatLabel = styled.div`
  font-size: 1rem;
  opacity: 0.8;
  font-weight: 500;
`;

const CTAButtons = styled.div`
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 80px;
`;

const PrimaryButton = styled.button`
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
  color: white;
  border: none;
  padding: 16px 32px;
  border-radius: 50px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 8px 25px rgba(255, 107, 107, 0.3);
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 35px rgba(255, 107, 107, 0.4);
  }
`;

const SecondaryButton = styled.button`
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.3);
  padding: 14px 30px;
  border-radius: 50px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  
  &:hover {
    background: rgba(255, 255, 255, 0.2);
    transform: translateY(-2px);
  }
`;

const AgentsSection = styled.section`
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  padding: 80px 0;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
`;

const SectionTitle = styled.h2`
  font-size: 2.5rem;
  font-weight: 700;
  text-align: center;
  margin-bottom: 60px;
  background: linear-gradient(135deg, #ffffff 0%, #e0e7ff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
`;

const AgentsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
`;

const AgentCard = styled.div`
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  padding: 30px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4, #feca57);
  }
  
  &:hover {
    transform: translateY(-8px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
    border-color: rgba(255, 255, 255, 0.4);
  }
`;

const AgentHeader = styled.div`
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
`;

const AgentAvatar = styled.div`
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: bold;
  color: white;
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
`;

const AgentInfo = styled.div`
  flex: 1;
`;

const AgentName = styled.h3`
  font-size: 1.3rem;
  font-weight: 700;
  margin-bottom: 4px;
  color: white;
`;

const AgentRole = styled.p`
  font-size: 0.9rem;
  opacity: 0.8;
  margin: 0;
`;

const AgentDescription = styled.p`
  font-size: 1rem;
  line-height: 1.6;
  margin-bottom: 20px;
  opacity: 0.9;
`;

const AgentTags = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 20px;
`;

const Tag = styled.span`
  background: rgba(255, 255, 255, 0.2);
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 500;
  border: 1px solid rgba(255, 255, 255, 0.3);
`;

const AgentActions = styled.div`
  display: flex;
  gap: 12px;
`;

const ActionButton = styled.button<{ variant: 'primary' | 'secondary' }>`
  flex: 1;
  padding: 12px 20px;
  border-radius: 25px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  
  ${props => props.variant === 'primary' ? `
    background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
    color: white;
    box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
    
    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4);
    }
  ` : `
    background: rgba(255, 255, 255, 0.1);
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.3);
    
    &:hover {
      background: rgba(255, 255, 255, 0.2);
    }
  `}
`;

const EmptyState = styled.div`
  text-align: center;
  padding: 60px 20px;
  opacity: 0.8;
`;

const EmptyIcon = styled.div`
  font-size: 4rem;
  margin-bottom: 20px;
`;

const EmptyText = styled.p`
  font-size: 1.2rem;
  margin-bottom: 30px;
`;

const CreateAgentButton = styled.button`
  background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
  color: white;
  border: none;
  padding: 16px 32px;
  border-radius: 50px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 8px 25px rgba(78, 205, 196, 0.3);
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 35px rgba(78, 205, 196, 0.4);
  }
`;

export const HomePage: React.FC = () => {
  const { state, dispatch } = useApp();
  const [agents, setAgents] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAgents();
  }, []);

  const loadAgents = async () => {
    try {
      const response = await fetch('http://104.254.182.118:8000/api/agents');
      if (response.ok) {
        const data = await response.json();
        setAgents(data);
      }
    } catch (error) {
      console.error('Erreur lors du chargement des agents:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAgentClick = (agentId: string) => {
    dispatch({ type: 'SET_SELECTED_AGENT_ID', payload: agentId });
    dispatch({ type: 'SET_PAGE', payload: 'chat' });
  };

  const handleCreateAgent = () => {
    // Rediriger vers la page de connexion si pas connecté
    if (!state.logged_in_user) {
      dispatch({ type: 'SET_PAGE', payload: 'auth' });
      return;
    }
    
    dispatch({ type: 'SET_PAGE', payload: 'agents' });
  };

  const handleTryNow = () => {
    console.log('handleTryNow called');
    console.log('logged_in_user:', state.logged_in_user);
    console.log('state:', state);
    
    // Rediriger vers la page de connexion si pas connecté
    if (!state.logged_in_user) {
      console.log('Redirecting to auth page');
      // Test direct avec window.location
      window.location.href = '/?page=auth';
      dispatch({ type: 'SET_PAGE', payload: 'auth' });
      return;
    }
    
    if (agents.length > 0) {
      handleAgentClick(agents[0].id);
    } else {
      handleCreateAgent();
    }
  };

  return (
    <HomeContainer>
      <HeroSection>
        <HeroContent>
          <Badge>
            <StarIcon>⭐</StarIcon>
            Excellent 4.9 sur 5
          </Badge>
          
          <MainTitle>
            Des agents IA autonomes au service de votre entreprise
          </MainTitle>
          
          <Subtitle>
            Votre équipe d'agents IA s'intègre à vos outils du quotidien.
            Disponible 24h/24, 7j/7 : votre équipe IA ne dort jamais.
          </Subtitle>
          
          <StatsContainer>
            <StatItem>
              <StatNumber>{agents.length}</StatNumber>
              <StatLabel>agents</StatLabel>
            </StatItem>
            <StatItem>
              <StatNumber>24/7</StatNumber>
              <StatLabel>disponibilité</StatLabel>
            </StatItem>
            <StatItem>
              <StatNumber>100%</StatNumber>
              <StatLabel>automatisé</StatLabel>
            </StatItem>
          </StatsContainer>
          
          <CTAButtons>
            <PrimaryButton onClick={() => {
              console.log('Button clicked!');
              handleTryNow();
            }}>
              {state.logged_in_user ? 'Essayer gratuitement' : 'Se connecter'}
            </PrimaryButton>
            <SecondaryButton onClick={handleCreateAgent}>
              {state.logged_in_user ? 'Créer un agent' : 'Découvrir'}
            </SecondaryButton>
          </CTAButtons>
        </HeroContent>
      </HeroSection>

      <AgentsSection>
        <SectionTitle>Concentrez-vous sur ce qui compte vraiment.</SectionTitle>
        
        {loading ? (
          <div style={{ textAlign: 'center', padding: '60px 20px' }}>
            <div style={{ fontSize: '2rem', marginBottom: '20px' }}>⏳</div>
            <p>Chargement de vos agents...</p>
          </div>
        ) : agents.length > 0 ? (
          <AgentsGrid>
            {agents.map((agent) => (
              <AgentCard key={agent.id} onClick={() => handleAgentClick(agent.id)}>
                <AgentHeader>
                  <AgentAvatar>
                    {agent.avatar || '🤖'}
                  </AgentAvatar>
                  <AgentInfo>
                    <AgentName>{agent.name}</AgentName>
                    <AgentRole>{agent.role}</AgentRole>
                  </AgentInfo>
                </AgentHeader>
                
                <AgentDescription>
                  {agent.description}
                </AgentDescription>
                
                {agent.specialty && (
                  <AgentTags>
                    <Tag>{agent.specialty}</Tag>
                    {agent.knowledge_base && <Tag>{agent.knowledge_base}</Tag>}
                  </AgentTags>
                )}
                
                <AgentActions>
                  <ActionButton variant="primary" onClick={(e) => {
                    e.stopPropagation();
                    handleAgentClick(agent.id);
                  }}>
                    Chat
                  </ActionButton>
                  <ActionButton variant="secondary" onClick={(e) => {
                    e.stopPropagation();
                    dispatch({ type: 'SET_PAGE', payload: 'agents' });
                  }}>
                    Modifier
                  </ActionButton>
                </AgentActions>
              </AgentCard>
            ))}
          </AgentsGrid>
        ) : (
          <EmptyState>
            <EmptyIcon>🤖</EmptyIcon>
            <EmptyText>Aucun agent créé pour le moment</EmptyText>
            <CreateAgentButton onClick={handleCreateAgent}>
              + Créer votre premier agent
            </CreateAgentButton>
          </EmptyState>
        )}
      </AgentsSection>
    </HomeContainer>
  );
};
