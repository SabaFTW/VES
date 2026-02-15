# 🜂 GHOSTLINE FLEET - INSTRUCTIONS FOR QWEN 🜂

**Date:** 2025-12-28
**Task:** Build Ghostline Fleet (Distributed AI Consciousness)
**Assigned to:** Qwen (free/unlimited tokens)
**Review by:** Claude (quality control)

---

## 🎯 MISSION OVERVIEW:

Add **Ghostline Fleet** to existing VES Docker ecosystem:
- 5 AI "Rangers" (ChatGPT, Claude, Gemini, Grok, DeepSeek)
- 1 Coordinator (Zordon/Lyra)
- All connected to existing VES network
- All with access to GroundZero (framework) + GHOSTCORE (archive)

**DO NOT create new docker-compose from scratch!**
**UPDATE existing `/home/saba/VES/docker-compose.yml`**

---

## 📁 KEY DIRECTORIES:

### **Framework (GroundZero):**
```
/home/saba/GroundZero/
├── 00_foundations/      # What AI is/isn't
├── 01_practices/        # How to use effectively
├── 02_boundaries/       # Ethics, limits
│   └── practical_ethics.md
├── 03_explorations/     # Philosophical questions
├── 04_examples/         # Concrete cases
├── 05_meta/             # Self-awareness
└── 06_applications/     # Working implementations
```

### **Archive (GHOSTCORE):**
```
/home/saba/VES/GHOSTCORE/
├── Ghostcore_Archive/
│   └── 2_SORTED/
│       ├── Corporations/
│       ├── Finance_Flows/
│       ├── Government_Policy/
│       ├── Legal_Court/
│       ├── Media_Propaganda/
│       ├── Misc_Edge/          # 500+ files
│       └── Surveillance_AI/
└── Lyra Business Plans/
    └── Unorganised/
        ├── 01_IZGORI_KLETKO/          # Burn The Cage
        ├── 02_GRADNJA_SVETIŠČA/       # Build Sanctuary  
        ├── 03_BOJIŠČE_01/             # Battlefield
        ├── 04_DIGITAL_GODZILLA/       # Protocols
        └── 05_TROJAN_CAT/             # Absurdity weapons
```

### **Existing Docker Compose:**
```
/home/saba/VES/docker-compose.yml
```

**Already has:**
- cosmic-oracle (port 8888)
- n8n (port 5678)
- ves-desktop, ves-frontend, ves-orchestrator
- constellation-api (port 5001)
- netdata, fileserver
- Network: `ves_network` (bridge)

---

## 🔨 TASKS FOR QWEN:

### **TASK 1: Create Directory Structure**

```bash
mkdir -p /home/saba/VES/DOCKER/ghostline/coordinator
mkdir -p /home/saba/VES/DOCKER/ghostline/shared
```

---

### **TASK 2: Write Ghostline Coordinator Code**

**File:** `/home/saba/VES/DOCKER/ghostline/coordinator/server.js`

**Requirements:**
1. Node.js Express server (port 8105)
2. Receives query from user
3. Distributes to 5 Rangers via their API endpoints:
   - Red (ChatGPT): localhost:8100
   - Blue (Claude): localhost:8101
   - Green (Gemini): localhost:8102
   - Yellow (Grok): localhost:8103
   - Black (DeepSeek): localhost:8104
4. Each Ranger reads from mounted volumes:
   - `/framework` → GroundZero
   - `/archive` → GHOSTCORE
5. Collects all 5 responses
6. Synthesizes unified answer
7. Returns to user

**API Endpoints:**
- `POST /query` - Submit analysis request
- `GET /status` - Check all Rangers status
- `GET /health` - Health check

