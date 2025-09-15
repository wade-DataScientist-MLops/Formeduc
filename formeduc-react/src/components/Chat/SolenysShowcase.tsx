import React from 'react';
import styled from 'styled-components';

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

const AgentCard = styled.div`
  background: white;
  border-radius: 15px;
  padding: 25px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
  max-width: 500px;
  margin: 0 auto;
`;

const AgentAvatar = styled.div`
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  margin: 0 auto 20px;
  box-shadow: 0 5px 15px rgba(240, 147, 251, 0.3);
`;

const AgentName = styled.h3`
  color: #2c3e50;
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 10px;
`;

const AgentTitle = styled.p`
  color: #6c757d;
  font-size: 1rem;
  margin-bottom: 15px;
  font-weight: 500;
`;

const AgentDescription = styled.p`
  color: #495057;
  font-size: 0.9rem;
  line-height: 1.5;
  margin-bottom: 25px;
`;

const SubjectButtons = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
  margin-bottom: 20px;
`;

const SubjectButton = styled.button`
  padding: 8px 16px;
  background: #f8f9fa;
  color: #2c3e50;
  border: 2px solid #e1e8ed;
  border-radius: 20px;
  cursor: pointer;
  font-size: 0.85rem;
  transition: all 0.3s ease;
  white-space: nowrap;

  &:hover {
    background: #f093fb;
    color: white;
    border-color: #f093fb;
    transform: translateY(-1px);
  }
`;

const TopicButtons = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
`;

const TopicButton = styled.button`
  padding: 6px 14px;
  background: #e1f0ff;
  color: #2c3e50;
  border: 2px solid #b3d9ff;
  border-radius: 15px;
  cursor: pointer;
  font-size: 0.8rem;
  transition: all 0.3s ease;
  white-space: nowrap;

  &:hover {
    background: #3b82f6;
    color: white;
    border-color: #3b82f6;
    transform: translateY(-1px);
  }
`;

interface SolenysShowcaseProps {
  onSubjectClick?: (subject: string) => void;
  onTopicClick?: (topic: string) => void;
}

export const SolenysShowcase: React.FC<SolenysShowcaseProps> = ({
  onSubjectClick,
  onTopicClick,
}) => {
  const subjects = [
    'Mathématiques',
    'Physique',
    'Chimie',
    'Biologie',
    'Français',
    'Histoire',
    'Géographie',
    'Anglais'
  ];

  const topics = [
    'Aide en mathématiques',
    'Problèmes de physique',
    'Questions de chimie',
    'Français et littérature',
    'Histoire du Québec',
    'Géographie'
  ];

  return (
    <ShowcaseContainer>
      <ShowcaseTitle>🤖 Solenys - Professeur Québécois</ShowcaseTitle>
      <ShowcaseSubtitle>
        Votre professeur spécialisé dans l'enseignement secondaire selon le programme PFEQ du Québec
      </ShowcaseSubtitle>
      
      <AgentCard>
        <AgentAvatar>🤖</AgentAvatar>
        <AgentName>Solenys</AgentName>
        <AgentTitle>Professeur québécois</AgentTitle>
        <AgentDescription>
          Votre professeur spécialisé dans l'enseignement secondaire selon le programme PFEQ du Québec. 
          Je suis là pour vous accompagner dans votre apprentissage et vous aider à réussir !
        </AgentDescription>
        
        <SubjectButtons>
          {subjects.map((subject) => (
            <SubjectButton
              key={subject}
              onClick={() => onSubjectClick?.(subject)}
            >
              {subject}
            </SubjectButton>
          ))}
        </SubjectButtons>
        
        <TopicButtons>
          {topics.map((topic) => (
            <TopicButton
              key={topic}
              onClick={() => onTopicClick?.(topic)}
            >
              {topic}
            </TopicButton>
          ))}
        </TopicButtons>
      </AgentCard>
    </ShowcaseContainer>
  );
};
