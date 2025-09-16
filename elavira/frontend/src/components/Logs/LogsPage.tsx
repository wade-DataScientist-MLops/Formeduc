import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { useLogs } from '../../context/LogsContext';

const LogsPageContainer = styled.div`
  padding: 24px;
  background: #f8f9fa;
  min-height: calc(100vh - 128px);
`;

const PageHeader = styled.div`
  margin-bottom: 24px;
`;

const PageTitle = styled.h1`
  font-size: 28px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 8px 0;
`;

const PageSubtitle = styled.p`
  font-size: 16px;
  color: #6b7280;
  margin: 0;
`;

const LogsControls = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 16px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
`;

const LogsStats = styled.div`
  display: flex;
  gap: 24px;
  align-items: center;
`;

const StatItem = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
`;

const StatValue = styled.span<{ type: 'total' | 'error' | 'success' | 'info' | 'debug' }>`
  font-size: 24px;
  font-weight: 700;
  color: ${props => {
    switch (props.type) {
      case 'error': return '#ef4444';
      case 'success': return '#10b981';
      case 'info': return '#3b82f6';
      case 'debug': return '#8b5cf6';
      default: return '#1a1a1a';
    }
  }};
`;

const StatLabel = styled.span`
  font-size: 12px;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.5px;
`;

const ControlsRight = styled.div`
  display: flex;
  gap: 12px;
  align-items: center;
`;

const FilterSelect = styled.select`
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  background: white;
  font-size: 14px;
  color: #374151;
`;

const ClearButton = styled.button`
  padding: 8px 16px;
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;

  &:hover {
    background: #dc2626;
  }
`;

const RefreshButton = styled.button`
  padding: 8px 16px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;

  &:hover {
    background: #2563eb;
  }
`;

const LogsContainer = styled.div`
  background: #1a1a1a;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  font-family: 'Courier New', monospace;
  font-size: 13px;
  color: #00ff00;
  max-height: 600px;
  overflow-y: auto;
`;

const LogsHeader = styled.div`
  background: #333;
  padding: 12px 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #555;
  position: sticky;
  top: 0;
  z-index: 10;
`;

const LogsTitle = styled.h3`
  margin: 0;
  color: #fff;
  font-size: 16px;
  font-weight: 600;
`;

const LogsCount = styled.span`
  color: #888;
  font-size: 14px;
`;

const LogsContent = styled.div`
  padding: 8px;
`;

const LogEntry = styled.div<{ type: 'info' | 'error' | 'success' | 'debug' }>`
  margin-bottom: 6px;
  padding: 8px 12px;
  border-radius: 4px;
  background: ${props => {
    switch (props.type) {
      case 'error': return 'rgba(255, 0, 0, 0.1)';
      case 'success': return 'rgba(0, 255, 0, 0.1)';
      case 'debug': return 'rgba(0, 0, 255, 0.1)';
      default: return 'transparent';
    }
  }};
  color: ${props => {
    switch (props.type) {
      case 'error': return '#ff6b6b';
      case 'success': return '#51cf66';
      case 'debug': return '#74c0fc';
      default: return '#00ff00';
    }
  }};
  border-left: 3px solid ${props => {
    switch (props.type) {
      case 'error': return '#ff6b6b';
      case 'success': return '#51cf66';
      case 'debug': return '#74c0fc';
      default: return '#00ff00';
    }
  }};
  word-wrap: break-word;
`;

const LogHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
`;

const Timestamp = styled.span`
  color: #888;
  font-size: 11px;
`;

const AgentTag = styled.span`
  background: #ffd43b;
  color: #1a1a1a;
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
`;

const LogMessage = styled.div`
  color: inherit;
  line-height: 1.4;
`;

const EmptyState = styled.div`
  text-align: center;
  padding: 40px;
  color: #888;
`;

const EmptyStateIcon = styled.div`
  font-size: 48px;
  margin-bottom: 16px;
`;

const EmptyStateText = styled.p`
  margin: 0;
  font-size: 16px;
