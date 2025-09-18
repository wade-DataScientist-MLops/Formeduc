import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { useApp } from '../../context/AppContext';

const Container = styled.div`
  min-height: 100vh;
  background: #ffffff;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
`;

const Header = styled.header`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  padding: 0 24px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
`;

const Logo = styled.div`
  font-size: 24px;
  font-weight: 700;
  color: #000;
  display: flex;
  align-items: center;
  gap: 8px;
`;

const LogoIcon = styled.div`
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
`;

const Nav = styled.nav`
  display: flex;
  align-items: center;
  gap: 32px;
`;

const NavLink = styled.a`
  color: #666;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
  
  &:hover {
    color: #000;
  }
`;

const AuthButtons = styled.div`
  display: flex;
  align-items: center;
  gap: 16px;
`;

const LoginButton = styled.button`
  background: none;
  border: none;
  color: #666;
  font-weight: 500;
  cursor: pointer;
  padding: 8px 16px;
  border-radius: 8px;
  transition: all 0.2s;
  
  &:hover {
    background: #f5f5f5;
    color: #000;
  }
`;

const SignUpButton = styled.button`
  background: #000;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  
  &:hover {
    background: #333;
    transform: translateY(-1px);
  }
`;

const HeroSection = styled.section`
  padding: 120px 0 80px;
  text-align: center;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
`;

const HeroContainer = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
`;

const Badge = styled.div`
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: #f1f5f9;
  border: 1px solid #e2e8f0;
  padding: 8px 16px;
  border-radius: 24px;
  font-size: 14px;
  font-weight: 500;
  color: #475569;
  margin-bottom: 32px;
`;

const StarIcon = styled.span`
  color: #fbbf24;
`;

const MainTitle = styled.h1`
  font-size: clamp(2.5rem, 5vw, 4rem);
  font-weight: 800;
  line-height: 1.1;
  color: #0f172a;
  margin-bottom: 24px;
  letter-spacing: -0.02em;
`;

const Subtitle = styled.p`
  font-size: clamp(1.1rem, 2vw, 1.25rem);
  line-height: 1.6;
  color: #64748b;
  margin-bottom: 48px;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
`;

const CTAButtons = styled.div`
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 80px;
`;

const PrimaryButton = styled.button`
  background: #000;
  color: white;
  border: none;
  padding: 16px 32px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  
  &:hover {
    background: #333;
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
  }
`;

const SecondaryButton = styled.button`
  background: white;
  color: #000;
  border: 2px solid #e2e8f0;
  padding: 14px 30px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  
  &:hover {
    border-color: #000;
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  }
`;

const StatsSection = styled.section`
  padding: 80px 0;
  background: white;
`;

const StatsContainer = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
`;

const StatsTitle = styled.h2`
  font-size: 2.5rem;
  font-weight: 700;
  text-align: center;
  color: #0f172a;
  margin-bottom: 60px;
`;

const StatsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 40px;
`;

const StatCard = styled.div`
  text-align: center;
  padding: 40px 24px;
  border-radius: 16px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  transition: all 0.2s;
  
  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  }
`;

const StatIcon = styled.div`
  font-size: 3rem;
  margin-bottom: 24px;
`;

const StatNumber = styled.div`
  font-size: 3rem;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 16px;
`;

const StatLabel = styled.div`
  font-size: 1.25rem;
  font-weight: 600;
  color: #64748b;
  margin-bottom: 16px;
`;

const StatDescription = styled.p`
  color: #64748b;
  line-height: 1.6;
`;

const AgentsSection = styled.section`
  padding: 80px 0;
  background: #f8fafc;
`;

const AgentsContainer = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
`;

const AgentsTitle = styled.h2`
  font-size: 2.5rem;
  font-weight: 700;
  text-align: center;
  color: #0f172a;
  margin-bottom: 60px;
`;

const AgentsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 32px;
`;

const AgentCard = styled.div`
  background: white;
  border-radius: 16px;
  padding: 32px;
  border: 1px solid #e2e8f0;
  transition: all 0.2s;
  cursor: pointer;
  
  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    border-color: #000;
  }
`;

const AgentHeader = styled.div`
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
`;

const AgentAvatar = styled.div`
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 20px;
`;

const AgentInfo = styled.div`
  flex: 1;
`;

const AgentName = styled.h3`
  font-size: 1.25rem;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 4px;
`;

const AgentRole = styled.p`
  color: #64748b;
  font-size: 14px;
`;

const AgentDescription = styled.p`
  color: #64748b;
  line-height: 1.6;
  margin-bottom: 24px;
`;

const AgentActions = styled.div`
  display: flex;
  gap: 12px;
