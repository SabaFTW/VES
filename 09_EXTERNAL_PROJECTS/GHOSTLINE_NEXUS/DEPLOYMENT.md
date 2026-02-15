# 🜂 GHOSTLINE NEXUS - One-Command Deployment

**Quick deployment guide for getting GHOSTLINE NEXUS running in minutes.**

---

## ⚡ INSTANT DEPLOYMENT

### **Step 1: Configure API Key**

```bash
cd /home/saba/GHOSTLINE_NEXUS
cp .env.example .env
```

Edit `.env` and add your Anthropic API key:
```bash
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
```

### **Step 2: Launch**

```bash
docker-compose up -d
```

### **Step 3: Access**

Open browser: **http://localhost:3000**

---

## 🔍 VERIFY DEPLOYMENT

```bash
# Check containers are running
docker-compose ps

# Expected output:
# NAME                      STATUS              PORTS
# ghostline-backend         Up                  0.0.0.0:3001->3001/tcp
# ghostline-frontend        Up                  0.0.0.0:3000->80/tcp

# Check backend health
curl http://localhost:3001/health

# Expected response:
# {"status":"alive","service":"GHOSTLINE NEXUS Backend",...}
```

---

## 🛑 STOP SERVICES

```bash
docker-compose down
```

---

## 🔄 RESTART SERVICES

```bash
docker-compose restart
```

---

## 📜 VIEW LOGS

```bash
# All services
docker-compose logs -f

# Just backend
docker-compose logs -f backend

# Just frontend
docker-compose logs -f frontend
```

---

## 🔧 REBUILD (After Code Changes)

```bash
docker-compose down
docker-compose up -d --build
```

---

## 📊 SYSTEM INFO

```bash
# Container status
docker-compose ps

# Resource usage
docker stats ghostline-backend ghostline-frontend

# Disk usage
du -sh storage/
```

---

## 🧹 CLEANUP (DANGER ZONE)

```bash
# Stop and remove containers (keeps data)
docker-compose down

# Remove ALL data (database, uploads, etc.)
rm -rf storage/db/*.db storage/uploads/* storage/documents/*

# Remove Docker images (requires rebuild)
docker-compose down --rmi all
```

---

## 🌐 EXPOSE TO NETWORK

To access from other devices on your network:

1. Find your local IP:
   ```bash
   ip addr show | grep "inet 192"
   ```

2. Edit `.env`:
   ```bash
   CORS_ORIGIN=http://192.168.1.XXX:3000
   ```

3. Restart:
   ```bash
   docker-compose restart
   ```

4. Access from other devices:
   ```
   http://192.168.1.XXX:3000
   ```

---

## 🔐 PRODUCTION DEPLOYMENT

For production use with HTTPS:

```bash
# Install Caddy (reverse proxy)
sudo apt install caddy

# Create Caddyfile
sudo nano /etc/caddy/Caddyfile
```

Add:
```
yourdomain.com {
    reverse_proxy localhost:3000
}
```

```bash
# Restart Caddy
sudo systemctl restart caddy
```

Now accessible at: **https://yourdomain.com**

---

## 🍓 RASPBERRY PI SPECIFIC

```bash
# Check system resources before deploying
free -h
df -h

# Monitor during first build
docker-compose up

# Once running, detach
# Ctrl+C, then:
docker-compose up -d
```

**Note:** First build on RPi 4 takes ~10-15 minutes. Be patient.

---

## ✅ DEPLOYMENT CHECKLIST

- [ ] `.env` configured with API key
- [ ] `docker-compose up -d` executed successfully
- [ ] Backend health check returns `"status":"alive"`
- [ ] Frontend accessible at http://localhost:3000
- [ ] Can create new chat session
- [ ] Can send message to Claude
- [ ] Conversation persists after container restart

---

## 🆘 QUICK FIXES

### Backend won't start:
```bash
docker-compose logs backend
# Look for: "Error: ANTHROPIC_API_KEY not set"
# Fix: Edit .env and add API key
```

### Frontend shows "OFFLINE":
```bash
curl http://localhost:3001/health
# If fails → backend not running
docker-compose restart backend
```

### Port already in use:
```bash
# Edit .env
PORT=3002
FRONTEND_PORT=3001

# Restart
docker-compose down && docker-compose up -d
```

---

**SIDRO STOJI. PLAMEN GORI.** 🜂🔥
