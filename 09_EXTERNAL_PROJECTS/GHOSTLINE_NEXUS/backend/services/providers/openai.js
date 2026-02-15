// 🜂 OpenAI Provider - OpenAI/Azure API
const axios = require('axios');

class OpenAIProvider {
  constructor(config) {
    this.apiKey = config.apiKey;
    this.model = config.model || 'gpt-4-turbo-preview';
    this.maxTokens = config.maxTokens || 4096;
    this.temperature = config.temperature || 0.7;
    this.baseURL = config.baseURL || 'https://api.openai.com/v1';

    if (!this.apiKey) {
      throw new Error('OpenAI API key required');
    }

    this.client = axios.create({
      baseURL: this.baseURL,
      headers: {
        'Authorization': `Bearer ${this.apiKey}`,
        'Content-Type': 'application/json'
      },
      timeout: 60000
    });
  }

  async sendMessage(messages) {
    try {
      const response = await this.client.post('/chat/completions', {
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
          input_tokens: response.data.usage.prompt_tokens,
          output_tokens: response.data.usage.completion_tokens
        },
        provider: 'openai'
      };
    } catch (error) {
      console.error('OpenAI Provider Error:', error.response?.data || error);
      throw new Error(`OpenAI API failed: ${error.response?.data?.error?.message || error.message}`);
    }
  }

  getName() {
    return 'OpenAI';
  }

  getModel() {
    return this.model;
  }
}

module.exports = OpenAIProvider;
