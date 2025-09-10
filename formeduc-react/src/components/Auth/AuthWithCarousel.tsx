import React from 'react';
import styled from 'styled-components';
import { AuthForm } from './AuthForm';
import { ImageCarousel } from '../ImageCarousel/ImageCarousel';

const AuthPageContainer = styled.div`
  display: flex;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
`;

const CarouselSection = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 40px;
  position: relative;
  
  @media (max-width: 768px) {
    display: none;
  }
`;

const AuthSection = styled.div`
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  min-width: 400px;
  
  @media (max-width: 768px) {
    flex: 1;
    min-width: auto;
  }
`;

const CarouselTitle = styled.h1`
  color: white;
  font-size: 2.5rem;
  font-weight: 700;
  text-align: center;
  margin-bottom: 30px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
`;

const CarouselSubtitle = styled.p`
  color: rgba(255, 255, 255, 0.9);
  font-size: 1.2rem;
  text-align: center;
  margin-bottom: 40px;
  max-width: 500px;
  line-height: 1.6;
`;

const CarouselWrapper = styled.div`
  width: 100%;
  max-width: 600px;
`;

// Données des assistants pour le carrousel
const assistantsData = [
  {
    id: 'elavira',
    image: '/images/elavira_assistant.png',
    name: '👩‍🏫 Elavira - Experte Formations',
    description: 'Professionnelle de la santé et de l\'éducation, Elavira vous accompagne dans vos formations de secourisme avec expertise et bienveillance.',
    features: ['Formations certifiantes', 'Secourisme adapté', 'Prévention des risques', 'Accompagnement personnalisé']
  },
  {
    id: 'solenys',
    image: '/images/solenys-banner.jpg',
    name: '🤖 Solenys - Assistant IA',
    description: 'Assistant intelligent de nouvelle génération, Solenys utilise la technologie avancée pour répondre à toutes vos questions.',
    features: ['IA Conversationnelle', 'Technologie avancée', 'Support 24/7', 'Réponses précises']
  }
];

export const AuthWithCarousel: React.FC = () => {
  return (
    <AuthPageContainer>
      <CarouselSection>
        <CarouselTitle>Bienvenue sur Formeduc</CarouselTitle>
        <CarouselSubtitle>
          Découvrez nos assistants intelligents qui vous accompagneront dans vos formations
        </CarouselSubtitle>
        <CarouselWrapper>
          <ImageCarousel 
            items={assistantsData}
            autoPlay={true}
            autoPlayInterval={4000}
          />
        </CarouselWrapper>
      </CarouselSection>
      
      <AuthSection>
        <AuthForm />
      </AuthSection>
    </AuthPageContainer>
  );
};
