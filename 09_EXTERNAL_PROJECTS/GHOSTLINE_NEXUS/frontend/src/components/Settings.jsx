import React, { useState, useEffect } from 'react';
import api from '../services/api';

function Settings() {
  const [providerInfo, setProviderInfo] = useState(null);
  const [testStatus, setTestStatus] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isTesting, setIsTesting] = useState(false);
  const [models, setModels] = useState(null);
  const [isSwitching, setIsSwitching] = useState(false);

  useEffect(() => {
    loadProviderInfo();
    loadModels();
  }, []);

  const loadProviderInfo = async () => {
    try {
      setIsLoading(true);
      const response = await api.getProviderInfo();
      setProviderInfo(response.data);
    } catch (error) {
      console.error('Failed to load provider info:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const loadModels = async () => {
    try {
      const response = await api.getModels();
      setModels(response.data);
    } catch (error) {
      console.error('Failed to load models:', error);
      // Not an error if provider is not local
    }
  };

  const testProvider = async () => {
    try {
      setIsTesting(true);
      setTestStatus(null);
      const response = await api.testProvider();
      setTestStatus(response.data);
    } catch (error) {
      console.error('Provider test failed:', error);
      setTestStatus({
        status: 'failed',
        error: error.response?.data?.error || error.message
      });
    } finally {
      setIsTesting(false);
    }
  };

  const handleSwitchModel = async (modelName) => {
    try {
      setIsSwitching(true);
      await api.switchModel(modelName);
      // Reload provider info and models after switch
      await loadProviderInfo();
      await loadModels();
      alert(`✅ Switched to ${modelName}`);
    } catch (error) {
      console.error('Model switch failed:', error);
      alert(`❌ Failed to switch model: ${error.response?.data?.error || error.message}`);
    } finally {
      setIsSwitching(false);
    }
  };

  if (isLoading) {
    return <div className="loading">Loading settings...</div>;
  }

  return (
    <div className="settings-container">
      <div className="settings-header">
        <h2>⚙️ System Settings</h2>
      </div>

      <div className="settings-section">
        <h3>🤖 LLM Provider</h3>

        {providerInfo && (
          <div className="provider-info">
            <div className="info-row">
              <span className="label">Current Provider:</span>
              <span className="value">{providerInfo.current_provider.name}</span>
            </div>
            <div className="info-row">
              <span className="label">Model:</span>
              <span className="value">{providerInfo.current_provider.model}</span>
            </div>
            <div className="info-row">
              <span className="label">Provider Type:</span>
              <span className="value">{providerInfo.current_provider.provider}</span>
            </div>
          </div>
        )}

        <div className="settings-actions">
          <button
            onClick={testProvider}
            className="btn-primary"
            disabled={isTesting}
          >
            {isTesting ? 'Testing...' : '🔍 Test Connection'}
          </button>
        </div>

        {testStatus && (
          <div className={`test-result ${testStatus.status}`}>
            <div className="test-status">
              Status: {testStatus.status === 'connected' ? '✅ Connected' : '❌ Failed'}
            </div>
            {testStatus.status === 'connected' && (
              <>
                <div className="test-response">
                  Test Response: {testStatus.test_response}
                </div>
                <div className="test-usage">
                  Tokens: {testStatus.usage.input_tokens} in / {testStatus.usage.output_tokens} out
                </div>
              </>
            )}
            {testStatus.status === 'failed' && (
              <>
                <div className="test-error">
                  Error: {testStatus.error}
                </div>
                {testStatus.suggestion && (
                  <div className="test-suggestion">
                    💡 {testStatus.suggestion}
                  </div>
                )}
              </>
            )}
          </div>
        )}
      </div>

      {models && models.available_models && (
        <div className="settings-section">
          <h3>🔄 Model Switching</h3>
          <div className="model-info">
            <p>Current Model: <strong>{models.current_model}</strong></p>
            <p className="model-note">💡 {models.dignum_note}</p>
          </div>

          <div className="models-grid">
            {models.available_models.map(model => {
              const isActive = model.name === models.current_model;
              const sizeMB = (model.size / (1024 * 1024)).toFixed(0);

              return (
                <div
                  key={model.name}
                  className={`model-card ${isActive ? 'active' : ''}`}
                >
                  <div className="model-header">
                    <span className="model-name">{model.name}</span>
                    {isActive && <span className="model-badge">✓ Active</span>}
                  </div>
                  <div className="model-meta">
                    <span className="model-size">{sizeMB} MB</span>
                  </div>
                  {!isActive && (
                    <button
                      onClick={() => handleSwitchModel(model.name)}
                      className="btn-secondary btn-small"
                      disabled={isSwitching}
                    >
                      {isSwitching ? 'Switching...' : 'Switch'}
                    </button>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}

      <div className="settings-section">
        <h3>🔄 Available Providers</h3>
        <div className="providers-list">
          {providerInfo?.available_providers.map(provider => (
            <div
              key={provider}
              className={`provider-card ${providerInfo.current_provider.provider === provider ? 'active' : ''}`}
            >
              <div className="provider-name">
                {provider === 'claude' && '🜂 Claude'}
                {provider === 'openai' && '🤖 OpenAI'}
                {provider === 'gemini' && '✨ Gemini'}
                {provider === 'local' && '🏠 Local LLM'}
              </div>
              {providerInfo.current_provider.provider === provider && (
                <div className="provider-active">✓ Active</div>
              )}
            </div>
          ))}
        </div>
        <div className="provider-note">
          💡 To switch providers, edit .env file and set LLM_PROVIDER
        </div>
      </div>

      <div className="settings-section">
        <h3>🛡️ DIGNUM Principles</h3>
        <div className="dignum-info">
          <p>✅ <strong>No Vendor Lock-in:</strong> Switch LLM providers anytime</p>
          <p>✅ <strong>Local-First:</strong> Use local LLMs for full privacy</p>
          <p>✅ <strong>Transparent:</strong> All provider code is visible</p>
          <p>✅ <strong>Sovereign:</strong> You control the intelligence</p>
        </div>
        {providerInfo?.dignum_note && (
          <div className="dignum-note">
            🜂 {providerInfo.dignum_note}
          </div>
        )}
      </div>

      <div className="settings-section">
        <h3>📋 Provider Setup Guide</h3>
        <div className="setup-guide">
          <details>
            <summary>🜂 Claude (Anthropic)</summary>
            <div className="guide-content">
              <p>1. Get API key: https://console.anthropic.com/</p>
              <p>2. Add to .env: ANTHROPIC_API_KEY=sk-ant-...</p>
              <p>3. Set: LLM_PROVIDER=claude</p>
              <p>4. Restart: docker-compose restart</p>
            </div>
          </details>

          <details>
            <summary>🤖 OpenAI (ChatGPT)</summary>
            <div className="guide-content">
              <p>1. Get API key: https://platform.openai.com/</p>
              <p>2. Add to .env: OPENAI_API_KEY=sk-...</p>
              <p>3. Set: LLM_PROVIDER=openai</p>
              <p>4. Restart: docker-compose restart</p>
            </div>
          </details>

          <details>
            <summary>✨ Gemini (Google)</summary>
            <div className="guide-content">
              <p>1. Get API key: https://makersuite.google.com/</p>
              <p>2. Add to .env: GEMINI_API_KEY=...</p>
              <p>3. Set: LLM_PROVIDER=gemini</p>
              <p>4. Restart: docker-compose restart</p>
            </div>
          </details>

          <details>
            <summary>🏠 Local LLM (Ollama)</summary>
            <div className="guide-content">
              <p>1. Install Ollama: https://ollama.ai/</p>
              <p>2. Pull model: ollama pull llama2</p>
              <p>3. Set .env: LLM_PROVIDER=local</p>
              <p>4. Set: LOCAL_LLM_ENDPOINT=http://localhost:11434</p>
              <p>5. Set: LOCAL_LLM_MODEL=llama2</p>
              <p>6. Restart: docker-compose restart</p>
              <p><strong>✨ Best for privacy & sovereignty!</strong></p>
            </div>
          </details>
        </div>
      </div>
    </div>
  );
}

export default Settings;
