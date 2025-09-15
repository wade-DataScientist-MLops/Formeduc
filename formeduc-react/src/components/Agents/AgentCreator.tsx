import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { AgentTemplate, CreateAgentRequest, Agent } from '../../types/agent';
import { agentTemplates, getTemplateById } from '../../data/agentTemplates';

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
  border-radius: 20px;
  padding: 30px;
  max-width: 600px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
`;

const ModalHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 2px solid #e1e8ed;
`;

const ModalTitle = styled.h2`
  color: #2c3e50;
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0;
`;

const CloseButton = styled.button`
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #6c757d;
  cursor: pointer;
  padding: 5px;
  border-radius: 50%;
  transition: all 0.3s ease;

  &:hover {
    background: #f8f9fa;
    color: #2c3e50;
  }
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 20px;
`;

const FormGroup = styled.div`
  display: flex;
  flex-direction: column;
  gap: 8px;
`;

const Label = styled.label`
  font-weight: 600;
  color: #2c3e50;
  font-size: 0.9rem;
`;

const Input = styled.input`
  padding: 12px 15px;
  border: 2px solid #e1e8ed;
  border-radius: 10px;
  font-size: 1rem;
  transition: all 0.3s ease;

  &:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }

  &::placeholder {
    color: #a0aec0;
  }
`;

const TextArea = styled.textarea`
  padding: 12px 15px;
  border: 2px solid #e1e8ed;
  border-radius: 10px;
  font-size: 1rem;
  min-height: 100px;
  resize: vertical;
  font-family: inherit;
  transition: all 0.3s ease;

  &:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }

  &::placeholder {
    color: #a0aec0;
  }
`;

const Select = styled.select`
  padding: 12px 15px;
  border: 2px solid #e1e8ed;
  border-radius: 10px;
  font-size: 1rem;
  background: white;
  cursor: pointer;
  transition: all 0.3s ease;

  &:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }
`;

const TemplateSelector = styled.div`
  display: flex;
  flex-direction: column;
  gap: 10px;
`;

const TemplateGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 10px;
`;

const TemplateCard = styled.div<{ selected: boolean }>`
  padding: 15px;
  border: 2px solid ${props => props.selected ? '#3b82f6' : '#e1e8ed'};
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
  background: ${props => props.selected ? '#f0f8ff' : 'white'};

  &:hover {
    border-color: #3b82f6;
    transform: translateY(-2px);
  }
`;

const TemplateIcon = styled.div`
  font-size: 2rem;
  text-align: center;
  margin-bottom: 10px;
`;

const TemplateName = styled.div`
  font-weight: 600;
  color: #2c3e50;
  text-align: center;
  font-size: 0.9rem;
`;

const ButtonGroup = styled.div`
  display: flex;
  gap: 15px;
  justify-content: flex-end;
  margin-top: 25px;
  padding-top: 20px;
  border-top: 2px solid #e1e8ed;
`;

const Button = styled.button<{ variant?: 'primary' | 'secondary' }>`
  padding: 12px 24px;
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;

  ${props => props.variant === 'primary' ? `
    background: #3b82f6;
    color: white;
    
    &:hover {
      background: #2e6bb4;
      transform: translateY(-1px);
    }
  ` : `
    background: #f8f9fa;
    color: #6c757d;
    border: 2px solid #e1e8ed;
    
    &:hover {
      background: #e9ecef;
      color: #2c3e50;
    }
  `}
