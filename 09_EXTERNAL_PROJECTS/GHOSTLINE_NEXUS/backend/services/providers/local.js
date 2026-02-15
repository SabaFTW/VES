// 🜂 Local LLM Provider - Ollama / LM Studio / vLLM / Any OpenAI-compatible endpoint
const axios = require('axios');

class LocalProvider {
  constructor(config) {
    this.endpoint = config.endpoint || 'http://localhost:11434';
    this.model = config.model || 'llama2';
    this.maxTokens = config.maxTokens || 4096;
    this.temperature = config.temperature || 0.7;
    this.format = config.format || 'openai'; // openai | ollama

    // Detect format from endpoint
    if (this.endpoint.includes('11434')) {
      this.format = 'ollama';
    }

    this.client = axios.create({
      baseURL: this.endpoint,
      headers: { 'Content-Type': 'application/json' },
      timeout: 120000 // Local LLMs can be slower
    });
  }

  async sendMessage(messages) {
    try {
      if (this.format === 'ollama') {
        return await this.sendOllamaMessage(messages);
      } else {
        return await this.sendOpenAIMessage(messages);
      }
    } catch (error) {
      console.error('Local LLM Provider Error:', error.response?.data || error);
      throw new Error(`Local LLM failed: ${error.message}`);
    }
  }

  async sendOllamaMessage(messages) {
    // Ollama chat format
    const response = await this.client.post('/api/chat', {
      model: this.model,
      messages: messages.map(msg => ({
        role: msg.role,
        content: msg.content
      })),
      stream: false,
      options: {
        temperature: this.temperature,
        num_predict: this.maxTokens
      }
    });

    return {
      content: response.data.message.content,
      usage: {
        input_tokens: response.data.prompt_eval_count || 0,
        output_tokens: response.data.eval_count || 0
      },
      provider: 'local-ollama'
    };
  }

  async sendOpenAIMessage(messages) {
    // OpenAI-compatible format (LM Studio, vLLM, etc.)
    const response = await this.client.post('/v1/chat/completions', {
      model: this.model,
      messages: messages.map(msg => ({
        role: msg.role === 'user' ? 'user' : 'assistant',
        content: msg.content
      })),
      max_tokens: this.maxTokens,
      temperature: this.temperature
    });

    const choice = response.data.choices[0];

    return {
      content: choice.message.content,
      usage: {
        input_tokens: response.data.usage?.prompt_tokens || 0,
        output_tokens: response.data.usage?.completion_tokens || 0
      },
      provider: 'local-openai'
    };
  }

  getName() {
    return `Local LLM (${this.format})`;
  }

  getModel() {
    return this.model;
  }
}

module.exports = LocalProvider;
