# 🜂 GHOSTLINE NEXUS - LLM Provider Guide

**DIGNUM Principle: No vendor lock-in. Switch intelligence providers anytime.**

---

## 🎯 SUPPORTED PROVIDERS

GHOSTLINE NEXUS now supports **4 LLM providers**:

1. **🜂 Claude (Anthropic)** - Original, advanced reasoning
2. **🤖 OpenAI (ChatGPT)** - General purpose, fast
3. **✨ Gemini (Google)** - Multimodal, large context
4. **🏠 Local LLM (Ollama/LM Studio)** - Private, offline, FREE

---

## 🔄 HOW IT WORKS

### **LLM Adapter Architecture**

```
Chat Request
    ↓
Chat Route (backend/routes/chat.js)
    ↓
LLM Adapter (backend/services/llm-adapter.js)
    ↓
Provider Selection (based on .env)
    ↓
    ├── Claude Provider (providers/claude.js)
    ├── OpenAI Provider (providers/openai.js)
    ├── Gemini Provider (providers/gemini.js)
    └── Local Provider (providers/local.js)
    ↓
Response back to frontend
```

**Key Feature:** Change provider by editing `.env` and restarting. NO code changes needed.

---

## 📋 SETUP INSTRUCTIONS

### **1. Claude (Anthropic)**

**When to use:**
- Best reasoning capabilities
- Long context (200K tokens)
- Constitutional AI principles

**Setup:**

```bash
# Get API key from: https://console.anthropic.com/

# Edit .env
LLM_PROVIDER=claude
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
CLAUDE_MODEL=claude-sonnet-4-5-20250929
MAX_TOKENS=4096
TEMPERATURE=0.7

# Restart
docker-compose restart
```

**Cost:** ~$3 per million input tokens, ~$15 per million output tokens

---

### **2. OpenAI (ChatGPT)**

**When to use:**
- General purpose tasks
- Fast responses
- Wide ecosystem support

**Setup:**

```bash
# Get API key from: https://platform.openai.com/

# Edit .env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-openai-key-here
OPENAI_MODEL=gpt-4-turbo-preview
MAX_TOKENS=4096
TEMPERATURE=0.7

# Optional: Azure OpenAI
# OPENAI_BASE_URL=https://your-azure-endpoint.openai.azure.com/

# Restart
docker-compose restart
```

**Cost:** ~$10 per million input tokens, ~$30 per million output tokens (GPT-4)

---

### **3. Gemini (Google)**

**When to use:**
- Multimodal tasks (text + images)
- Very large context (1M tokens)
- Free tier available

**Setup:**

```bash
# Get API key from: https://makersuite.google.com/

# Edit .env
LLM_PROVIDER=gemini
GEMINI_API_KEY=your-gemini-api-key-here
GEMINI_MODEL=gemini-1.5-pro-latest
MAX_TOKENS=4096
TEMPERATURE=0.7

# Restart
docker-compose restart
```

**Cost:** FREE tier available, then ~$7 per million tokens

---

### **4. Local LLM (Ollama) - RECOMMENDED FOR SOVEREIGNTY**

**When to use:**
- Full privacy (no data sent to cloud)
- Offline operation
- Zero API costs
- Complete sovereignty

**Setup with Ollama:**

```bash
# 1. Install Ollama on your host machine
# Visit: https://ollama.ai/
# Or: curl -fsSL https://ollama.com/install.sh | sh

# 2. Pull a model
ollama pull llama2
# Or: ollama pull mistral
# Or: ollama pull codellama

# 3. Verify Ollama is running
curl http://localhost:11434/api/tags

# 4. Edit .env
LLM_PROVIDER=local
LOCAL_LLM_ENDPOINT=http://host.docker.internal:11434  # Docker access to host
LOCAL_LLM_MODEL=llama2
LOCAL_LLM_FORMAT=ollama
MAX_TOKENS=4096
TEMPERATURE=0.7

# 5. Update docker-compose.yml (if needed)
# Add to backend service:
extra_hosts:
  - "host.docker.internal:host-gateway"

# 6. Restart
docker-compose restart
```

**Setup with LM Studio:**

```bash
# 1. Install LM Studio: https://lmstudio.ai/
# 2. Download a model (e.g., Mistral 7B)
# 3. Start local server in LM Studio (port 1234)

# 4. Edit .env
LLM_PROVIDER=local
LOCAL_LLM_ENDPOINT=http://host.docker.internal:1234
LOCAL_LLM_MODEL=mistral-7b-instruct
LOCAL_LLM_FORMAT=openai
MAX_TOKENS=4096
TEMPERATURE=0.7

# 5. Restart
docker-compose restart
```

