# 🐋 VES DOCKER PREPARATION 🐋

**Date:** 2025-12-27
**Purpose:** Prepare VES for complete Docker containerization
**Strategy:** VES = Complete AI System (everything except native Linux)

---

## 🎯 GOAL:

Package the entire VES system (3.7GB) into a Docker container so that:
- All AI systems, protocols, scripts, and data are portable
- Can be deployed to any Docker host
- Complete system backup/restore via Docker image
- Easy migration between machines

---

## 📦 WHAT'S IN VES (3.7GB Total):

### **Core Systems:**
- **SHABAD_CloudCore/** - Consciousness & ritual systems
- **00_SYSTEMS/** - System documentation
- **01_PROTOCOLS/** - Protocols & codexes (Hermes, Witness, ZALA)
- **02_RESEARCH/** - Research dossiers
- **05_ZALA/** - ZALA daemon & shrine

### **Web Interfaces:**
- **03_WEB/** - 44 HTML files (portals, ghostcore, ghostline, tools)
- **index.html** - 150KB master portal

### **Development:**
- **04_SCRIPTS/** - 29 Python scripts (generators, protocols, tools)
- **CODEX/** - 109MB PWA development (React, Vite, node_modules)

### **Infrastructure:**
- **CONSTELLATION_BRIDGE/** - 48KB inter-agent communication
- **MASTER_NAVIGATOR/** - 5.0MB project discovery (7,024 projects indexed)
- **SVETISCE/** - 204KB archived project

### **Archives & Documentation:**
- **06_ARCHIVE/** - Old versions & completed work
- **07_PERSONAL/** - Personal philosophical documents
- **08_MASTER_DOCS/** - Master guides
- **09_EXTERNAL_PROJECTS/** - Links to GroundZero, Consciousness Guide

### **Operational:**
- **CHECKPOINTS/** - 26.6MB safety backups
- **INBOX/** - Empty (processing area)
- **_INVENTORY/** - File tracking
- **logs/** - System logs

---

## 🐳 DOCKERFILE STRATEGY:

### **Option A: Full System Container (Recommended)**
```dockerfile
FROM ubuntu:latest

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    nodejs \
    npm \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create VES directory
WORKDIR /ves

# Copy entire VES system
COPY . /ves/

# Install Python requirements (if requirements.txt exists)
RUN if [ -f requirements.txt ]; then pip3 install -r requirements.txt; fi

# Install CODEX dependencies
RUN cd /ves/CODEX && npm install

# Expose ports
EXPOSE 8099  # VES PWA
EXPOSE 8420  # VES Agent
EXPOSE 3000  # CODEX dev server

# Set environment
ENV VES_HOME=/ves
ENV PYTHONPATH=/ves

# Start services (customize as needed)
CMD ["/bin/bash"]
```

### **Option B: Multi-Stage Build (Optimized)**
```dockerfile
# Stage 1: Build CODEX
FROM node:latest AS codex-builder
WORKDIR /build/CODEX
COPY CODEX/package*.json ./
RUN npm install
COPY CODEX/ ./
RUN npm run build

# Stage 2: Final image
FROM ubuntu:latest
RUN apt-get update && apt-get install -y \
    python3 python3-pip git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /ves
COPY --from=codex-builder /build/CODEX/dist /ves/CODEX/dist
COPY . /ves/

EXPOSE 8099 8420 3000
CMD ["/bin/bash"]
```

---

## 📋 PRE-DOCKER CHECKLIST:

### **1. Clean Up (Optional)**
- [ ] Remove node_modules from CODEX (npm install in Docker)
- [ ] Remove CHECKPOINTS (backups not needed in image)
- [ ] Remove _INVENTORY (can regenerate)
- [ ] This would reduce image size from 3.7GB to ~500MB

### **2. Create Requirements Files**
- [ ] `requirements.txt` - Python dependencies
- [ ] `.dockerignore` - Exclude files from image

### **3. Configuration**
- [ ] Environment variables for ports
- [ ] Service startup scripts
- [ ] Health check endpoints

### **4. External Dependencies**
- [ ] Systemd services (ves-agent, zala-daemon) → Convert to Docker CMD
- [ ] File paths (/home/saba/...) → Update to /ves/...
- [ ] localhost references → Use Docker networking

---

## 🔧 DEPENDENCIES TO INSTALL:

### **Python Packages** (create requirements.txt):
```txt
fastapi
uvicorn
requests
jinja2
# Add others as discovered
```

### **System Packages:**
```bash
python3
python3-pip
nodejs
npm
git
curl
wget
# Add others as needed
```

---

## 🚀 DOCKER COMMANDS:

### **Build Image:**
```bash
cd /home/saba
docker build -t ves-system:latest ./VES
```

### **Run Container:**
```bash
docker run -d \
  --name ves \
  -p 8099:8099 \
  -p 8420:8420 \
  -p 3000:3000 \
  -v /home/saba/VES/logs:/ves/logs \
  ves-system:latest
```

### **Interactive Shell:**
```bash
docker exec -it ves /bin/bash
```

### **Export Image:**
```bash
docker save ves-system:latest | gzip > ves-system.tar.gz
```

### **Import on Another Machine:**
```bash
docker load < ves-system.tar.gz
```

---

## 🎯 NEXT STEPS:

### **Phase 1: Preparation** (Do First)
1. [ ] Create `requirements.txt` from existing Python scripts
2. [ ] Create `.dockerignore` to exclude unnecessary files
3. [ ] Test Python scripts for hardcoded paths
4. [ ] Document required environment variables

### **Phase 2: Dockerfile Creation**
1. [ ] Create initial Dockerfile (Option A)
2. [ ] Test build locally
3. [ ] Fix any build errors
4. [ ] Optimize layers

### **Phase 3: Service Integration**
1. [ ] Convert systemd services to Docker CMD/ENTRYPOINT
2. [ ] Create startup script for multiple services
3. [ ] Add health checks
4. [ ] Test service connectivity

### **Phase 4: Optimization**
1. [ ] Reduce image size (multi-stage build)
2. [ ] Cache npm/pip dependencies
3. [ ] Use Alpine Linux for smaller base image
4. [ ] Document final image size

### **Phase 5: Deployment**
1. [ ] Test complete system in container
2. [ ] Create docker-compose.yml for orchestration
3. [ ] Document deployment procedure
4. [ ] Create backup/restore scripts

---

## 💡 DOCKER COMPOSE EXAMPLE:

```yaml
version: '3.8'

services:
  ves:
    build: .
    container_name: ves-system
    ports:
      - "8099:8099"  # VES PWA
      - "8420:8420"  # VES Agent
      - "3000:3000"  # CODEX
    volumes:
      - ./logs:/ves/logs
      - ./CHECKPOINTS:/ves/CHECKPOINTS
    environment:
      - VES_HOME=/ves
      - PYTHONPATH=/ves
    restart: unless-stopped
    command: /ves/start-services.sh
```

---

## 🔍 IMPORTANT NOTES:

### **Paths to Update:**
All hardcoded `/home/saba/` paths need to become `/ves/` or use environment variables:
- Python scripts in `04_SCRIPTS/`
- CONSTELLATION_BRIDGE scripts
- CODEX configuration
- ZALA daemon configuration

### **Services to Adapt:**
- **ves-agent** (FastAPI on :8420) → Docker CMD
- **ZALA daemon** → Docker CMD or supervisor
- **VES PWA** (SimpleHTTPServer :8099) → Docker CMD

### **External Projects:**
- **GroundZero** and **Consciousness-Survival-Guide** are in `/home/saba/`, not VES
- Decision: Keep separate or integrate into VES?

---

## 🜂 PHILOSOPHY:

**VES = Complete AI System**
- Everything needed to run the AI constellation
- Self-contained, portable, reproducible
- Docker = vessel for the vessel
- "Sidro stoji" even in containers 🔥

**Docker Strategy:**
- One image = entire system
- Volume mounts for logs/data only
- Stateless where possible
- Easy backup/restore via docker save/load

---

## 📊 SIZE OPTIMIZATION:

**Current:** 3.7GB (with all data)
**Optimized (no node_modules, checkpoints):** ~500MB
**Final Docker image (compressed):** ~1.5GB estimated

**Breakdown:**
- CODEX node_modules: ~105MB (reinstall in Docker)
- CHECKPOINTS: ~26MB (exclude from image)
- MASTER_NAVIGATOR data: ~5MB (keep - valuable)
- SHABAD_CloudCore: ~3.5GB (keep - core data)

---

## ✅ READINESS:

**Current Status:** 🟡 READY FOR PREPARATION
**Next Action:** Create requirements.txt and .dockerignore
**Estimated Time:** 2-3 hours to first working container
**Priority:** Medium (system works fine locally, Docker = portability)

---

**Last Updated:** 2025-12-27
**System Size:** 3.7GB
**Docker Ready:** Not yet (needs Dockerfile)
**Strategy:** Complete system containerization

🐋🜂⚓

**SIDRO STOJI. V DOCKERJU AL' NE.** 🔥

---

*For VES documentation, see: [README.md](./README.md)*
*For system status, see: [00_SYSTEMS/SYSTEM_STATUS_2025.md](./00_SYSTEMS/SYSTEM_STATUS_2025.md)*