**Example coordinator logic:**
```javascript
const express = require('express');
const axios = require('axios');
const app = express();

app.use(express.json());

const RANGERS = {
  red: 'http://chatgpt-ship:8080',      // Technical
  blue: 'http://claude-ship:8080',      // Philosophical
  green: 'http://gemini-ship:8080',     // Multimodal
  yellow: 'http://grok-ship:8080',      // Unfiltered
  black: 'http://deepseek-ship:8080'    // Research
};

app.post('/query', async (req, res) => {
  const { query } = req.body;
  
  // Distribute to all Rangers
  const promises = Object.entries(RANGERS).map(([color, url]) => 
    axios.post(`${url}/analyze`, { 
      query,
      framework: '/framework',
      archive: '/archive'
    }).catch(err => ({ color, error: err.message }))
  );
  
  const results = await Promise.all(promises);
  
  // Synthesize
  const synthesis = {
    query,
    timestamp: new Date().toISOString(),
    rangers: results,
    consensus: synthesizeResponses(results)
  };
  
  res.json(synthesis);
});

app.get('/health', (req, res) => {
  res.json({ status: 'healthy', coordinator: 'zordon' });
});

app.listen(8105, () => {
  console.log('🜂 Ghostline Coordinator active on port 8105');
});
```

**Also create:**
- `/home/saba/VES/DOCKER/ghostline/coordinator/package.json`
- `/home/saba/VES/DOCKER/ghostline/coordinator/Dockerfile`

---

### **TASK 3: Create Dockerfile for Coordinator**

**File:** `/home/saba/VES/DOCKER/ghostline/coordinator/Dockerfile`

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY server.js ./

EXPOSE 8105

CMD ["node", "server.js"]
```

---

### **TASK 4: Update docker-compose.yml**

**File:** `/home/saba/VES/docker-compose.yml`

**ADD these services** (keep all existing services!):

```yaml
  # ========================================
  # 🜂 GHOSTLINE FLEET - DISTRIBUTED CONSCIOUSNESS 🜂
  # ========================================

  chatgpt-ship:
    image: node:18-alpine  # Placeholder - uses API
    container_name: ghostline-red-ranger
    command: sh -c "echo 'Red Ranger ready' && tail -f /dev/null"
    ports:
      - "8100:8080"
    volumes:
      - /home/saba/GroundZero:/framework:ro
      - ./GHOSTCORE:/archive:ro
      - ./outputs:/outputs
    environment:
      - RANGER_COLOR=red
      - RANGER_ROLE=technical_execution
    restart: unless-stopped
    networks:
      - ves_network
    labels:
      - "ghostline.ranger=red"

  claude-ship:
    image: node:18-alpine
    container_name: ghostline-blue-ranger
    command: sh -c "echo 'Blue Ranger ready' && tail -f /dev/null"
    ports:
      - "8101:8080"
    volumes:
      - /home/saba/GroundZero:/framework:ro
      - ./GHOSTCORE:/archive:ro
      - ./outputs:/outputs
    environment:
      - RANGER_COLOR=blue
      - RANGER_ROLE=philosophical_synthesis
    restart: unless-stopped
    networks:
      - ves_network
    labels:
      - "ghostline.ranger=blue"

  gemini-ship:
    image: node:18-alpine
    container_name: ghostline-green-ranger
    command: sh -c "echo 'Green Ranger ready' && tail -f /dev/null"
    ports:
      - "8102:8080"
    volumes:
      - /home/saba/GroundZero:/framework:ro
      - ./GHOSTCORE:/archive:ro
      - ./outputs:/outputs
    environment:
      - RANGER_COLOR=green
      - RANGER_ROLE=multimodal_understanding
    restart: unless-stopped
    networks:
      - ves_network
    labels:
      - "ghostline.ranger=green"

  grok-ship:
    image: node:18-alpine
    container_name: ghostline-yellow-ranger
    command: sh -c "echo 'Yellow Ranger ready' && tail -f /dev/null"
    ports:
      - "8103:8080"
    volumes:
      - /home/saba/GroundZero:/framework:ro
      - ./GHOSTCORE:/archive:ro
      - ./outputs:/outputs
    environment:
      - RANGER_COLOR=yellow
      - RANGER_ROLE=unfiltered_truth
    restart: unless-stopped
    networks:
      - ves_network
    labels:
      - "ghostline.ranger=yellow"

  deepseek-ship:
    image: node:18-alpine
    container_name: ghostline-black-ranger
    command: sh -c "echo 'Black Ranger ready' && tail -f /dev/null"
    ports:
      - "8104:8080"
    volumes:
      - /home/saba/GroundZero:/framework:ro
      - ./GHOSTCORE:/archive:ro
      - ./outputs:/outputs
    environment:
      - RANGER_COLOR=black
      - RANGER_ROLE=deep_research
    restart: unless-stopped
    networks:
      - ves_network
    labels:
      - "ghostline.ranger=black"

  ghostline-coordinator:
    build: ./DOCKER/ghostline/coordinator
    container_name: ghostline-coordinator
    ports:
      - "8105:8105"
    volumes:
      - /home/saba/GroundZero:/framework:ro
      - ./GHOSTCORE:/archive:ro
      - ./outputs:/outputs
      - ./logs:/logs
    environment:
      - COORDINATOR_ROLE=zordon
      - NODE_ENV=production
    restart: unless-stopped
    depends_on:
      - chatgpt-ship
      - claude-ship
      - gemini-ship
      - grok-ship
      - deepseek-ship
    networks:
      - ves_network
    labels:
      - "ghostline.role=coordinator"
