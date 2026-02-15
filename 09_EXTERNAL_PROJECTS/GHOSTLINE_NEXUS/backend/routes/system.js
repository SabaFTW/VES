// 🜂 System Routes - Provider info, health, diagnostics
const express = require('express');
const router = express.Router();
const { getLLMAdapter } = require('../services/llm-adapter');

// Get current LLM provider info
router.get('/provider', (req, res) => {
  try {
    const adapter = getLLMAdapter();
    const info = adapter.getProviderInfo();

    res.json({
      current_provider: info,
      available_providers: ['claude', 'openai', 'gemini', 'local'],
      dignum_note: 'No vendor lock-in. Switch providers anytime.'
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Test LLM provider connectivity
router.get('/provider/test', async (req, res) => {
  try {
    const adapter = getLLMAdapter();
    const info = adapter.getProviderInfo();

    // Send test message
    const testResponse = await adapter.sendMessage([
      { role: 'user', content: 'Respond with just: OK' }
    ]);

    res.json({
      status: 'connected',
      provider: info,
      test_response: testResponse.content,
      usage: testResponse.usage
    });
  } catch (error) {
    res.status(500).json({
      status: 'failed',
      error: error.message,
      suggestion: 'Check your API key or local LLM endpoint in .env'
    });
  }
});

// Get available models (for local provider)
router.get('/models', async (req, res) => {
  try {
    const adapter = getLLMAdapter();
    const provider = adapter.getProviderInfo().provider;

    if (provider !== 'local') {
      return res.status(400).json({
        error: 'Model switching only supported for local provider',
        current_provider: provider
      });
    }

    // Query Ollama for available models
    const endpoint = process.env.LOCAL_LLM_ENDPOINT || 'http://host.docker.internal:11434';
    const response = await fetch(`${endpoint}/api/tags`);
    const data = await response.json();

    const models = data.models.map(m => ({
      name: m.name,
      size: m.size,
      modified: m.modified_at
    }));

    res.json({
      available_models: models,
      current_model: process.env.LOCAL_LLM_MODEL || 'llama2',
      dignum_note: 'Switch models without restart'
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Switch active model (updates env, restarts adapter)
router.post('/models/switch', async (req, res) => {
  try {
    const { model } = req.body;

    if (!model) {
      return res.status(400).json({ error: 'Model name required' });
    }

    const adapter = getLLMAdapter();
    const provider = adapter.getProviderInfo().provider;

    if (provider !== 'local') {
      return res.status(400).json({
        error: 'Model switching only supported for local provider',
        current_provider: provider
      });
    }

    // Update runtime environment
    process.env.LOCAL_LLM_MODEL = model;

    // Force adapter reload by clearing require cache
    delete require.cache[require.resolve('../services/llm-adapter')];

    res.json({
      status: 'switched',
      new_model: model,
      dignum_note: 'Model switched. Next message will use new model.'
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;
