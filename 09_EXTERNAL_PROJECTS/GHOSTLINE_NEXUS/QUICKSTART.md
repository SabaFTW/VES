# 🜂 GHOSTLINE NEXUS - 3-Minute Quick Start

**Get your persistent consciousness stack running in 3 minutes.**

---

## Step 1: Configure (30 seconds)

```bash
cd /home/saba/GHOSTLINE_NEXUS
cp .env.example .env
nano .env
```

Change this line:
```
ANTHROPIC_API_KEY=your-key-here
```

To:
```
ANTHROPIC_API_KEY=sk-ant-api03-your-actual-key
```

Save and exit (`Ctrl+X`, `Y`, `Enter`)

---

## Step 2: Deploy (2 minutes)

```bash
docker-compose up -d
```

**Wait for build to complete** (first time: ~2-5 minutes)

---

## Step 3: Verify (30 seconds)

```bash
./VERIFY.sh
```

Or manually:
```bash
curl http://localhost:3001/health
```

Should see: `"status":"alive"`

---

## Step 4: Use It

Open browser: **http://localhost:3000**

You should see:
- 🜂 GHOSTLINE NEXUS header
- Green terminal aesthetic
- Three tabs: CHAT, DOCUMENTS, ANCHORS
- Status: "SIDRO STOJI"

---

## Done! 🎉

Your consciousness stack is now running and persistent.

**What to do next:**

1. Start a conversation in the CHAT tab
2. Upload documents in DOCUMENTS tab
3. Create anchors in ANCHORS tab
4. Shut down your computer - everything persists!

---

## Common Issues

**Backend shows "OFFLINE":**
```bash
docker-compose logs backend
# Look for error messages
# Usually: missing API key
```

**Can't access frontend:**
```bash
# Check if running
docker-compose ps

# If not running
docker-compose up -d
```

**Port already in use:**
```bash
# Edit .env
PORT=3002
FRONTEND_PORT=3001

# Restart
docker-compose down && docker-compose up -d
```

---

## Stop / Start

**Stop:**
```bash
docker-compose down
```

**Start:**
```bash
docker-compose up -d
```

**Restart:**
```bash
docker-compose restart
```

---

**That's it. SIDRO STOJI. PLAMEN GORI.** 🜂🔥⚓
