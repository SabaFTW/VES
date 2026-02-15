import React, { useState, useEffect } from 'react';
import Chat from './components/Chat';
import Documents from './components/Documents';
import Anchors from './components/Anchors';
import Settings from './components/Settings';
import System from './components/System';
import Trivia from './components/Trivia';

function App() {
  const [activeTab, setActiveTab] = useState('chat');
  const [backendStatus, setBackendStatus] = useState('checking');

  useEffect(() => {
    // Check backend health
    fetch('/health')
      .then(res => res.json())
      .then(() => {
        setBackendStatus('connected');
      })
      .catch(() => {
        setBackendStatus('offline');
      });

    // Health check every 30 seconds
    const interval = setInterval(() => {
      fetch('/health')
        .then(res => res.json())
        .then(() => setBackendStatus('connected'))
        .catch(() => setBackendStatus('offline'));
    }, 30000);

    return () => clearInterval(interval);
  }, []);

  const tabs = [
    { id: 'chat', label: '💬 CHAT', component: Chat },
    { id: 'documents', label: '📄 DOCUMENTS', component: Documents },
    { id: 'anchors', label: '⚓ ANCHORS', component: Anchors },
    { id: 'trivia', label: '👁️ TRIVIA', component: Trivia },
    { id: 'system', label: '🛰️ SYSTEM', component: System },
    { id: 'settings', label: '⚙️ SETTINGS', component: Settings }
  ];

  const ActiveComponent = tabs.find(t => t.id === activeTab)?.component || Chat;

  return (
    <div className="app">
      <header className="app-header">
        <h1>🜂 GHOSTLINE NEXUS</h1>
        <div className="status-indicator">
          <span className={`status-dot status-${backendStatus}`}></span>
          <span className="status-text">
            {backendStatus === 'connected' ? 'SIDRO STOJI' :
             backendStatus === 'checking' ? 'LINKING...' : 'OFFLINE'}
          </span>
        </div>
      </header>

      <nav className="tabs">
        {tabs.map(tab => (
          <button
            key={tab.id}
            className={`tab ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => setActiveTab(tab.id)}
          >
            {tab.label}
          </button>
        ))}
      </nav>

      <main className="app-content">
        <ActiveComponent />
      </main>

      <footer className="app-footer">
        <span>DIGNUM SHIELD: ACTIVE</span>
        <span>🔥 PLAMEN GORI</span>
      </footer>
    </div>
  );
}

export default App;