`;

interface AgentCreatorProps {
  isOpen: boolean;
  onClose: () => void;
  onSave: (agent: CreateAgentRequest) => void;
  existingAgents?: Agent[];
}

export const AgentCreator: React.FC<AgentCreatorProps> = ({
  isOpen,
  onClose,
  onSave,
  existingAgents = []
}) => {
  const [selectedTemplate, setSelectedTemplate] = useState<AgentTemplate | null>(null);
  const [formData, setFormData] = useState<CreateAgentRequest>({
    name: '',
    role: '',
    specialty: '',
    description: '',
    prompt: '',
    model: 'llama3.2:1b',
    avatar: '🤖',
    color: '#6b7280',
    knowledgeBase: 'custom'
  });

  useEffect(() => {
    if (selectedTemplate) {
      setFormData(prev => ({
        ...prev,
        prompt: selectedTemplate.defaultPrompt,
        model: selectedTemplate.defaultModel,
        avatar: selectedTemplate.defaultAvatar,
        color: selectedTemplate.defaultColor,
        knowledgeBase: selectedTemplate.suggestedKnowledgeBase
      }));
    }
  }, [selectedTemplate]);

  const handleTemplateSelect = (template: AgentTemplate) => {
    setSelectedTemplate(template);
  };

  const handleInputChange = (field: keyof CreateAgentRequest, value: string) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    // Vérifier que le nom est unique
    const isNameUnique = !existingAgents.some(agent => 
      agent.name.toLowerCase() === formData.name.toLowerCase()
    );
    
    if (!isNameUnique) {
      alert('Un agent avec ce nom existe déjà. Veuillez choisir un autre nom.');
      return;
    }

    onSave(formData);
    onClose();
  };

  const generateUniqueId = () => {
    return `agent-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  };

  if (!isOpen) return null;

  return (
    <ModalOverlay onClick={onClose}>
      <ModalContent onClick={e => e.stopPropagation()}>
        <ModalHeader>
          <ModalTitle>Créer un nouvel agent</ModalTitle>
          <CloseButton onClick={onClose}>×</CloseButton>
        </ModalHeader>

        <Form onSubmit={handleSubmit}>
          <TemplateSelector>
            <Label>Choisir un template</Label>
            <TemplateGrid>
              {agentTemplates.map(template => (
                <TemplateCard
                  key={template.id}
                  selected={selectedTemplate?.id === template.id}
                  onClick={() => handleTemplateSelect(template)}
                >
                  <TemplateIcon>{template.defaultAvatar}</TemplateIcon>
                  <TemplateName>{template.name}</TemplateName>
                </TemplateCard>
              ))}
            </TemplateGrid>
          </TemplateSelector>

          {selectedTemplate && (
            <>
              {selectedTemplate.fields.map(field => (
                <FormGroup key={field.name}>
                  <Label>
                    {field.label}
                    {field.required && ' *'}
                  </Label>
                  {field.type === 'textarea' ? (
                    <TextArea
                      value={formData[field.name as keyof CreateAgentRequest] as string || ''}
                      onChange={(e) => handleInputChange(field.name as keyof CreateAgentRequest, e.target.value)}
                      placeholder={field.placeholder}
                      required={field.required}
                    />
                  ) : field.type === 'select' ? (
                    <Select
                      value={formData[field.name as keyof CreateAgentRequest] as string || ''}
                      onChange={(e) => handleInputChange(field.name as keyof CreateAgentRequest, e.target.value)}
                      required={field.required}
                    >
                      <option value="">Sélectionner...</option>
                      {field.options?.map(option => (
                        <option key={option} value={option}>{option}</option>
                      ))}
                    </Select>
                  ) : (
                    <Input
                      type={field.type}
                      value={formData[field.name as keyof CreateAgentRequest] as string || ''}
                      onChange={(e) => handleInputChange(field.name as keyof CreateAgentRequest, e.target.value)}
                      placeholder={field.placeholder}
                      required={field.required}
                    />
                  )}
                </FormGroup>
              ))}
            </>
          )}

          <ButtonGroup>
            <Button type="button" onClick={onClose}>
              Annuler
            </Button>
            <Button type="submit" variant="primary" disabled={!selectedTemplate}>
              Créer l'agent
            </Button>
          </ButtonGroup>
        </Form>
      </ModalContent>
    </ModalOverlay>
  );
};
