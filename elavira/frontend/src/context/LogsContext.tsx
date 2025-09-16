import React, { createContext, useContext, useState, useCallback, ReactNode } from 'react';

export interface LogEntry {
  id: string;
  timestamp: string;
  type: 'info' | 'error' | 'success' | 'debug';
  message: string;
  agent?: string;
}

interface LogsContextType {
  logs: LogEntry[];
  addLog: (message: string, type?: 'info' | 'error' | 'success' | 'debug', agent?: string) => void;
  clearLogs: () => void;
  logRequest: (url: string, method: string, agent?: string) => void;
  logResponse: (status: number, message: string, agent?: string) => void;
  logError: (error: string, agent?: string) => void;
  logInfo: (message: string, agent?: string) => void;
}

const LogsContext = createContext<LogsContextType | undefined>(undefined);

export const useLogs = () => {
  const context = useContext(LogsContext);
  if (!context) {
    throw new Error('useLogs must be used within a LogsProvider');
  }
  return context;
};

interface LogsProviderProps {
  children: ReactNode;
}

export const LogsProvider: React.FC<LogsProviderProps> = ({ children }) => {
  const [logs, setLogs] = useState<LogEntry[]>([]);

  const addLog = useCallback((message: string, type: 'info' | 'error' | 'success' | 'debug' = 'info', agent?: string) => {
    const newLog: LogEntry = {
      id: Date.now().toString() + Math.random().toString(36).substr(2, 9),
      timestamp: new Date().toISOString(),
      type,
      message,
      agent
    };
    
    setLogs(prev => [...prev, newLog].slice(-100)); // Garder seulement les 100 derniers logs
  }, []);

  const clearLogs = useCallback(() => {
    setLogs([]);
  }, []);

  const logRequest = useCallback((url: string, method: string, agent?: string) => {
    addLog(`${method} ${url}`, 'debug', agent);
  }, [addLog]);

  const logResponse = useCallback((status: number, message: string, agent?: string) => {
    const type = status >= 400 ? 'error' : status >= 200 ? 'success' : 'info';
    addLog(`Response ${status}: ${message}`, type, agent);
  }, [addLog]);

  const logError = useCallback((error: string, agent?: string) => {
    addLog(`Error: ${error}`, 'error', agent);
  }, [addLog]);

  const logInfo = useCallback((message: string, agent?: string) => {
    addLog(message, 'info', agent);
  }, [addLog]);

  const value: LogsContextType = {
    logs,
    addLog,
    clearLogs,
    logRequest,
    logResponse,
    logError,
    logInfo
  };

  return (
    <LogsContext.Provider value={value}>
      {children}
    </LogsContext.Provider>
  );
};