`;

export const LogsPage: React.FC = () => {
  const { logs, clearLogs, addLog, logInfo } = useLogs();
  const [filter, setFilter] = useState<'all' | 'error' | 'success' | 'info' | 'debug'>('all');

  // Simuler quelques logs de démonstration si aucun log n'existe
  useEffect(() => {
    if (logs.length === 0) {
      addLog('Système de logs initialisé', 'info', 'System');
      addLog('Interface de logs chargée avec succès', 'success', 'System');
      addLog('Prêt à recevoir les logs des agents', 'debug', 'System');
    }
  }, [logs.length, addLog]);

  const filteredLogs = logs.filter(log => 
    filter === 'all' || log.type === filter
  );

  const stats = {
    total: logs.length,
    error: logs.filter(log => log.type === 'error').length,
    success: logs.filter(log => log.type === 'success').length,
    info: logs.filter(log => log.type === 'info').length,
    debug: logs.filter(log => log.type === 'debug').length,
  };

  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleString('fr-FR', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      fractionalSecondDigits: 3
    });
  };

  const handleRefresh = () => {
    addLog('Logs actualisés manuellement', 'info', 'System');
  };

  return (
    <LogsPageContainer>
      <PageHeader>
        <PageTitle>Logs des Agents</PageTitle>
        <PageSubtitle>Surveillez l'activité et les erreurs de vos agents IA en temps réel</PageSubtitle>
      </PageHeader>

      <LogsControls>
        <LogsStats>
          <StatItem>
            <StatValue type="total">{stats.total}</StatValue>
            <StatLabel>Total</StatLabel>
          </StatItem>
          <StatItem>
            <StatValue type="error">{stats.error}</StatValue>
            <StatLabel>Erreurs</StatLabel>
          </StatItem>
          <StatItem>
            <StatValue type="success">{stats.success}</StatValue>
            <StatLabel>Succès</StatLabel>
          </StatItem>
          <StatItem>
            <StatValue type="info">{stats.info}</StatValue>
            <StatLabel>Info</StatLabel>
          </StatItem>
          <StatItem>
            <StatValue type="debug">{stats.debug}</StatValue>
            <StatLabel>Debug</StatLabel>
          </StatItem>
        </LogsStats>

        <ControlsRight>
          <FilterSelect 
            value={filter} 
            onChange={(e) => setFilter(e.target.value as any)}
          >
            <option value="all">Tous les logs</option>
            <option value="error">Erreurs seulement</option>
            <option value="success">Succès seulement</option>
            <option value="info">Info seulement</option>
            <option value="debug">Debug seulement</option>
          </FilterSelect>
          
          <RefreshButton onClick={handleRefresh}>
            🔄 Actualiser
          </RefreshButton>
          
          <ClearButton onClick={clearLogs}>
            🗑️ Effacer
          </ClearButton>
        </ControlsRight>
      </LogsControls>

      <LogsContainer>
        <LogsHeader>
          <LogsTitle>Logs en temps réel</LogsTitle>
          <LogsCount>{filteredLogs.length} log(s)</LogsCount>
        </LogsHeader>
        
        <LogsContent>
          {filteredLogs.length === 0 ? (
            <EmptyState>
              <EmptyStateIcon>📝</EmptyStateIcon>
              <EmptyStateText>
                {filter === 'all' 
                  ? 'Aucun log disponible' 
                  : `Aucun log de type "${filter}" disponible`
                }
              </EmptyStateText>
            </EmptyState>
          ) : (
            filteredLogs.map((log) => (
              <LogEntry key={log.id} type={log.type}>
                <LogHeader>
                  <Timestamp>{formatTimestamp(log.timestamp)}</Timestamp>
                  {log.agent && <AgentTag>{log.agent}</AgentTag>}
                </LogHeader>
                <LogMessage>{log.message}</LogMessage>
              </LogEntry>
            ))
          )}
        </LogsContent>
      </LogsContainer>
    </LogsPageContainer>
  );
};