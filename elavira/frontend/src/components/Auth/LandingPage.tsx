import React, { useState } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { useApp } from '../../context/AppContext';

const LandingContainer = styled.div`
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  flex-direction: column;
`;

const Header = styled.header`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 40px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
`;

const Logo = styled.div`
  font-size: 24px;
  font-weight: 700;
  color: white;
  display: flex;
  align-items: center;
  gap: 10px;
`;

const LogoIcon = styled.span`
  font-size: 28px;
`;

const NavLinks = styled.div`
  display: flex;
  gap: 30px;
  align-items: center;
`;

const NavLink = styled.a`
  color: white;
  text-decoration: none;
  font-weight: 500;
  transition: opacity 0.3s ease;
  
  &:hover {
    opacity: 0.8;
  }
`;

const AuthButtons = styled.div`
  display: flex;
  gap: 15px;
  align-items: center;
`;

const Button = styled.button<{ variant?: 'primary' | 'secondary' }>`
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  
  ${props => props.variant === 'primary' ? `
    background: white;
    color: #667eea;
    
    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
    }
  ` : `
    background: transparent;
    color: white;
    border: 2px solid white;
    
    &:hover {
      background: white;
      color: #667eea;
    }
  `}
`;

const HeroSection = styled.section`
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 80px 40px;
  text-align: center;
`;

const HeroContent = styled.div`
  max-width: 800px;
`;

const HeroTitle = styled.h1`
  font-size: 48px;
  font-weight: 800;
  margin-bottom: 20px;
  line-height: 1.2;
`;

const HeroSubtitle = styled.p`
  font-size: 20px;
  margin-bottom: 40px;
  opacity: 0.9;
  line-height: 1.6;
`;

const CTAButtons = styled.div`
  display: flex;
  gap: 20px;
  justify-content: center;
  margin-bottom: 60px;
`;

const CTAButton = styled.button<{ variant?: 'primary' | 'secondary' }>`
  padding: 16px 32px;
  border-radius: 12px;
  font-size: 18px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  
  ${props => props.variant === 'primary' ? `
    background: #ff6b6b;
    color: white;
    
    &:hover {
      background: #ff5252;
      transform: translateY(-3px);
      box-shadow: 0 15px 30px rgba(255, 107, 107, 0.4);
    }
  ` : `
    background: white;
    color: #667eea;
    
    &:hover {
      transform: translateY(-3px);
      box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
    }
  `}
`;

const FormationsSection = styled.section`
  background: #f8f9fa;
  padding: 80px 40px;
  color: #333;
`;

const FormationsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  max-width: 1200px;
  margin: 0 auto;
`;

const FormationCard = styled.div`
  background: white;
  border-radius: 16px;
  padding: 30px;
  text-align: center;
  transition: transform 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  
  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
  }
`;

const FormationIcon = styled.div`
  font-size: 48px;
  margin-bottom: 20px;
`;

const FormationTitle = styled.h3`
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 15px;
  color: #333;
`;

const FormationDescription = styled.p`
  color: #666;
  line-height: 1.6;
  margin-bottom: 20px;
`;

const FormationFeatures = styled.ul`
  list-style: none;
  padding: 0;
  margin: 20px 0;
  text-align: left;
`;

const AgentsSection = styled.section`
  background: white;
  padding: 80px 40px;
  color: #333;
`;

const SectionTitle = styled.h2`
  font-size: 36px;
  font-weight: 700;
  text-align: center;
  margin-bottom: 60px;
  color: #333;
`;

const AgentsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  max-width: 1200px;
  margin: 0 auto;
`;

const AgentCard = styled.div`
  background: #f8f9fa;
  border-radius: 16px;
  padding: 30px;
  text-align: center;
  transition: transform 0.3s ease;
  
  &:hover {
    transform: translateY(-5px);
  }
`;

const AgentIcon = styled.div`
  font-size: 48px;
  margin-bottom: 20px;
`;

const AgentName = styled.h3`
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 15px;
  color: #333;
`;

const AgentDescription = styled.p`
  color: #666;
  line-height: 1.6;
  margin-bottom: 20px;
`;

const AgentFeatures = styled.ul`
  list-style: none;
  padding: 0;
  margin: 20px 0;
`;

const FeatureItem = styled.li`
  padding: 5px 0;
  color: #555;
  
  &:before {
    content: "✓ ";
    color: #4CAF50;
    font-weight: bold;
  }
`;

