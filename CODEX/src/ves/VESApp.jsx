/**
 * VES PWA - Main Application Component
 * Unified interface for all VES systems
 */

import React, { useEffect } from 'react';
import { useVESStore } from './store/vesStore';
import Dashboard from './pages/Dashboard';
import AgentConsole from './pages/AgentConsole';
import OracleViewer from './pages/OracleViewer';

export default function VESApp() {
  const { initialize, isDarkMode, currentView } = useVESStore();

  useEffect(() => {
    // Initialize VES store
    initialize();

    // Set up dark mode
    if (isDarkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [initialize, isDarkMode]);

  // Route to different views
  const renderView = () => {
    switch (currentView) {
      case 'agents':
        return <AgentConsole />;
      case 'oracle':
        return <OracleViewer />;
      case 'system-detail':
      case 'dashboard':
      default:
        return <Dashboard />;
    }
  };

  return (
    <div className={isDarkMode ? 'dark' : ''}>
      {renderView()}
    </div>
  );
}
