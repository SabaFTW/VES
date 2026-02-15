// 🜂 Gemini Provider - Google Gemini API
const axios = require('axios');

class GeminiProvider {
  constructor(config) {
    this.apiKey = config.apiKey;
    this.model = config.model || 'gemini-1.5-pro-latest';
    this.maxTokens = config.maxTokens || 4096;
    this.temperature = config.temperature || 0.7;

    if (!this.apiKey) {
      throw new Error('Gemini API key required');
    }

    this.baseURL = `https://generativelanguage.googleapis.com/v1beta/models/${this.model}:generateContent`;
  }

  async sendMessage(messages) {
    try {
      // Convert messages to Gemini format
      const contents = messages.map(msg => ({
        role: msg.role === 'user' ? 'user' : 'model',
        parts: [{ text: msg.content }]
      }));

      const response = await axios.post(
        `${this.baseURL}?key=${this.apiKey}`,
        {
          contents: contents,
          generationConfig: {
            maxOutputTokens: this.maxTokens,
            temperature: this.temperature
          }
        },
        {
          headers: { 'Content-Type': 'application/json' },
          timeout: 60000
        }
      );

      const candidate = response.data.candidates[0];
      const content = candidate.content.parts[0].text;

      return {
        content: content,
        usage: {
          input_tokens: response.data.usageMetadata?.promptTokenCount || 0,
          output_tokens: response.data.usageMetadata?.candidatesTokenCount || 0
        },
        provider: 'gemini'
      };
    } catch (error) {
      console.error('Gemini Provider Error:', error.response?.data || error);
      throw new Error(`Gemini API failed: ${error.response?.data?.error?.message || error.message}`);
    }
  }

  getName() {
    return 'Gemini';
  }

  getModel() {
    return this.model;
  }
}

module.exports = GeminiProvider;
