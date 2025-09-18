import React, { useState } from 'react';
import styled from 'styled-components';
import { useApp } from '../../context/AppContext';

const HeaderContainer = styled.header`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 80px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 40px;
  z-index: 1000;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
`;

const Logo = styled.div`
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 1.5rem;
  font-weight: 800;
  color: #667eea;
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:hover {
    transform: scale(1.05);
  }
`;

const LogoIcon = styled.div`
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 20px;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
`;

const Navigation = styled.nav`
  display: flex;
  align-items: center;
  gap: 40px;
  
  @media (max-width: 768px) {
    display: none;
  }
`;

const NavLink = styled.button<{ active?: boolean }>`
  background: none;
  border: none;
  color: ${props => props.active ? '#667eea' : '#64748b'};
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  padding: 8px 16px;
  border-radius: 8px;
  position: relative;
  
  &:hover {
    color: #667eea;
    background: rgba(102, 126, 234, 0.1);
  }
  
  ${props => props.active && `
    &::after {
      content: '';
      position: absolute;
      bottom: -8px;
      left: 50%;
      transform: translateX(-50%);
      width: 20px;
      height: 3px;
      background: linear-gradient(90deg, #667eea, #764ba2);
      border-radius: 2px;
    }
  `}
`;

const RightSection = styled.div`
  display: flex;
  align-items: center;
  gap: 20px;
`;

const CTAButton = styled.button`
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 25px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4);
  }
  
  @media (max-width: 768px) {
    padding: 10px 20px;
    font-size: 0.8rem;
  }
`;

const UserInfo = styled.div`
  display: flex;
  align-items: center;
  gap: 12px;
  font-weight: 500;
  color: #64748b;
`;

const UserAvatar = styled.div`
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 16px;
  color: white;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
`;

const LogoutButton = styled.button`
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #ef4444;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
  
  &:hover {
    background: rgba(239, 68, 68, 0.2);
    transform: translateY(-1px);
  }
`;

const MobileMenuButton = styled.button`
  display: none;
  background: none;
  border: none;
  color: #64748b;
  font-size: 1.5rem;
  cursor: pointer;
  
  @media (max-width: 768px) {
    display: block;
  }
`;

export const Header: React.FC = () => {
  const { state, dispatch } = useApp();
  const { logged_in_user } = state;
  const current_page = state.page;
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const handleLogout = () => {
    dispatch({ type: 'LOGOUT' });
  };

  const handlePageChange = (page: string) => {
    dispatch({ type: 'SET_PAGE', payload: page });
    setIsMobileMenuOpen(false);
  };

  const handleLogoClick = () => {
    dispatch({ type: 'SET_PAGE', payload: 'home' });
  };

  return (
    <HeaderContainer>
      <Logo onClick={handleLogoClick}>
        <LogoIcon>E</LogoIcon>
        Elavira
      </Logo>
      
      <Navigation>
        <NavLink 
          active={current_page === 'home'} 
          onClick={() => handlePageChange('home')}
        >
          Accueil
        </NavLink>
        <NavLink 
          active={current_page === 'agents'} 
          onClick={() => handlePageChange('agents')}
        >
          Agents
        </NavLink>
        <NavLink 
          active={current_page === 'chat'} 
          onClick={() => handlePageChange('chat')}
        >
          Chat
        </NavLink>
        <NavLink 
          active={current_page === 'logs'} 
          onClick={() => handlePageChange('logs')}
        >
          Logs
        </NavLink>
      </Navigation>
      
      <RightSection>
        <CTAButton onClick={() => handlePageChange('agents')}>
          + Créer un agent
        </CTAButton>
        
        <UserInfo>
          <UserAvatar>
            {logged_in_user ? logged_in_user.charAt(0).toUpperCase() : 'U'}
          </UserAvatar>
          <span style={{ display: window.innerWidth > 768 ? 'block' : 'none' }}>
            {logged_in_user || 'Utilisateur'}
          </span>
          <LogoutButton onClick={handleLogout}>
            Déconnexion
          </LogoutButton>
        </UserInfo>
        
        <MobileMenuButton onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}>
          ☰
        </MobileMenuButton>
      </RightSection>
    </HeaderContainer>
  );
};