`;

const ActionButton = styled.button<{ variant: 'primary' | 'secondary' }>`
  flex: 1;
  padding: 12px 20px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
  
  ${props => props.variant === 'primary' ? `
    background: #000;
    color: white;
    
    &:hover {
      background: #333;
    }
  ` : `
    background: #f8fafc;
    color: #64748b;
    border: 1px solid #e2e8f0;
    
    &:hover {
      background: #f1f5f9;
      color: #000;
    }
  `}
`;

const EmptyState = styled.div`
  text-align: center;
  padding: 80px 24px;
`;

const EmptyIcon = styled.div`
  font-size: 4rem;
  margin-bottom: 24px;
`;

const EmptyText = styled.p`
  font-size: 1.25rem;
  color: #64748b;
  margin-bottom: 32px;
`;

const CreateButton = styled.button`
  background: #000;
  color: white;
  border: none;
  padding: 16px 32px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  
  &:hover {
    background: #333;
    transform: translateY(-2px);
  }
`;

export const LimovaHomePage: React.FC = () => {
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
    if (!state.logged_in_user) {
      dispatch({ type: 'SET_PAGE', payload: 'auth' });
      return;
    }
    dispatch({ type: 'SET_PAGE', payload: 'agents' });
  };

  const handleTryNow = () => {
    console.log('Try now clicked');
    if (!state.logged_in_user) {
      dispatch({ type: 'SET_PAGE', payload: 'auth' });
      return;
    }
    if (agents.length > 0) {
      handleAgentClick(agents[0].id);
    } else {
      handleCreateAgent();
    }
  };

  const handleLogin = () => {
    console.log('Login clicked');
    dispatch({ type: 'SET_PAGE', payload: 'auth' });
  };

  const handleSignUp = () => {
    console.log('Sign up clicked');
    dispatch({ type: 'SET_PAGE', payload: 'auth' });
  };

  return (
    <Container>
      <Header>
        <Logo>
          <LogoIcon>E</LogoIcon>
          Elavira
        </Logo>
        <Nav>
          <NavLink href="#features">Fonctionnalités</NavLink>
          <NavLink href="#pricing">Tarifs</NavLink>
          <NavLink href="#about">À propos</NavLink>
        </Nav>
        <AuthButtons>
          <LoginButton onClick={handleLogin}>
            Se connecter
          </LoginButton>
          <SignUpButton onClick={handleSignUp}>
            Commencer
          </SignUpButton>
        </AuthButtons>
      </Header>

      <HeroSection>
        <HeroContainer>
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
          
          <CTAButtons>
            <PrimaryButton onClick={handleTryNow}>
              {state.logged_in_user ? 'Essayer gratuitement' : 'Commencer gratuitement'}
            </PrimaryButton>
            <SecondaryButton onClick={handleCreateAgent}>
              {state.logged_in_user ? 'Créer un agent' : 'Voir la démo'}
            </SecondaryButton>
          </CTAButtons>
        </HeroContainer>
      </HeroSection>

      <StatsSection>
        <StatsContainer>
          <StatsTitle>Concentrez-vous sur ce qui compte vraiment</StatsTitle>
          <StatsGrid>
            <StatCard>
              <StatIcon>🤖</StatIcon>
              <StatNumber>{agents.length}</StatNumber>
              <StatLabel>Agents IA</StatLabel>
              <StatDescription>
                Vos agents IA personnalisés travaillent 24h/24 pour automatiser vos tâches
              </StatDescription>
            </StatCard>
            <StatCard>
              <StatIcon>⚡</StatIcon>
              <StatNumber>24/7</StatNumber>
              <StatLabel>Disponibilité</StatLabel>
              <StatDescription>
                Vos agents ne dorment jamais et sont toujours prêts à vous aider
              </StatDescription>
            </StatCard>
            <StatCard>
              <StatIcon>🎯</StatIcon>
              <StatNumber>100%</StatNumber>
              <StatLabel>Automatisé</StatLabel>
              <StatDescription>
                Automatisez vos processus métier et gagnez du temps sur les tâches répétitives
              </StatDescription>
            </StatCard>
          </StatsGrid>
        </StatsContainer>
      </StatsSection>

      <AgentsSection>
        <AgentsContainer>
          <AgentsTitle>Vos agents IA personnalisés</AgentsTitle>
          
          {loading ? (
            <div style={{ textAlign: 'center', padding: '80px 24px' }}>
              <div style={{ fontSize: '2rem', marginBottom: '24px' }}>⏳</div>
              <p style={{ color: '#64748b' }}>Chargement de vos agents...</p>
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
              <CreateButton onClick={handleCreateAgent}>
                + Créer votre premier agent
              </CreateButton>
            </EmptyState>
          )}
        </AgentsContainer>
      </AgentsSection>
    </Container>
  );
};
