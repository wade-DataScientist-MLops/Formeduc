import React from 'react';
import styled from 'styled-components';
import { ImageCarousel } from '../ImageCarousel/ImageCarousel';

const ShowcaseContainer = styled.div`
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  padding: 30px 20px;
  border-radius: 20px;
  margin: 20px 0;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
`;

const ShowcaseTitle = styled.h2`
  text-align: center;
  color: #2c3e50;
  font-size: 1.8rem;
  font-weight: 600;
  margin-bottom: 20px;
`;

const ShowcaseSubtitle = styled.p`
  text-align: center;
  color: #6c757d;
  font-size: 1rem;
  margin-bottom: 30px;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
`;

const CarouselWrapper = styled.div`
  max-width: 800px;
  margin: 0 auto;
`;

// Données des assistants pour le showcase
const assistantsShowcaseData = [
  {
    id: 'elavira-showcase',
    image: '/images/elavira_assistant.png',
    name: '👩‍🏫 Elavira - Experte Formations',
    description: 'Professionnelle de la santé et de l\'éducation, Elavira vous accompagne dans vos formations de secourisme avec expertise et bienveillance. Elle porte des lunettes et un stéthoscope, symboles de son professionnalisme.',
    features: ['Formations certifiantes', 'Secourisme adapté', 'Prévention des risques', 'Accompagnement personnalisé']
  },
  {
    id: 'solenys-showcase',
    image: '/images/solenys-banner.jpg',
    name: '🤖 Solenys - Assistant IA',
    description: 'Assistant intelligent de nouvelle génération en uniforme futuriste, Solenys utilise la technologie avancée pour répondre à toutes vos questions avec précision et efficacité.',
    features: ['IA Conversationnelle', 'Technologie avancée', 'Support 24/7', 'Réponses précises']
  }
];

export const AssistantShowcase: React.FC = () => {
  return (
    <ShowcaseContainer>
      <ShowcaseTitle>Découvrez nos Assistants Intelligents</ShowcaseTitle>
      <ShowcaseSubtitle>
        Choisissez l'assistant qui correspond le mieux à vos besoins et commencez votre conversation
      </ShowcaseSubtitle>
      <CarouselWrapper>
        <ImageCarousel 
          items={assistantsShowcaseData}
          autoPlay={true}
          autoPlayInterval={6000}
        />
      </CarouselWrapper>
    </ShowcaseContainer>
  );
};