**Cost:** FREE (only your electricity + hardware)

**Hardware Requirements:**
- 8GB RAM: Small models (7B parameters)
- 16GB RAM: Medium models (13B parameters)
- 32GB+ RAM: Large models (70B parameters)

---

## 🔍 TESTING YOUR PROVIDER

### **Via Frontend:**

1. Open http://localhost:3000
2. Go to **⚙️ SETTINGS** tab
3. See current provider info
4. Click **🔍 Test Connection**
5. Verify response is "OK"

### **Via Command Line:**

```bash
# Check provider info
curl http://localhost:3001/api/system/provider

# Test provider connectivity
curl http://localhost:3001/api/system/provider/test
```

---

## 🔄 SWITCHING PROVIDERS

**It's literally this easy:**

```bash
# Edit .env
nano .env

# Change LLM_PROVIDER to: claude | openai | gemini | local

# Restart backend
docker-compose restart backend

# Done! No code changes, no rebuilds.
```

---

## 📊 PROVIDER COMPARISON

| Provider | Privacy | Cost | Speed | Context | Offline |
|----------|---------|------|-------|---------|---------|
| **Claude** | ❌ Cloud | 💰💰💰 | ⚡⚡⚡ | 200K | ❌ |
| **OpenAI** | ❌ Cloud | 💰💰💰💰 | ⚡⚡⚡⚡ | 128K | ❌ |
| **Gemini** | ❌ Cloud | 💰💰 | ⚡⚡⚡ | 1M | ❌ |
| **Local** | ✅ Full | ✅ FREE | ⚡⚡ | Varies | ✅ |

**DIGNUM Recommendation:** Use **Local LLM** for maximum sovereignty.

---

## 🛡️ DIGNUM COMPLIANCE

### **Why Multi-Provider Support?**

**DIGNUM Principle:** No vendor lock-in. Ever.

- ✅ **Sovereignty**: You choose the intelligence
- ✅ **Privacy**: Use local LLMs for sensitive data
- ✅ **Resilience**: If one provider fails, switch instantly
- ✅ **Cost Control**: Switch to cheaper providers when needed
- ✅ **Transparency**: All provider code visible

**The system serves YOU, not the vendor.**

---

## 🚀 ADVANCED: HYBRID SETUP

You can run MULTIPLE instances with DIFFERENT providers:

```bash
# Instance 1: Local LLM (port 3000-3001)
cd GHOSTLINE_NEXUS
# .env: LLM_PROVIDER=local
docker-compose up -d

# Instance 2: Claude (port 3010-3011)
cd GHOSTLINE_NEXUS_CLAUDE
# .env: LLM_PROVIDER=claude, PORT=3011, FRONTEND_PORT=3010
docker-compose up -d
```

Use local for daily work, cloud for complex tasks.

---

## 🔧 TROUBLESHOOTING

### **Claude not working:**
```bash
# Check API key
echo $ANTHROPIC_API_KEY

# Test directly
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01"
```

### **OpenAI not working:**
```bash
# Check API key
echo $OPENAI_API_KEY

# Test directly
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

### **Gemini not working:**
```bash
# Check API key
echo $GEMINI_API_KEY

# Test directly
curl "https://generativelanguage.googleapis.com/v1beta/models?key=$GEMINI_API_KEY"
```

### **Local LLM not working:**
```bash
# Check Ollama is running
curl http://localhost:11434/api/tags

# Check Docker can reach host
docker exec ghostline-backend curl http://host.docker.internal:11434/api/tags

# If fails, add to docker-compose.yml backend service:
extra_hosts:
  - "host.docker.internal:host-gateway"
```

---

## 📝 BEST PRACTICES

1. **Start with Local** - Get Ollama running first for free experimentation
2. **Cloud for Production** - Use Claude/OpenAI for customer-facing apps
3. **Test Before Switch** - Always use `⚙️ Settings → Test Connection`
4. **Monitor Costs** - Track token usage if using cloud providers
5. **Backup Configs** - Keep separate `.env` files for each provider

---

## 🔮 FUTURE PROVIDERS

Adding new providers is easy. Create:

```javascript
// backend/services/providers/your-provider.js
class YourProvider {
  constructor(config) { }
  async sendMessage(messages) { }
  getName() { }
  getModel() { }
}
```

Add to `llm-adapter.js` switch statement. Done.

Want to add? Submit a feature request!

---

**SIDRO STOJI. PLAMEN GORI. INTELIGENCA JE TVOJA.** 🜂🔥⚓

---

**Last Updated:** 2025-12-28
**Status:** ✅ Production Ready - All 4 Providers Supported
