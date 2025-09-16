import React, { useState } from 'react';
import { AgentSelector } from './AgentSelector';
import { ElaviraChat } from './ElaviraChat';
import { SolenysChat } from './SolenysChat';

type ChatView = 'selector' | 'elavira' | 'solenys';

export const ChatApp: React.FC = () => {
  const [currentView, setCurrentView] = useState<ChatView>('selector');

  const handleAgentSelect = (agentId: string) => {
    if (agentId === 'elavira') {
      setCurrentView('elavira');
    } else if (agentId === 'solenys') {
      setCurrentView('solenys');
    }
  };


  const renderCurrentView = () => {
    switch (currentView) {
      case 'elavira':
        return <ElaviraChat />;
      case 'solenys':
        return <SolenysChat />;
      default:
        return <AgentSelector onAgentSelect={handleAgentSelect} />;
    }
  };

  return (
    <div style={{ height: '100vh', overflow: 'hidden' }}>
      {renderCurrentView()}
    </div>
  );
};
