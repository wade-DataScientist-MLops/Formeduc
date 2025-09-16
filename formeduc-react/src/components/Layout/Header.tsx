import React from 'react';
import styled from 'styled-components';

const HeaderContainer = styled.header`
  height: 64px;
  background: #ffffff;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding: 0 32px;
  margin-left: 280px; /* Pour laisser place à la sidebar */
  position: fixed;
  top: 0;
  right: 0;
  left: 280px;
  z-index: 99;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
`;

const RightSection = styled.div`
  display: flex;
  align-items: center;
  gap: 16px;
`;

const IconButton = styled.button`
  width: 40px;
  height: 40px;
  border: none;
  background: #f3f4f6;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 16px;
  color: #6b7280;

  &:hover {
    background: #e5e7eb;
    color: #374151;
  }
`;

const ProfileButton = styled.button`
  width: 40px;
  height: 40px;
  border: none;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  color: white;
  font-weight: 600;
  font-size: 14px;

  &:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
  }
`;

export const Header: React.FC = () => {
  return (
    <HeaderContainer>
      <RightSection>
        <IconButton title="Notifications">
          🔔
        </IconButton>
        <ProfileButton title="Profil">
          U
        </ProfileButton>
      </RightSection>
    </HeaderContainer>
  );
};
