import React, { useState } from 'react';
import styled from 'styled-components';
// import { motion } from 'framer-motion';

interface AgentCreatorModalProps {
  isOpen: boolean;
  onClose: () => void;
  onAgentCreated: (agent: any) => void;
}

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
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
`;

const ModalHeader = styled.div`
  padding: 24px 24px 0;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const ModalTitle = styled.h2`
  font-size: 24px;
  font-weight: 600;
  color: #111827;
  margin: 0;
`;

const CloseButton = styled.button`
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #6b7280;
  padding: 4px;
  
  &:hover {
    color: #374151;
  }
`;

const TabContainer = styled.div`
  display: flex;
  border-bottom: 1px solid #e5e7eb;
  margin-top: 16px;
`;

const Tab = styled.button<{ active: boolean }>`
  padding: 12px 20px;
  border: none;
  background: none;
  cursor: pointer;
  font-weight: 500;
  color: ${props => props.active ? '#3b82f6' : '#6b7280'};
  border-bottom: 2px solid ${props => props.active ? '#3b82f6' : 'transparent'};
  display: flex;
  align-items: center;
  gap: 8px;
  
  &:hover {
    color: #3b82f6;
  }
`;

const TabIcon = styled.span`
  font-size: 16px;
`;

const TabContent = styled.div`
  padding: 24px;
`;

const FormGroup = styled.div`
  margin-bottom: 20px;
`;

const Label = styled.label`
  display: block;
  font-weight: 500;
  color: #374151;
  margin-bottom: 8px;
  font-size: 14px;
`;

const Required = styled.span`
  color: #ef4444;
  margin-left: 4px;
`;

const Input = styled.input`
  width: 100%;
  padding: 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
  
  &:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }
`;

const TextArea = styled.textarea`
  width: 100%;
  padding: 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
  min-height: 120px;
  resize: vertical;
  
  &:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }
`;

const Select = styled.select`
  width: 100%;
  padding: 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
  background: white;
  
  &:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }
`;

const CheckboxGroup = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
`;

const CheckboxItem = styled.label`
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-size: 14px;
  color: #374151;
`;

const Checkbox = styled.input`
  width: 16px;
  height: 16px;
`;

const ButtonGroup = styled.div`
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  padding: 24px;
  border-top: 1px solid #e5e7eb;
`;

const Button = styled.button<{ variant?: 'primary' | 'secondary' }>`
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  border: none;
  
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

const Slider = styled.input`
  width: 100%;
  margin: 8px 0;
`;

const SliderValue = styled.span`
  font-weight: 500;
  color: #3b82f6;
`;

const TipBox = styled.div`
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  border-radius: 8px;
  padding: 16px;
  margin-top: 16px;
`;

const TipTitle = styled.h4`
  margin: 0 0 8px 0;
  color: #1e40af;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 8px;
`;

const TipText = styled.p`
  margin: 0;
  font-size: 13px;
  color: #1e40af;
  line-height: 1.4;
`;