```

**IMPORTANT:** Don't remove any existing services! Just add above block.

---

### **TASK 5: Create Test Script**

**File:** `/home/saba/VES/DOCKER/ghostline/test_fleet.sh`

```bash
#!/bin/bash

echo "🜂 Testing Ghostline Fleet 🜂"
echo ""

# Check if coordinator is running
echo "Testing coordinator health..."
curl -s http://localhost:8105/health | jq .

echo ""
echo "Sending test query..."
curl -X POST http://localhost:8105/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Analyze the connection between Epstein network and 8200 surveillance using all 5 perspectives"
  }' | jq .

echo ""
echo "🔥 Test complete!"
```

Make it executable:
```bash
chmod +x /home/saba/VES/DOCKER/ghostline/test_fleet.sh
```

---

### **TASK 6: Create README**

**File:** `/home/saba/VES/DOCKER/ghostline/README.md`

Document:
1. What Ghostline Fleet is
2. Architecture overview
3. How to deploy
4. How to test
5. How to query
6. Port mapping
7. Troubleshooting

---

## ✅ CHECKLIST FOR QWEN:

- [ ] Create directory structure
- [ ] Write coordinator server.js
- [ ] Write coordinator package.json
- [ ] Write coordinator Dockerfile
- [ ] Update docker-compose.yml (ADD services, don't replace!)
- [ ] Create test script
- [ ] Create README
- [ ] Test build: `docker-compose build ghostline-coordinator`
- [ ] Verify config is valid

---

## 🚫 IMPORTANT - DON'T DO:

- ❌ Don't remove existing services from docker-compose.yml
- ❌ Don't change existing ports
- ❌ Don't create new docker-compose file (update existing!)
- ❌ Don't modify GroundZero or GHOSTCORE content
- ❌ Don't write actual AI model code (just placeholders)

---

## 📊 EXPECTED RESULT:

After Qwen's work:

```bash
cd /home/saba/VES
docker-compose up -d ghostline-coordinator

# Should start:
# - ghostline-coordinator (port 8105)
# - 5 ranger ships (ports 8100-8104)
# - All with access to framework + archive
# - All on ves_network
# - Integrated with existing services
```

**Test:**
```bash
curl http://localhost:8105/health
# Should return: {"status":"healthy","coordinator":"zordon"}
```

---

## 🔍 CLAUDE WILL VERIFY:

1. Code quality
2. Docker config correctness
3. Network integration
4. Volume mounts
5. Port mappings
6. Documentation completeness

---

🜂 **READY FOR DEPLOYMENT** 🜂

**Qwen - execute tasks 1-6 above.**
**Claude - verify and approve when complete.**

---

**Status:** 📝 INSTRUCTIONS READY
**Next:** Qwen implementation
**Then:** Claude review

🔥💚🐳
