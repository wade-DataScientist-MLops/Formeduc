import React from 'react';
import styled from 'styled-components';
import { useApp } from '../../context/AppContext';

const SidebarContainer = styled.div`
  width: 280px;
  height: 100vh;
  background: #ffffff;
  border-right: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
  position: fixed;
  left: 0;
  top: 0;
  z-index: 100;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.05);
`;

const LogoSection = styled.div`
  padding: 24px;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  gap: 12px;
`;

const Logo = styled.div`
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 18px;
`;

const LogoText = styled.h1`
  font-size: 24px;
  font-weight: 700;
  color: #1f2937;
  margin: 0;
`;

const Navigation = styled.nav`
  flex: 1;
  padding: 24px 0;
`;

const NavItem = styled.div<{ active?: boolean }>`
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 24px;
  cursor: pointer;
  transition: all 0.2s ease;
  background: ${props => props.active ? '#f3f4f6' : 'transparent'};
  border-right: ${props => props.active ? '3px solid #667eea' : '3px solid transparent'};
  color: ${props => props.active ? '#667eea' : '#6b7280'};
  font-weight: ${props => props.active ? '600' : '500'};

  &:hover {
    background: #f9fafb;
    color: #667eea;
  }
`;

const NavIcon = styled.div`
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
`;

const NavText = styled.span`
  font-size: 14px;
`;

const UserSection = styled.div`
  padding: 24px;
  border-top: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  gap: 12px;
`;

const UserAvatar = styled.div`
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: 14px;
`;

const UserInfo = styled.div`
  flex: 1;
`;

const UserName = styled.div`
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
`;

const UserRole = styled.div`
  font-size: 12px;
  color: #6b7280;
`;

export const Sidebar: React.FC = () => {
  const { state, dispatch } = useApp();

  const navigationItems = [
    { id: 'dashboard', icon: '📊', text: 'Dashboard' },
    { id: 'agents', icon: '🤖', text: 'Agents' },
    { id: 'chat', icon: '💬', text: 'Chat' },
    { id: 'multi-agents', icon: '👥', text: 'Multi-Agents' },
    { id: 'knowledge', icon: '📚', text: 'Connaissances' },
    { id: 'workflows', icon: '⚡', text: 'Workflows' },
    { id: 'logs', icon: '📋', text: 'Logs' },
    { id: 'settings', icon: '⚙️', text: 'Paramètres' },
  ];

  const handleNavClick = (itemId: string) => {
    if (itemId === 'agents') {
      dispatch({ type: 'SET_PAGE', payload: 'agents' });
    } else if (itemId === 'chat') {
      dispatch({ type: 'SET_PAGE', payload: 'chat' });
    } else if (itemId === 'logs') {
      dispatch({ type: 'SET_PAGE', payload: 'logs' });
    } else if (itemId === 'dashboard') {
      dispatch({ type: 'SET_PAGE', payload: 'agents' }); // Pour l'instant, dashboard = agents
    }
    // Les autres pages ne sont pas encore implémentées
  };

  const getCurrentPage = () => {
    if (state.page === 'agents') return 'agents';
    if (state.page === 'chat') return 'chat';
    if (state.page === 'logs') return 'logs';
    return 'agents'; // Par défaut
  };

  return (
    <SidebarContainer>
      <LogoSection>
        <Logo>E</Logo>
        <LogoText>Elavira</LogoText>
      </LogoSection>
      
      <Navigation>
        {navigationItems.map((item) => (
          <NavItem
            key={item.id}
            active={getCurrentPage() === item.id}
            onClick={() => handleNavClick(item.id)}
          >
            <NavIcon>{item.icon}</NavIcon>
            <NavText>{item.text}</NavText>
          </NavItem>
        ))}
      </Navigation>

      <UserSection>
        <UserAvatar>U</UserAvatar>
        <UserInfo>
          <UserName>Utilisateur</UserName>
          <UserRole>Admin</UserRole>
        </UserInfo>
      </UserSection>
    </SidebarContainer>
  );
};