const AgentCreatorModal: React.FC<AgentCreatorModalProps> = ({ isOpen, onClose, onAgentCreated }) => {
  const [activeTab, setActiveTab] = useState('general');
  
  // Debug
  console.log('AgentCreatorModal - isOpen:', isOpen);
  const [formData, setFormData] = useState({
    // General
    name: '',
    role: '',
    description: '',
    model: 'qwen2.5:7b',
    timeout: 30000,
    
    // Model
    temperature: 0.6,
    maxTokens: 400,
    topK: 40,
    topP: 0.9,
    repetitionPenalty: 1.0,
    stopWords: 'User:\nÉlève:\nAssistant:',
    
    // Prompt
    systemPrompt: '',
    
    // Tools
    tools: {
      'rag.search': true,
      'rag.add_document': true,
      'rag.answer': true,
      'file.read': true,
      'file.write': true,
      'math.evaluate': true,
      'few-shot': true
    },
    
    // Knowledge Packs
    knowledgePacks: {
      'enseignement': true,
      'pedagogie': true
    }
  });

  const models = [
    'qwen2.5:7b',
    'qwen2:1.5b',
    'llama3.2:1b',
    'llama3.2:3b',
    'mistral:7b',
    'codellama:7b'
  ];

  const handleInputChange = (field: string, value: any) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleToolChange = (tool: string, enabled: boolean) => {
    setFormData(prev => ({
      ...prev,
      tools: {
        ...prev.tools,
        [tool]: enabled
      }
    }));
  };

  const handleKnowledgePackChange = (pack: string, enabled: boolean) => {
    setFormData(prev => ({
      ...prev,
      knowledgePacks: {
        ...prev.knowledgePacks,
        [pack]: enabled
      }
    }));
  };

  const handleSubmit = async () => {
    try {
      console.log('Données du formulaire:', formData);
      
      // Créer l'agent via l'API
      const response = await fetch('http://104.254.182.118:8000/api/agents', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: formData.name,
          role: formData.role,
          description: formData.description,
          model: formData.model,
          prompt: formData.systemPrompt
        }),
      });

      console.log('Réponse API:', response.status, response.statusText);

      if (response.ok) {
        const newAgent = await response.json();
        console.log('Agent créé:', newAgent);
        onAgentCreated(newAgent);
        onClose();
        
        // Reset form
        setFormData({
          name: '',
          role: '',
          description: '',
          model: 'qwen2.5:7b',
          timeout: 30000,
          temperature: 0.6,
          maxTokens: 400,
          topK: 40,
          topP: 0.9,
          repetitionPenalty: 1.0,
          stopWords: 'User:\nÉlève:\nAssistant:',
          systemPrompt: '',
          tools: {
            'rag.search': true,
            'rag.add_document': true,
            'rag.answer': true,
            'file.read': true,
            'file.write': true,
            'math.evaluate': true,
            'few-shot': true
          },
          knowledgePacks: {
            'enseignement': true,
            'pedagogie': true
          }
        });
      }
    } catch (error) {
      console.error('Error creating agent:', error);
      alert(`Erreur de connexion: ${error instanceof Error ? error.message : 'Erreur inconnue'}`);
    }
  };

  const tabs = [
    { id: 'general', label: 'Général', icon: '⚙️' },
    { id: 'model', label: 'Modèle', icon: '🧠' },
    { id: 'prompt', label: 'Prompt', icon: '💬' },
    { id: 'tools', label: 'Outils', icon: '🔧' }
  ];

  if (!isOpen) return null;

  return (
    <ModalOverlay onClick={onClose}>
      <ModalContent onClick={(e) => e.stopPropagation()}>
            <ModalHeader>
              <ModalTitle>Créer un nouvel agent</ModalTitle>
              <CloseButton onClick={onClose}>×</CloseButton>
            </ModalHeader>

            <TabContainer>
              {tabs.map(tab => (
                <Tab
                  key={tab.id}
                  active={activeTab === tab.id}
                  onClick={() => setActiveTab(tab.id)}
                >
                  <TabIcon>{tab.icon}</TabIcon>
                  {tab.label}
                </Tab>
              ))}
            </TabContainer>

            <TabContent>
              {activeTab === 'general' && (
                <>
                  <FormGroup>
                    <Label>
                      Nom de l'agent <Required>*</Required>
                    </Label>
                    <Input
                      type="text"
                      value={formData.name}
                      onChange={(e) => handleInputChange('name', e.target.value)}
                      placeholder="Ex: Mon Assistant IA"
                    />
                  </FormGroup>

                  <FormGroup>
                    <Label>
                      Rôle <Required>*</Required>
                    </Label>
                    <Input
                      type="text"
                      value={formData.role}
                      onChange={(e) => handleInputChange('role', e.target.value)}
                      placeholder="Ex: Assistant pédagogique"
                    />
                  </FormGroup>

                  <FormGroup>
                    <Label>
                      Description <Required>*</Required>
                    </Label>
                    <TextArea
                      value={formData.description}
                      onChange={(e) => handleInputChange('description', e.target.value)}
                      placeholder="Décrivez le rôle et les capacités de votre agent..."
                    />
                  </FormGroup>

                  <FormGroup>
                    <Label>
                      Modèle IA <Required>*</Required>
                    </Label>
                    <Select
                      value={formData.model}
                      onChange={(e) => handleInputChange('model', e.target.value)}
                    >
                      {models.map(model => (
                        <option key={model} value={model}>{model}</option>
                      ))}
                    </Select>
                  </FormGroup>

                  <FormGroup>
                    <Label>Timeout de chat (ms)</Label>
                    <Input
                      type="number"
                      value={formData.timeout}
                      onChange={(e) => handleInputChange('timeout', parseInt(e.target.value))}
                    />
                  </FormGroup>
                </>
              )}

              {activeTab === 'model' && (
                <>
                  <h3>Configuration du modèle</h3>
                  <p>Configurez les paramètres de génération du modèle pour cet agent</p>

                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
                    <div>
                      <FormGroup>
                        <Label>
                          Température <SliderValue>{formData.temperature}</SliderValue>
                        </Label>
                        <Slider
                          type="range"
                          min="0"
                          max="2"
                          step="0.1"
                          value={formData.temperature}
                          onChange={(e) => handleInputChange('temperature', parseFloat(e.target.value))}
                        />
                        <small>0.0 (Déterministe) - 2.0 (Créatif)</small>
                      </FormGroup>

                      <FormGroup>
                        <Label>Nombre max de tokens</Label>
                        <Input
                          type="number"
                          value={formData.maxTokens}
                          onChange={(e) => handleInputChange('maxTokens', parseInt(e.target.value))}
                          min="10"
                          max="2000"
                        />
                        <small>Nombre maximum de tokens à générer (10-2000)</small>
                      </FormGroup>

                      <FormGroup>
                        <Label>Top-K</Label>
                        <Input
                          type="number"
                          value={formData.topK}
                          onChange={(e) => handleInputChange('topK', parseInt(e.target.value))}
                          min="1"
                          max="100"
                        />
                        <small>Limite le nombre de tokens candidats (1-100)</small>
                      </FormGroup>
                    </div>

                    <div>
                      <FormGroup>
                        <Label>
                          Top-P <SliderValue>{formData.topP}</SliderValue>
                        </Label>
                        <Slider
                          type="range"
                          min="0"
                          max="1"
                          step="0.1"
                          value={formData.topP}
                          onChange={(e) => handleInputChange('topP', parseFloat(e.target.value))}
                        />
                        <small>0.0 (Conservateur) - 1.0 (Diversifié)</small>
                      </FormGroup>

                      <FormGroup>
                        <Label>
                          Pénalité de répétition <SliderValue>{formData.repetitionPenalty}</SliderValue>
                        </Label>
                        <Slider
                          type="range"
                          min="0.5"
                          max="2"
                          step="0.1"
                          value={formData.repetitionPenalty}
                          onChange={(e) => handleInputChange('repetitionPenalty', parseFloat(e.target.value))}
                        />
                        <small>0.5 (Répétitif) - 2.0 (Évite répétition)</small>
                      </FormGroup>

                      <FormGroup>
                        <Label>Mots d'arrêt</Label>
                        <TextArea
                          value={formData.stopWords}
                          onChange={(e) => handleInputChange('stopWords', e.target.value)}
                          placeholder="Un mot par ligne"
                        />
                        <small>Mots qui arrêtent la génération (un par ligne)</small>
                      </FormGroup>
                    </div>
                  </div>

                  <TipBox>
                    <TipTitle>
                      💡 Conseils de configuration
                    </TipTitle>
                    <TipText>
                      • Température basse (0.1-0.3): Réponses cohérentes et factuelles<br/>
                      • Température élevée (0.7-1.0): Réponses créatives et variées<br/>
                      • Max tokens élevé (500-1000): Pour des histoires ou explications longues<br/>
                      • Max tokens bas (20-50): Pour des réponses courtes et précises
                    </TipText>
                  </TipBox>
                </>
              )}

              {activeTab === 'prompt' && (
                <>
                  <FormGroup>
                    <Label>
                      Prompt système <Required>*</Required>
                    </Label>
                    <TextArea
                      value={formData.systemPrompt}
                      onChange={(e) => handleInputChange('systemPrompt', e.target.value)}
                      placeholder="Tu es un assistant IA spécialisé..."
                    />
                    <small>Ce prompt définit le comportement de base de votre agent. Utilisez des instructions claires et spécifiques.</small>
                  </FormGroup>
                </>
              )}

              {activeTab === 'tools' && (
                <>
                  <h3>Outils disponibles</h3>
                  <CheckboxGroup>
                    <CheckboxItem>
                      <Checkbox
                        type="checkbox"
                        checked={formData.tools['rag.search']}
                        onChange={(e) => handleToolChange('rag.search', e.target.checked)}
                      />
                      rag.search
                    </CheckboxItem>
                    <CheckboxItem>
                      <Checkbox
                        type="checkbox"
                        checked={formData.tools['rag.add_document']}
                        onChange={(e) => handleToolChange('rag.add_document', e.target.checked)}
                      />
                      rag.add_document
                    </CheckboxItem>
                    <CheckboxItem>
                      <Checkbox
                        type="checkbox"
                        checked={formData.tools['rag.answer']}
                        onChange={(e) => handleToolChange('rag.answer', e.target.checked)}
                      />
                      rag.answer
                    </CheckboxItem>
                    <CheckboxItem>
                      <Checkbox
                        type="checkbox"
                        checked={formData.tools['file.read']}
                        onChange={(e) => handleToolChange('file.read', e.target.checked)}
                      />
                      file.read
                    </CheckboxItem>
                    <CheckboxItem>
                      <Checkbox
                        type="checkbox"
                        checked={formData.tools['file.write']}
                        onChange={(e) => handleToolChange('file.write', e.target.checked)}
                      />
                      file.write
                    </CheckboxItem>
                    <CheckboxItem>
                      <Checkbox
                        type="checkbox"
                        checked={formData.tools['math.evaluate']}
                        onChange={(e) => handleToolChange('math.evaluate', e.target.checked)}
                      />
                      math.evaluate
                    </CheckboxItem>
                    <CheckboxItem>
                      <Checkbox
                        type="checkbox"
                        checked={formData.tools['few-shot']}
                        onChange={(e) => handleToolChange('few-shot', e.target.checked)}
                      />
                      few-shot
                    </CheckboxItem>
                  </CheckboxGroup>

                  <h3 style={{ marginTop: '32px' }}>Packs de connaissances</h3>
                  <CheckboxGroup>
                    <CheckboxItem>
                      <Checkbox
                        type="checkbox"
                        checked={formData.knowledgePacks['enseignement']}
                        onChange={(e) => handleKnowledgePackChange('enseignement', e.target.checked)}
                      />
                      enseignement
                    </CheckboxItem>
                    <CheckboxItem>
                      <Checkbox
                        type="checkbox"
                        checked={formData.knowledgePacks['pedagogie']}
                        onChange={(e) => handleKnowledgePackChange('pedagogie', e.target.checked)}
                      />
                      pedagogie
                    </CheckboxItem>
                  </CheckboxGroup>
                </>
              )}
            </TabContent>

            <ButtonGroup>
              <Button onClick={onClose}>Annuler</Button>
              <Button variant="primary" onClick={handleSubmit}>
                Créer l'agent
              </Button>
            </ButtonGroup>
          </ModalContent>
    </ModalOverlay>
  );
};

export default AgentCreatorModal;
