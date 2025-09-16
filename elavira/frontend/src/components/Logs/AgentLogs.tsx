import React, { useState, useEffect } from 'react';
import styled from 'styled-components';

const LogsContainer = styled.div`
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 400px;
  max-height: 300px;
  background: #1a1a1a;
  border: 1px solid #333;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  z-index: 1000;
  font-family: 'Courier New', monospace;
  font-size: 12px;
  color: #00ff00;
  overflow: hidden;
`;

const LogsHeader = styled.div`
  background: #333;
  padding: 8px 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #555;
`;

const LogsTitle = styled.h3`
  margin: 0;
  color: #fff;
  font-size: 14px;
  font-weight: 600;
`;

const ToggleButton = styled.button`
  background: #555;
  color: #fff;
  border: none;
  padding: 4px 8px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 10px;
  
  &:hover {
    background: #666;
  }
`;

const LogsContent = styled.div<{ isExpanded: boolean }>`
  height: ${props => props.isExpanded ? '250px' : '0px'};
  overflow-y: auto;
  transition: height 0.3s ease;
  padding: ${props => props.isExpanded ? '8px' : '0px'};
`;

const LogEntry = styled.div<{ type: 'info' | 'error' | 'success' | 'debug' }>`
  margin-bottom: 4px;
  padding: 2px 4px;
  border-radius: 2px;
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
  border-left: 2px solid ${props => {
    switch (props.type) {
      case 'error': return '#ff6b6b';
      case 'success': return '#51cf66';
      case 'debug': return '#74c0fc';
      default: return '#00ff00';
    }
  }};
`;

const Timestamp = styled.span`
  color: #888;
  margin-right: 8px;
`;

interface LogEntry {
  id: string;
  timestamp: string;
  type: 'info' | 'error' | 'success' | 'debug';
  message: string;
  agent?: string;
}

interface AgentLogsProps {
  logs: LogEntry[];
  onClearLogs: () => void;
}

export const AgentLogs: React.FC<AgentLogsProps> = ({ logs, onClearLogs }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleTimeString('fr-FR', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  return (
    <LogsContainer>
      <LogsHeader>
        <LogsTitle>Agent Logs ({logs.length})</LogsTitle>
        <div>
          <ToggleButton onClick={() => setIsExpanded(!isExpanded)}>
            {isExpanded ? '▼' : '▲'}
          </ToggleButton>
          <ToggleButton onClick={onClearLogs} style={{ marginLeft: '4px' }}>
            Clear
          </ToggleButton>
        </div>
      </LogsHeader>
      <LogsContent isExpanded={isExpanded}>
        {logs.map((log) => (
          <LogEntry key={log.id} type={log.type}>
            <Timestamp>{formatTimestamp(log.timestamp)}</Timestamp>
            {log.agent && <span style={{ color: '#ffd43b' }}>[{log.agent}] </span>}
            {log.message}
          </LogEntry>
        ))}
        {logs.length === 0 && (
          <LogEntry type="info">
            <Timestamp>{formatTimestamp(new Date().toISOString())}</Timestamp>
            Aucun log disponible
          </LogEntry>
        )}
      </LogsContent>
    </LogsContainer>
  );
};