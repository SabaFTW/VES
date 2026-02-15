// 🜂 Claude Provider - Anthropic API
const Anthropic = require('@anthropic-ai/sdk');

class ClaudeProvider {
  constructor(config) {
    this.apiKey = config.apiKey;
    this.model = config.model || 'claude-sonnet-4-5-20250929';
    this.maxTokens = config.maxTokens || 4096;
    this.temperature = config.temperature || 0.7;

    if (!this.apiKey) {
      throw new Error('Claude API key required');
    }

    this.client = new Anthropic({ apiKey: this.apiKey });
  }

  async sendMessage(messages) {
    try {
      const response = await this.client.messages.create({
        model: this.model,
        max_tokens: this.maxTokens,
        temperature: this.temperature,
        messages: messages.map(msg => ({
          role: msg.role,
          content: msg.content
        }))
      });

      return {
        content: response.content[0].text,
        usage: {
          input_tokens: response.usage.input_tokens,
          output_tokens: response.usage.output_tokens
        },
        provider: 'claude'
      };
    } catch (error) {
      console.error('Claude Provider Error:', error);
      throw new Error(`Claude API failed: ${error.message}`);
    }
  }

  getName() {
    return 'Claude';
  }

  getModel() {
    return this.model;
  }
}

module.exports = ClaudeProvider;
