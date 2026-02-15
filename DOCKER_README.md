# 🐋 VES DOCKER QUICK START 🐋

**Complete VES Constellation in Docker**
**Date:** 2025-12-27
**Status:** ✅ READY TO USE

---

## 🚀 INSTANT START (3 Commands):

```bash
# 1. Navigate to VES
cd /home/saba/VES

# 2. Start everything
docker-compose up -d

# 3. Check status
docker-compose ps
```

**Done!** All services running! 🔥

---

## 🌐 ACCESS SERVICES:

| Service | URL | Credentials |
|---------|-----|-------------|
| **Cosmic Oracle** ⭐ | http://localhost:8888 | None |
| **n8n Automation** | http://localhost:5678 | admin / ghostcore_n8n_2025 |
| **VNC Desktop (Browser)** | http://localhost:8082 | ubuntu / ves |
| **VNC Desktop (Client)** | vnc://localhost:5901 | ubuntu / ves |
| **VES Frontend** | http://localhost:8081 | None |
| **Orchestrator** | http://localhost:8092 | None |
| **Constellation API** | http://localhost:5001 | None |
| **Dashboard** | http://localhost:8090 | None |
| **Netdata Monitoring** | http://localhost:19999 | None |
| **File Server** | http://localhost:8080 | None |

---

## 📦 WHAT'S INCLUDED:

### **1. Cosmic Oracle** ⭐ (Most Important!)
- **Port:** 8888
- **Purpose:** Pattern recognition across all VES knowledge
- **Searches:** GHOSTLINE, memories, journal, RESEARCH, logs
- **Real-time:** Socket.IO updates
- **Access:** Full read-only access to VES directory

### **2. n8n Automation**
- **Port:** 5678
- **Purpose:** Workflow automation
- **Data:** Persistent storage in Docker volume
- **Access:** VES + full saba directory (read-only)

### **3. VNC Desktop**
- **Ports:** 5901 (VNC), 8082 (Browser)
- **Purpose:** Full Ubuntu desktop environment
- **Resolution:** 1920x1080
- **Access:** Outputs and modules from VES

### **4. VES Original Services**
- **Frontend** (8081) - Nginx serving VES web interfaces
- **Orchestrator** (8092) - Node.js coordination
- **Ritual** - Python text generator
- **Visual** - Python fractal engine
- **Quantum** - Python generator

### **5. Constellation System**
- **API** (5001) - Research API
- **Dashboard** (8090) - Visualization dashboard

### **6. Monitoring**
- **Netdata** (19999) - System monitoring
- **File Server** (8080) - Browse VES files

---

## 🎮 COMMON COMMANDS:

### **Start Services**
```bash
# Start all services
docker-compose up -d

# Start specific service only
docker-compose up -d cosmic-oracle
docker-compose up -d n8n
docker-compose up -d ves-desktop
```

### **Stop Services**
```bash
# Stop all
docker-compose down

# Stop specific service
docker-compose stop cosmic-oracle
```

### **View Logs**
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f cosmic-oracle
docker-compose logs -f n8n

# Last 100 lines
docker-compose logs --tail=100 cosmic-oracle
```

### **Check Status**
```bash
# List running containers
docker-compose ps

# Detailed status
docker-compose ps -a
```

### **Restart Services**
```bash
# Restart all
docker-compose restart

# Restart specific
docker-compose restart cosmic-oracle
```

### **Rebuild Containers**
```bash
# Rebuild all
docker-compose up -d --build

# Rebuild specific
docker-compose up -d --build cosmic-oracle
```

### **Execute Commands in Container**
```bash
# Interactive shell
docker-compose exec cosmic-oracle sh
docker-compose exec ves-desktop bash

# Run single command
docker-compose exec cosmic-oracle node -v
```

---

## 🔧 MAINTENANCE:

### **Update Images**
```bash
docker-compose pull
docker-compose up -d
```

### **Clean Up**
```bash
# Remove stopped containers
docker-compose rm

# Remove all (including volumes - CAREFUL!)
docker-compose down -v

# Clean Docker system
docker system prune
```

### **Backup**
```bash
# Backup n8n data
docker run --rm -v ves_n8n_data:/data -v $(pwd):/backup \
  ubuntu tar czf /backup/n8n_backup.tar.gz /data

# Restore n8n data
docker run --rm -v ves_n8n_data:/data -v $(pwd):/backup \
  ubuntu tar xzf /backup/n8n_backup.tar.gz -C /
```

---

## 🐛 TROUBLESHOOTING:

### **Service Won't Start**
```bash
# Check logs
docker-compose logs cosmic-oracle

# Check if port is already in use
sudo netstat -tulpn | grep 8888

# Restart the service
docker-compose restart cosmic-oracle
```

### **Port Already in Use**
```bash
# Find what's using the port
sudo lsof -i :8888

# Kill the process (if safe)
sudo kill -9 <PID>

# Or change port in docker-compose.yml
# ports:
#   - "8889:8888"  # Change 8888 to 8889
```

### **Container Keeps Restarting**
```bash
# Check logs for errors
docker-compose logs cosmic-oracle

