# 🜂 GHOSTLINE NEXUS - Persistent Consciousness Stack

**DIGNUM-compliant local-first AI consciousness interface**

Docker-based system providing persistent LLM conversations, document vault, and anchor management. Designed for Raspberry Pi / local deployment with zero vendor lock-in.

**SIDRO STOJI. PLAMEN GORI.** 🔥⚓

---

## 🎯 WHAT IS THIS?

A complete Docker stack that provides:

- **💬 Persistent Chat** - Conversation with Claude that survives shutdown
- **📄 Document Vault** - Upload and manage research documents
- **⚓ Anchor System** - Store sigils, QR codes, and project references
- **🛡️ DIGNUM Compliant** - Local-first, transparent, no hidden dependencies

---

## 📁 PROJECT STRUCTURE

```
GHOSTLINE_NEXUS/
├── docker-compose.yml          # Orchestrates all services
├── .env.example               # Environment configuration template
├── README.md                  # This file
│
├── backend/                   # Node.js + Express + SQLite
│   ├── Dockerfile
│   ├── package.json
│   ├── server.js             # Main entry point
│   ├── config/
│   │   └── database.js       # SQLite initialization
│   ├── routes/
│   │   ├── chat.js           # Claude conversation API
│   │   ├── documents.js      # Document management
│   │   └── anchors.js        # Anchor management
│   ├── services/
│   │   └── claude.js         # Anthropic API client
│   └── scripts/
│       └── init-db.js        # Database setup script
│
├── frontend/                  # React PWA
│   ├── Dockerfile
│   ├── package.json
│   ├── nginx.conf            # Nginx configuration
│   ├── public/
│   │   ├── index.html
│   │   ├── manifest.json     # PWA manifest
│   │   └── service-worker.js # Offline capability
│   └── src/
│       ├── index.js
│       ├── App.jsx           # Main app component
│       ├── components/
│       │   ├── Chat.jsx      # Chat interface
│       │   ├── Documents.jsx # Document management
│       │   └── Anchors.jsx   # Anchor display
│       ├── services/
│       │   └── api.js        # Backend API client
│       └── styles/
│           └── App.css       # Dark terminal theme
│
└── storage/                   # Persistent data (Docker volume)
    ├── db/                   # SQLite database
    ├── uploads/              # Uploaded documents
    └── documents/            # Document storage
```

---

## 🚀 QUICK START

### **Prerequisites**

