import React from 'react';
import styled from 'styled-components';

const Container = styled.div`
  padding: 15px 20px;
  background: white;
  border-top: 1px solid #e1e8ed;
`;

const ToggleButton = styled.button`
  display: block;
  margin: 0 auto 15px;
  padding: 8px 20px;
  background: linear-gradient(135deg, #3b82f6, #2e6bb4);
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-1px);
    box-shadow: 0 5px 15px rgba(59, 130, 246, 0.3);
  }
`;

const PromptsContainer = styled.div<{ showAll: boolean }>`
  display: ${props => props.showAll ? 'flex' : 'none'};
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
  margin-top: 10px;
`;

const PromptButton = styled.button`
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
    background: #3b82f6;
    color: white;
    border-color: #3b82f6;
    transform: translateY(-1px);
  }
`;

interface SuggestedPromptsProps {
  prompts: string[];
  onPromptClick: (prompt: string) => void;
  onShowSuggestions: () => void;
  showAll?: boolean;
}

export const SuggestedPrompts: React.FC<SuggestedPromptsProps> = ({
  prompts,
  onPromptClick,
  onShowSuggestions,
  showAll = false,
}) => {
  if (prompts.length === 0) return null;

  return (
    <Container>
      {!showAll && (
        <ToggleButton onClick={onShowSuggestions}>
          Afficher les suggestions de prompt
        </ToggleButton>
      )}
      
      <PromptsContainer showAll={showAll}>
        {prompts.map((prompt, index) => (
          <PromptButton
            key={index}
            onClick={() => onPromptClick(prompt)}
          >
            {prompt}
          </PromptButton>
        ))}
      </PromptsContainer>
    </Container>
  );
};

