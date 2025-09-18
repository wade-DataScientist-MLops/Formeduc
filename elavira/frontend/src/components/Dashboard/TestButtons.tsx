import React from 'react';
import { useApp } from '../../context/AppContext';

export const TestButtons: React.FC = () => {
  const { state, dispatch } = useApp();

  const handleTestAuth = () => {
    console.log('Test auth button clicked');
    console.log('Current state:', state);
    dispatch({ type: 'SET_PAGE', payload: 'auth' });
  };

  const handleTestAgents = () => {
    console.log('Test agents button clicked');
    console.log('Current state:', state);
    dispatch({ type: 'SET_PAGE', payload: 'agents' });
  };

  const handleTestChat = () => {
    console.log('Test chat button clicked');
    console.log('Current state:', state);
    dispatch({ type: 'SET_PAGE', payload: 'chat' });
  };

  return (
    <div style={{ 
      position: 'fixed', 
      top: '10px', 
      right: '10px', 
      zIndex: 9999, 
      background: 'rgba(0,0,0,0.8)', 
      color: 'white', 
      padding: '20px',
      borderRadius: '10px'
    }}>
      <h3>Test Buttons</h3>
      <p>Current page: {state.page}</p>
      <p>Logged in: {state.logged_in_user ? 'Yes' : 'No'}</p>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
        <button onClick={handleTestAuth} style={{ padding: '10px', background: 'red', color: 'white', border: 'none', borderRadius: '5px' }}>
          Test Auth
        </button>
        <button onClick={handleTestAgents} style={{ padding: '10px', background: 'blue', color: 'white', border: 'none', borderRadius: '5px' }}>
          Test Agents
        </button>
        <button onClick={handleTestChat} style={{ padding: '10px', background: 'green', color: 'white', border: 'none', borderRadius: '5px' }}>
          Test Chat
        </button>
      </div>
    </div>
  );
};
