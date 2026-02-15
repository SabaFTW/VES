import React, { useState, useEffect } from 'react';

function System() {
  const [services, setServices] = useState([
    {
      name: '🜂 GHOSTLINE NEXUS',
      description: 'Main application (you are here)',
      url: 'http://localhost:3000',
      local_url: 'http://192.168.1.243:3000',
      status: 'active',
      category: 'core'
    },
    {
      name: '🎛️ Command Deck',
      description: 'Dashboard & File Browser',
      url: 'http://localhost:8085',
      local_url: 'http://192.168.1.243:8085',
      status: 'unknown',
      category: 'tools'
    },
    {
      name: '🤖 Coordinator',
      description: 'AI Agent Coordinator (CLI only - no web UI)',
      url: null,
      local_url: null,
      status: 'active',
      category: 'agents',
      cli_only: true
    },
    {
      name: '🔴 Red Ranger',
      description: 'AI Agent Node',
      url: 'http://localhost:8100',
      local_url: 'http://192.168.1.243:8100',
      status: 'unknown',
      category: 'agents'
    },
    {
      name: '🔵 Blue Ranger',
      description: 'AI Agent Node',
      url: 'http://localhost:8101',
      local_url: 'http://192.168.1.243:8101',
      status: 'unknown',
      category: 'agents'
    },
    {
      name: '🟢 Green Ranger',
      description: 'AI Agent Node',
      url: 'http://localhost:8102',
      local_url: 'http://192.168.1.243:8102',
      status: 'unknown',
      category: 'agents'
    },
    {
      name: '🟡 Yellow Ranger',
      description: 'AI Agent Node',
      url: 'http://localhost:8103',
      local_url: 'http://192.168.1.243:8103',
      status: 'unknown',
      category: 'agents'
    },
    {
      name: '⚫ Black Ranger',
      description: 'AI Agent Node',
      url: 'http://localhost:8104',
      local_url: 'http://192.168.1.243:8104',
      status: 'unknown',
      category: 'agents'
    }
  ]);

  useEffect(() => {
    // Check service availability
    const checkServices = async () => {
      const updated = await Promise.all(
        services.map(async (service) => {
          if (service.category === 'core') {
            return { ...service, status: 'active' };
          }

          try {
            const response = await fetch(service.url, {
              method: 'GET',
              mode: 'no-cors', // Avoid CORS issues for quick check
              signal: AbortSignal.timeout(2000)
            });
            return { ...service, status: 'active' };
          } catch (error) {
            return { ...service, status: 'offline' };
          }
        })
      );
      setServices(updated);
    };

    checkServices();
    const interval = setInterval(checkServices, 30000); // Check every 30s
    return () => clearInterval(interval);
  }, []);

  const categories = {
    core: 'Core Services',
    tools: 'Tools & Utilities',
    agents: 'AI Agent Constellation'
  };

  return (
    <div className="system-container">
      <div className="system-header">
        <h2>🛰️ System Services</h2>
        <p className="system-description">
          All active services in your Ghostline ecosystem
        </p>
      </div>

      {Object.entries(categories).map(([category, label]) => {
        const categoryServices = services.filter(s => s.category === category);
        if (categoryServices.length === 0) return null;

        return (
          <div key={category} className="service-category">
            <h3>{label}</h3>
            <div className="services-grid">
              {categoryServices.map((service, idx) => (
                <div
                  key={idx}
                  className={`service-card service-${service.status}`}
                >
                  <div className="service-header">
                    <span className="service-name">{service.name}</span>
                    <span className={`service-status-badge status-${service.status}`}>
                      {service.status === 'active' ? '🟢 Online' :
                       service.status === 'offline' ? '🔴 Offline' :
                       '⚪ Checking...'}
                    </span>
                  </div>
                  <p className="service-description">{service.description}</p>

                  {service.cli_only ? (
                    <div className="service-cli-note">
                      <span>💻 CLI Tool - No web interface</span>
                    </div>
                  ) : (
                    <div className="service-links">
                      <a
                        href={service.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="service-link"
                      >
                        🖥️ Desktop: {service.url.replace('http://', '')}
                      </a>
                      <a
                        href={service.local_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="service-link service-link-mobile"
                      >
                        📱 LAN: {service.local_url.replace('http://', '')}
                      </a>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        );
      })}

      <div className="system-info">
        <h3>📡 Network Info</h3>
        <div className="info-grid">
          <div className="info-item">
            <span className="info-label">Local Access (Desktop):</span>
            <span className="info-value">localhost</span>
          </div>
          <div className="info-item">
            <span className="info-label">LAN Access (Phone/Tablet):</span>
            <span className="info-value">192.168.1.243</span>
          </div>
          <div className="info-item">
            <span className="info-label">Total Services:</span>
            <span className="info-value">{services.length}</span>
          </div>
          <div className="info-item">
            <span className="info-label">Active:</span>
            <span className="info-value status-active">
              {services.filter(s => s.status === 'active').length}
            </span>
          </div>
        </div>
      </div>

      <div className="system-footer">
        <p>💡 <strong>Tip:</strong> Open services in new tabs to navigate between them</p>
        <p>🔒 All services run locally - your data never leaves your machine</p>
      </div>
    </div>
  );
}

export default System;