const PricingSection = styled.section`
  background: #f8f9fa;
  padding: 80px 40px;
`;

const PricingGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  max-width: 1200px;
  margin: 0 auto;
`;

const PricingCard = styled.div<{ featured?: boolean }>`
  background: white;
  border-radius: 16px;
  padding: 40px 30px;
  text-align: center;
  position: relative;
  transition: transform 0.3s ease;
  
  ${props => props.featured && `
    border: 3px solid #ff6b6b;
    transform: scale(1.05);
  `}
  
  &:hover {
    transform: ${props => props.featured ? 'scale(1.08)' : 'translateY(-5px)'};
  }
`;

const PopularBadge = styled.div`
  position: absolute;
  top: -15px;
  left: 50%;
  transform: translateX(-50%);
  background: #ff6b6b;
  color: white;
  padding: 8px 20px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
`;

const PlanName = styled.h3`
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 10px;
  color: #333;
`;

const PlanPrice = styled.div`
  font-size: 36px;
  font-weight: 800;
  color: #ff6b6b;
  margin-bottom: 20px;
`;

const PlanDescription = styled.p`
  color: #666;
  margin-bottom: 30px;
`;

const PlanFeatures = styled.ul`
  list-style: none;
  padding: 0;
  margin: 30px 0;
`;

const PlanFeature = styled.li`
  padding: 10px 0;
  color: #555;
  
  &:before {
    content: "✓ ";
    color: #4CAF50;
    font-weight: bold;
  }
`;

const Footer = styled.footer`
  background: #333;
  color: white;
  padding: 40px;
  text-align: center;
