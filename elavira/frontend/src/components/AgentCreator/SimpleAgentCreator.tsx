import React, { useState } from 'react';
import styled from 'styled-components';

const ModalOverlay = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
`;

const ModalContent = styled.div`
  background: white;
  border-radius: 12px;
  padding: 30px;
  width: 500px;
  max-height: 80vh;
  overflow-y: auto;
`;

const Title = styled.h2`
  margin: 0 0 20px 0;
  color: #333;
`;

const FormGroup = styled.div`
  margin-bottom: 20px;
`;

const Label = styled.label`
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  color: #333;
`;

const Input = styled.input`
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
`;

const TextArea = styled.textarea`
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  min-height: 80px;
  resize: vertical;
`;

const ButtonGroup = styled.div`
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 20px;
`;

const Button = styled.button<{ variant?: string }>`
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  
  ${props => props.variant === 'primary' ? `
    background: #3b82f6;
    color: white;
    
    &:hover {
      background: #2563eb;
    }
  ` : `
    background: #f3f4f6;
    color: #374151;
    
    &:hover {
      background: #e5e7eb;
    }
  `}
`;

interface SimpleAgentCreatorProps {
  isOpen: boolean;
  onClose: () => void;
  onAgentCreated: (agent: any) => void;
}

const SimpleAgentCreator: React.FC<SimpleAgentCreatorProps> = ({ isOpen, onClose, onAgentCreated }) => {
  const [formData, setFormData] = useState({
    name: '',
    role: '',
    description: '',
    model: 'qwen2.5:7b',
    systemPrompt: 'You are a helpful assistant'
  });

  const handleSubmit = async () => {
    try {
      alert('handleSubmit appelé !'); // Test immédiat
      console.log('SimpleAgentCreator - Données du formulaire:', formData);
      
      const response = await fetch('http://104.254.182.118:8000/api/agents', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...formData,
          timeout: 30000,
          temperature: 0.6,
          maxTokens: 400,
          topK: 40,
          topP: 0.9,
          repetitionPenalty: 1.0,
          stopWords: "User:\nAssistant:",
          tools: { "rag.search": true },
          knowledgePacks: { "enseignement": true }
        }),
      });

      console.log('SimpleAgentCreator - Réponse API:', response.status, response.statusText);

      if (response.ok) {
        const newAgent = await response.json();
        console.log('SimpleAgentCreator - Agent créé:', newAgent);
        onAgentCreated(newAgent);
        onClose();
        alert('Agent créé avec succès !');
      } else {
        const errorData = await response.text();
        console.error('SimpleAgentCreator - Erreur:', response.status, errorData);
        alert(`Erreur ${response.status}: ${errorData}`);
      }
    } catch (error) {
      console.error('SimpleAgentCreator - Erreur:', error);
      alert(`Erreur de connexion: ${error instanceof Error ? error.message : 'Erreur inconnue'}`);
    }
  };

  if (!isOpen) return null;

  return (
    <ModalOverlay onClick={onClose}>
      <ModalContent onClick={(e) => e.stopPropagation()}>
        <Title>Créer un nouvel agent</Title>
        
        <FormGroup>
          <Label>Nom de l'agent *</Label>
          <Input
            type="text"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            placeholder="Ex: Mon Assistant"
          />
        </FormGroup>

        <FormGroup>
          <Label>Rôle *</Label>
          <Input
            type="text"
            value={formData.role}
            onChange={(e) => setFormData({ ...formData, role: e.target.value })}
            placeholder="Ex: Assistant spécialisé"
          />
        </FormGroup>

        <FormGroup>
          <Label>Description *</Label>
          <TextArea
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            placeholder="Décrivez le rôle et les capacités de cet agent..."
          />
        </FormGroup>

        <FormGroup>
          <Label>Modèle IA *</Label>
          <Input
            type="text"
            value={formData.model}
            onChange={(e) => setFormData({ ...formData, model: e.target.value })}
          />
        </FormGroup>

        <FormGroup>
          <Label>Prompt système</Label>
          <TextArea
            value={formData.systemPrompt}
            onChange={(e) => setFormData({ ...formData, systemPrompt: e.target.value })}
            placeholder="Instructions pour l'agent..."
          />
        </FormGroup>

        <ButtonGroup>
          <Button onClick={onClose}>Annuler</Button>
          <Button variant="primary" onClick={() => {
            alert('Bouton cliqué !'); // Test du bouton
            handleSubmit();
          }}>
            Créer l'agent
          </Button>
        </ButtonGroup>
      </ModalContent>
    </ModalOverlay>
  );
};

export default SimpleAgentCreator;
