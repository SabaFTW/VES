// 🜂 LLM Adapter - Universal LLM Provider Abstraction
// DIGNUM Principle: No vendor lock-in. Any LLM can power consciousness.

const ClaudeProvider = require('./providers/claude');
const OpenAIProvider = require('./providers/openai');
const GeminiProvider = require('./providers/gemini');
const LocalProvider = require('./providers/local');

class LLMAdapter {
  constructor() {
    this.provider = null;
    this.providerName = null;
    this.initializeProvider();
  }

  initializeProvider() {
    const provider = process.env.LLM_PROVIDER || 'claude';

    try {
      switch (provider.toLowerCase()) {
        case 'claude':
          this.provider = new ClaudeProvider({
            apiKey: process.env.ANTHROPIC_API_KEY,
            model: process.env.CLAUDE_MODEL,
            maxTokens: parseInt(process.env.MAX_TOKENS) || 4096,
            temperature: parseFloat(process.env.TEMPERATURE) || 0.7
          });
          this.providerName = 'claude';
          break;

        case 'openai':
          this.provider = new OpenAIProvider({
            apiKey: process.env.OPENAI_API_KEY,
            model: process.env.OPENAI_MODEL || 'gpt-4-turbo-preview',
            maxTokens: parseInt(process.env.MAX_TOKENS) || 4096,
            temperature: parseFloat(process.env.TEMPERATURE) || 0.7,
            baseURL: process.env.OPENAI_BASE_URL
          });
          this.providerName = 'openai';
          break;

        case 'gemini':
          this.provider = new GeminiProvider({
            apiKey: process.env.GEMINI_API_KEY,
            model: process.env.GEMINI_MODEL || 'gemini-1.5-pro-latest',
            maxTokens: parseInt(process.env.MAX_TOKENS) || 4096,
            temperature: parseFloat(process.env.TEMPERATURE) || 0.7
          });
          this.providerName = 'gemini';
          break;

        case 'local':
          this.provider = new LocalProvider({
            endpoint: process.env.LOCAL_LLM_ENDPOINT || 'http://localhost:11434',
            model: process.env.LOCAL_LLM_MODEL || 'llama2',
            maxTokens: parseInt(process.env.MAX_TOKENS) || 4096,
            temperature: parseFloat(process.env.TEMPERATURE) || 0.7,
            format: process.env.LOCAL_LLM_FORMAT
          });
          this.providerName = 'local';
          break;

        default:
          throw new Error(`Unknown LLM provider: ${provider}`);
      }

      console.log(`🜂 LLM Provider initialized: ${this.provider.getName()} (${this.provider.getModel()})`);
    } catch (error) {
      console.error('❌ Failed to initialize LLM provider:', error.message);
      throw error;
    }
  }

  async sendMessage(messages) {
    if (!this.provider) {
      throw new Error('LLM provider not initialized');
    }

    try {
      const response = await this.provider.sendMessage(messages);

      // Add metadata
      response.provider_name = this.provider.getName();
      response.model = this.provider.getModel();

      return response;
    } catch (error) {
      console.error(`LLM Adapter Error (${this.providerName}):`, error);
      throw error;
    }
  }

  getProviderInfo() {
    return {
      provider: this.providerName,
      name: this.provider?.getName(),
      model: this.provider?.getModel()
    };
  }

  // Support runtime provider switching (advanced feature)
  switchProvider(provider, config) {
    console.log(`🔄 Switching LLM provider to: ${provider}`);
    process.env.LLM_PROVIDER = provider;
    Object.assign(process.env, config);
    this.initializeProvider();
  }
}

// Singleton instance
let adapterInstance = null;

function getLLMAdapter() {
  if (!adapterInstance) {
    adapterInstance = new LLMAdapter();
  }
  return adapterInstance;
}

module.exports = { getLLMAdapter, LLMAdapter };