`;

const LandingPage: React.FC = () => {
  const { dispatch } = useApp();
  const [isLoginModalOpen, setIsLoginModalOpen] = useState(false);

  const handleGetStarted = () => {
    dispatch({ type: 'SET_PAGE', payload: 'register' });
  };

  const handleLogin = () => {
    dispatch({ type: 'SET_PAGE', payload: 'login' });
  };

  const agents = [
    {
      name: 'Elavira',
      icon: '🎓',
      description: 'Spécialiste des formations professionnelles FormEduc',
      features: ['Secourisme 8h', 'Formations SST', 'Certifications reconnues', 'Support 24/7']
    },
    {
      name: 'Solenys',
      icon: '👨‍🏫',
      description: 'Professeur spécialisé dans l\'enseignement PFEQ',
      features: ['Mathématiques', 'Sciences', 'Français', 'Programme québécois']
    },
    {
      name: 'Créez votre agent',
      icon: '🤖',
      description: 'Créez votre propre agent IA personnalisé',
      features: ['Modèles IA avancés', 'Prompts personnalisés', 'RAG intégré', 'Outils configurables']
    }
  ];

  const plans = [
    {
      name: 'Découverte',
      price: 'Gratuit',
      description: 'Parfait pour découvrir FormEduc',
      features: ['Elavira & Solenys', 'Chat illimité', 'Formations de base', 'Support email'],
      featured: false
    },
    {
      name: 'Professionnel',
      price: '49€/mois',
      description: 'Solution complète pour les professionnels',
      features: ['Tous les agents', 'Création d\'agents', 'Formations certifiantes', 'Support prioritaire', 'API access'],
      featured: true
    },
    {
      name: 'Entreprise',
      price: 'Sur mesure',
      description: 'Solution sur mesure pour les entreprises',
      features: ['Agents personnalisés', 'Formations en entreprise', 'Intégrations CRM', 'Support dédié', 'Formation équipe'],
      featured: false
    }
  ];

  return (
    <LandingContainer>
      <Header>
        <Logo>
          <LogoIcon>🎓</LogoIcon>
          FormEduc.ai
        </Logo>
        <NavLinks>
          <NavLink href="#formations">Formations</NavLink>
          <NavLink href="#agents">Agents IA</NavLink>
          <NavLink href="#pricing">Tarifs</NavLink>
          <NavLink href="#contact">Contact</NavLink>
        </NavLinks>
        <AuthButtons>
          <Button onClick={handleLogin}>Se connecter</Button>
          <Button variant="primary" onClick={handleGetStarted}>
            Essayer gratuitement
          </Button>
        </AuthButtons>
      </Header>

      <HeroSection>
        <HeroContent>
          <HeroTitle>
            Formation professionnelle intelligente avec l'IA
          </HeroTitle>
          <HeroSubtitle>
            FormEduc.ai révolutionne la formation professionnelle avec des agents IA spécialisés.
            Secourisme, SST, formations en entreprise - disponible 24h/7j.
          </HeroSubtitle>
          <CTAButtons>
            <CTAButton variant="primary" onClick={handleGetStarted}>
              Essayer gratuitement
            </CTAButton>
            <CTAButton onClick={() => {/* Book demo */}}>
              Réserver une démo
            </CTAButton>
          </CTAButtons>
        </HeroContent>
      </HeroSection>

      <FormationsSection id="formations">
        <SectionTitle>Nos formations professionnelles</SectionTitle>
        <FormationsGrid>
          <FormationCard>
            <FormationIcon>🚑</FormationIcon>
            <FormationTitle>Secourisme</FormationTitle>
            <FormationDescription>
              Formations de secourisme adaptées à la petite enfance et milieu scolaire
            </FormationDescription>
            <FormationFeatures>
              <li>Secourisme petite enfance (8h)</li>
              <li>Secourisme milieu scolaire</li>
              <li>Renouvellement de certifications</li>
              <li>Formations chauffeurs d'autobus</li>
            </FormationFeatures>
          </FormationCard>
          
          <FormationCard>
            <FormationIcon>🏠</FormationIcon>
            <FormationTitle>Service de garde</FormationTitle>
            <FormationDescription>
              Formation complète 45h pour RSG et RSGE
            </FormationDescription>
            <FormationFeatures>
              <li>Programme éducatif</li>
              <li>Développement de l'enfant</li>
              <li>Santé, sécurité et alimentation</li>
              <li>Rôle de la responsable</li>
            </FormationFeatures>
          </FormationCard>
          
          <FormationCard>
            <FormationIcon>👨‍👩‍👧‍👦</FormationIcon>
            <FormationTitle>Familles d'accueil</FormationTitle>
            <FormationDescription>
              Formations hybrides spécialisées pour familles d'accueil
            </FormationDescription>
            <FormationFeatures>
              <li>Formation hybride secourisme</li>
              <li>Développement de l'enfant</li>
              <li>Gestion des allergies</li>
              <li>Prévention maltraitance</li>
            </FormationFeatures>
          </FormationCard>
        </FormationsGrid>
      </FormationsSection>

      <AgentsSection id="agents">
        <SectionTitle>Vos assistants IA FormEduc</SectionTitle>
        <AgentsGrid>
          {agents.map((agent, index) => (
            <motion.div
              key={agent.name}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.2 }}
            >
              <AgentCard>
                <AgentIcon>{agent.icon}</AgentIcon>
                <AgentName>{agent.name}</AgentName>
                <AgentDescription>{agent.description}</AgentDescription>
                <AgentFeatures>
                  {agent.features.map((feature, idx) => (
                    <FeatureItem key={idx}>{feature}</FeatureItem>
                  ))}
                </AgentFeatures>
              </AgentCard>
            </motion.div>
          ))}
        </AgentsGrid>
      </AgentsSection>

      <PricingSection id="pricing">
        <SectionTitle>Nos offres</SectionTitle>
        <PricingGrid>
          {plans.map((plan, index) => (
            <motion.div
              key={plan.name}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.2 }}
            >
              <PricingCard featured={plan.featured}>
                {plan.featured && <PopularBadge>Populaire</PopularBadge>}
                <PlanName>{plan.name}</PlanName>
                <PlanPrice>{plan.price}</PlanPrice>
                <PlanDescription>{plan.description}</PlanDescription>
                <PlanFeatures>
                  {plan.features.map((feature, idx) => (
                    <PlanFeature key={idx}>{feature}</PlanFeature>
                  ))}
                </PlanFeatures>
                <CTAButton 
                  variant={plan.featured ? "primary" : "secondary"}
                  onClick={handleGetStarted}
                >
                  Commencer
                </CTAButton>
              </PricingCard>
            </motion.div>
          ))}
        </PricingGrid>
      </PricingSection>

      <Footer>
        <p>&copy; 2025 FormEduc.ai. Tous droits réservés.</p>
        <p>Contact: contact@formeduc.ai | +1 (418) 842-7523</p>
        <p>5121 ave Chauveau Ouest, Québec, QC G2E 5A6 local 101</p>
      </Footer>
    </LandingContainer>
  );
};

export default LandingPage;