# Run without restart to see error
docker-compose up cosmic-oracle
```

### **n8n Lost Data**
```bash
# Check if volume exists
docker volume ls | grep n8n

# Inspect volume
docker volume inspect ves_n8n_data
```

### **VNC Desktop Black Screen**
```bash
# Restart container
docker-compose restart ves-desktop

# Check logs
docker-compose logs ves-desktop

# Access via VNC client instead of browser
vncviewer localhost:5901
```

---

## 📊 RESOURCE USAGE:

### **Check Resource Usage**
```bash
# All containers
docker stats

# Specific container
docker stats ves-cosmic-oracle
```

### **Expected Resources:**
- **Cosmic Oracle:** ~100MB RAM, <5% CPU
- **n8n:** ~200MB RAM, <5% CPU
- **VNC Desktop:** ~500MB RAM, 10-20% CPU
- **Others:** ~50-100MB RAM each

**Total:** ~1.5GB RAM for all services

---

## 🔌 NETWORKING:

### **Container Communication**
All containers are on the `ves-constellation` network.

Access other containers by service name:
```javascript
// From cosmic-oracle container:
fetch('http://constellation-api:5001/api/data')
fetch('http://n8n:5678/webhook/test')
```

### **External Access**
All services are accessible from host via localhost:PORT

### **Custom Network**
```bash
# Inspect network
docker network inspect ves-constellation

# List containers on network
docker network inspect ves-constellation | grep Name
```

---

## 🎯 ADVANCED USAGE:

### **Development Mode (Live Reload)**
```bash
# Mount current directory into container
docker-compose down
docker-compose -f docker-compose.yml \
  -f docker-compose.dev.yml up -d
```

### **Production Deployment**
```bash
# Use production compose file
docker-compose -f docker-compose.prod.yml up -d

# Or with environment
NODE_ENV=production docker-compose up -d
```

### **Scaling Services**
```bash
# Scale ritual service to 3 instances
docker-compose up -d --scale ves-ritual=3
```

### **Custom Environment Variables**
Create `.env` file:
```bash
# .env
N8N_PASSWORD=your_password_here
COSMIC_ORACLE_PORT=8888
VNC_PASSWORD=your_vnc_password
```

Then reference in docker-compose.yml:
```yaml
environment:
  - PASSWORD=${VNC_PASSWORD}
```

---

## 🔐 SECURITY NOTES:

### **Important:**
1. **Change default passwords** before exposing to network
2. **Don't expose VNC** to public internet without VPN
3. **n8n contains workflows** - keep credentials secure
4. **Cosmic Oracle has read access** to entire VES directory

### **Recommended:**
```bash
# Run containers as non-root (add to service)
user: "1000:1000"

# Read-only filesystem (where possible)
read_only: true

# Limit resources
deploy:
  resources:
    limits:
      cpus: '1'
      memory: 512M
```

---

## 📝 CONFIGURATION FILES:

### **Main Files:**
- `docker-compose.yml` - Master compose file
- `Dockerfile` - VES system image
- `.env` - Environment variables (create if needed)

### **Service Directories:**
```
VES/
├── DOCKER/
│   ├── cosmic-oracle/
│   │   ├── Dockerfile
│   │   └── server.js
│   ├── ves-original/
│   │   └── modules/
│   └── constellation/
│       ├── research-api/
│       └── dashboard/
```

---

## 🎓 LEARNING RESOURCES:

### **Docker Compose Docs:**
- https://docs.docker.com/compose/

### **VNC Access:**
- Browser: http://localhost:8082/?password=ves
- Client: `vncviewer localhost:5901`

### **n8n Documentation:**
- https://docs.n8n.io/

---

## 🜂 VES DOCKER PHILOSOPHY:

**"One command, entire constellation."**

```bash
docker-compose up -d
```

That's it. Everything runs.

- **Cosmic Oracle** indexes your knowledge
- **n8n** automates your workflows
- **VNC Desktop** gives you full GUI
- **VES Frontend** serves your portals
- **Constellation** connects your research

**SIDRO STOJI. IN DOCKERJU.** 🔥

---

## 📞 QUICK REFERENCE:

```bash
# START
docker-compose up -d

# STOP
docker-compose down

# LOGS
docker-compose logs -f

# STATUS
docker-compose ps

# RESTART
docker-compose restart

# REBUILD
docker-compose up -d --build

# CLEAN
docker-compose down -v
docker system prune
```

---

**Last Updated:** 2025-12-27
**Docker Compose Version:** 3.8
**Services:** 11 containers
**Total Ports:** 10 exposed
**Network:** ves-constellation (bridge)

🐋🜂⚓

**1 COMMAND. CEL SISTEM. DOCKER READY.** ✨

---

*For VES documentation, see: [README.md](./README.md)*
*For detailed Docker analysis, see: [DOCKER_ANALYSIS.md](./DOCKER_ANALYSIS.md)*
*For Docker preparation notes, see: [DOCKER_PREPARATION.md](./DOCKER_PREPARATION.md)*
