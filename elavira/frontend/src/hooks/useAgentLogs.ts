import { useState, useCallback } from 'react';

export interface LogEntry {
  id: string;
  timestamp: string;
  type: 'info' | 'error' | 'success' | 'debug';
  message: string;
  agent?: string;
}

export const useAgentLogs = () => {
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

  return {
    logs,
    addLog,
    clearLogs,
    logRequest,
    logResponse,
    logError,
    logInfo
  };
};
