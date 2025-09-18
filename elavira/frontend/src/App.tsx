import React, { useEffect, useState } from 'react';
import styled, { createGlobalStyle } from 'styled-components';
import { AppProvider, useApp } from './context/AppContext';
import { LogsProvider } from './context/LogsContext';
import { AuthWithCarousel } from './components/Auth/AuthWithCarousel';
import { AgentChatRouter } from './components/Chat/AgentChatRouter';
import { AgentsManagementDashboard } from './components/Dashboard/AgentsManagementDashboard';
import { MainLayout } from './components/Layout/MainLayout';
import { LogsPage } from './components/Logs/LogsPage';
import { LimovaHomePage } from './components/Dashboard/LimovaHomePage';

const GlobalStyle = createGlobalStyle`
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #fefefe;
    color: #2c3e50;
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }

  #root {
    height: 100vh;
    overflow: hidden;
  }

  button {
    font-family: inherit;
  }

  input, textarea, select {
    font-family: inherit;
  }

  /* Scrollbar styling */
  ::-webkit-scrollbar {
    width: 8px;
  }

  ::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 4px;
  }

  ::-webkit-scrollbar-thumb {
    background: #c1c1c1;
    border-radius: 4px;
  }

  ::-webkit-scrollbar-thumb:hover {
    background: #a8a8a8;
  }

  /* Focus styles */
  *:focus {
    outline: 2px solid #3b82f6;
    outline-offset: 2px;
  }

  /* Animation utilities */
  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
  }

  @keyframes slideIn {
    from { transform: translateX(-100%); }
    to { transform: translateX(0); }
  }

  .fade-in {
    animation: fadeIn 0.3s ease-out;
  }

  .slide-in {
    animation: slideIn 0.3s ease-out;
  }
`;

const AppContainer = styled.div`
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  position: relative;
`;

const LoadingScreen = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
`;

const LoadingSpinner = styled.div`
  width: 50px;
  height: 50px;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top: 4px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
`;

const LoadingText = styled.p`
  font-size: 1.1rem;
  font-weight: 500;
`;

function AppContent() {
  const { state, dispatch } = useApp();
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Vérifier si l'utilisateur est déjà connecté
    const checkAuth = async () => {
      const token = localStorage.getItem('access_token');
      const user = localStorage.getItem('logged_in_user');
      
      if (token && user) {
        try {
          // Vérifier la validité du token
          const response = await fetch('http://104.254.182.118:8000/users/me/', {
            headers: {
              'Authorization': `Bearer ${token}`,
            },
          });
          
          if (response.ok) {
            dispatch({ type: 'SET_ACCESS_TOKEN', payload: token });
            dispatch({ type: 'SET_LOGGED_IN_USER', payload: user });
            dispatch({ type: 'SET_PAGE', payload: 'agents' });
          } else {
            // Token invalide, nettoyer le localStorage
            localStorage.removeItem('access_token');
            localStorage.removeItem('logged_in_user');
          }
        } catch (error) {
          console.error('Erreur de vérification du token:', error);
          localStorage.removeItem('access_token');
          localStorage.removeItem('logged_in_user');
        }
      }
      
      setIsLoading(false);
    };

    checkAuth();
  }, [dispatch]);

  if (isLoading) {
    return (
      <LoadingScreen>
        <LoadingSpinner />
        <LoadingText>Chargement d'Elavira...</LoadingText>
      </LoadingScreen>
    );
  }

  const renderPage = () => {
    switch (state.page) {
      case 'home':
        return <LimovaHomePage />;
      case 'auth':
        return <AuthWithCarousel />;
      case 'agents':
        return (
          <MainLayout>
            <AgentsManagementDashboard />
          </MainLayout>
        );
      case 'chat':
        return (
          <MainLayout>
            <AgentChatRouter />
          </MainLayout>
        );
      case 'logs':
        return (
          <MainLayout>
            <LogsPage />
          </MainLayout>
        );
      default:
        return <LimovaHomePage />;
    }
  };

  return (
    <AppContainer>
      {renderPage()}
    </AppContainer>
  );
}

function App() {
  return (
    <AppProvider>
      <LogsProvider>
        <GlobalStyle />
        <AppContent />
      </LogsProvider>
    </AppProvider>
  );
}

export default App;