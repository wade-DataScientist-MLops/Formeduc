import React from 'react';
import styled from 'styled-components';
import { Sidebar } from './Sidebar';
import { Header } from './Header';

const LayoutContainer = styled.div`
  display: flex;
  min-height: 100vh;
  background: #f9fafb;
`;

const MainContent = styled.main`
  flex: 1;
  margin-left: 280px; /* Pour laisser place à la sidebar */
  padding-top: 64px; /* Pour laisser place au header */
  min-height: 100vh;
`;

const ContentWrapper = styled.div`
  padding: 32px;
`;

interface MainLayoutProps {
  children: React.ReactNode;
}

export const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
  return (
    <LayoutContainer>
      <Sidebar />
      <MainContent>
        <Header />
        <ContentWrapper>
          {children}
        </ContentWrapper>
      </MainContent>
    </LayoutContainer>
  );
};