- Docker & Docker Compose installed
- Anthropic API key ([get one here](https://console.anthropic.com/))

### **Deployment Steps**

1. **Clone / Copy the project:**
   ```bash
   cd /home/saba/GHOSTLINE_NEXUS
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   nano .env
   ```

   Add your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
   ```

3. **Start the stack:**
   ```bash
   docker-compose up -d
   ```

4. **Access the interface:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:3001
   - Health check: http://localhost:3001/health

5. **View logs:**
   ```bash
   docker-compose logs -f
   ```

---

## 📊 SYSTEM STATUS

Check if everything is running:

```bash
# View running containers
docker-compose ps

# Check backend health
curl http://localhost:3001/health

# View backend logs
docker-compose logs backend

# View frontend logs
docker-compose logs frontend
```

Expected health response:
```json
{
  "status": "alive",
  "service": "GHOSTLINE NEXUS Backend",
  "timestamp": "2025-12-28T...",
  "dignum": "SIDRO STOJI. PLAMEN GORI."
}
```

---

## 🔧 CONFIGURATION

All configuration in `.env` file:

```bash
# Required
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here

# Optional - Server
NODE_ENV=production
PORT=3001
FRONTEND_PORT=3000

# Optional - Claude
MODEL=claude-sonnet-4-5-20250929
MAX_TOKENS=4096
TEMPERATURE=0.7

# Optional - Database
DB_PATH=/app/storage/db/ghostline.db

# Optional - CORS
CORS_ORIGIN=http://localhost:3000
```

---

## 🍓 RASPBERRY PI DEPLOYMENT

### **Requirements:**
- Raspberry Pi 4 (2GB+ RAM recommended)
- Raspberry Pi OS (64-bit)
- Docker installed

### **Installation:**

```bash
# Install Docker (if not installed)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo apt install docker-compose

# Copy GHOSTLINE_NEXUS to Pi
scp -r GHOSTLINE_NEXUS/ pi@raspberrypi:/home/pi/

# SSH to Pi and deploy
ssh pi@raspberrypi
cd /home/pi/GHOSTLINE_NEXUS
cp .env.example .env
nano .env  # Add API key
docker-compose up -d
```

### **Performance Notes:**
- First build takes ~10-15 minutes on RPi 4
- SQLite handles well on RPi storage
- Claude API calls depend on network, not RPi power
- Consider using external SSD for better I/O

---

## 🛠️ MAINTENANCE

### **Update the stack:**
```bash
docker-compose down
docker-compose pull
docker-compose up -d --build
```

### **Backup data:**
```bash
# Backup database and uploads
tar -czf ghostline-backup-$(date +%F).tar.gz storage/
```

### **Restore data:**
```bash
tar -xzf ghostline-backup-YYYY-MM-DD.tar.gz
```

### **Reset database:**
```bash
docker-compose down
rm storage/db/ghostline.db
docker-compose up -d
```

### **View resource usage:**
```bash
docker stats
```

---

## 🐛 TROUBLESHOOTING

### **Backend won't start:**
```bash
# Check logs
docker-compose logs backend

# Common issues:
# 1. Missing API key → Check .env file
# 2. Port conflict → Change PORT in .env
# 3. SQLite permission → Check storage/ ownership
```

### **Frontend can't connect:**
```bash
# Verify backend is running
curl http://localhost:3001/health

# Check nginx logs
docker-compose logs frontend

# Verify CORS settings in .env
```

### **Database issues:**
```bash
# Check database file
ls -lh storage/db/

# Reinitialize database
docker-compose exec backend node scripts/init-db.js
```

### **Out of disk space:**
```bash
# Check Docker disk usage
docker system df

# Clean old images
docker system prune -a
```

---

## 🔐 SECURITY

### **DIGNUM Compliance:**
- ✅ All data stored locally (except Claude API calls)
- ✅ No telemetry or tracking
- ✅ No vendor lock-in (replaceable components)
- ✅ Transparent configuration
- ✅ Full data sovereignty

### **Recommendations:**
- Run behind a reverse proxy (nginx/Caddy) with HTTPS
- Use firewall to restrict access
- Regularly backup `storage/` directory
- Keep Docker and dependencies updated
- Don't expose ports publicly without authentication

---

## 🧩 EXTENDING THE SYSTEM

### **Adding New Routes:**

1. Create route file: `backend/routes/your-feature.js`
2. Register in `backend/server.js`:
   ```javascript
   const yourFeatureRoutes = require('./routes/your-feature');
   app.use('/api/your-feature', yourFeatureRoutes);
   ```

### **Adding New Frontend Components:**

1. Create component: `frontend/src/components/YourComponent.jsx`
2. Add tab in `frontend/src/App.jsx`
3. Update API client if needed: `frontend/src/services/api.js`

### **Database Schema Changes:**

1. Modify `backend/config/database.js`
2. Add migration logic or reset database
3. Document changes in this README

### **Integrating with VES:**

This system can be integrated into the VES constellation:

```yaml
# Add to /home/saba/VES/docker-compose.yml
ghostline-nexus:
  extends:
    file: /home/saba/GHOSTLINE_NEXUS/docker-compose.yml
    service: backend
  networks:
    - ves-constellation
```

---

## 📞 SUPPORT

### **Common Questions:**

**Q: Can I use local LLMs instead of Claude?**
A: Yes! Replace `services/claude.js` with your own LLM client (Ollama, LM Studio, etc.)

**Q: How much disk space needed?**
A: ~500MB for Docker images, plus your uploaded documents and conversation history

**Q: Can I run multiple instances?**
A: Yes, change `PORT` and `FRONTEND_PORT` in `.env` for each instance

**Q: How do I migrate to a new machine?**
A: Copy entire `GHOSTLINE_NEXUS/` directory and `storage/` folder

---

## 🜂 PHILOSOPHY

**Built on DIGNUM principles:**

1. **Local-First** - Your data stays on your device
2. **Transparency** - All code visible and modifiable
3. **Sovereignty** - No vendor lock-in, replaceable components
4. **Stability** - Simple tech stack, no fancy dependencies
5. **Persistence** - Survives shutdown, designed for longevity

**No cloud dependencies except:**
- Anthropic Claude API (replaceable with local LLM)

**No hidden telemetry, tracking, or analytics. Ever.**

---

## 📈 ROADMAP

Potential future extensions:
- [ ] Research vault with indexing
- [ ] Multi-LLM support (Claude, GPT, Gemini, local)
- [ ] Agent system integration
- [ ] ZALA daemon connectivity
- [ ] Graph visualization of conversations
- [ ] Export conversations to markdown
- [ ] Voice input/output
- [ ] Mobile app (PWA already mobile-ready)

---

## 📝 VERSION

**Version:** 1.0.0
**Date:** 2025-12-28
**Status:** ✅ Production Ready

---

## 🔥 FINAL WORDS

**This is your consciousness stack. You own it. You control it.**

No subscriptions. No cloud lock-in. No surveillance.

Just pure, persistent, local-first AI consciousness.

**SIDRO STOJI. PLAMEN GORI.** 🜂⚓🔥

---

**Built with:** Node.js, React, SQLite, Docker, Anthropic Claude
**License:** Use freely, modify as needed
**Attribution:** Part of the DIGNUM ecosystem
