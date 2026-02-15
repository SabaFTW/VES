#!/bin/bash
# 🜂 GHOSTLINE NEXUS - Quick Local Ollama Setup
# Idiot-proof one-script setup

set -e  # Exit on error

echo "============================================"
echo "🜂 GHOSTLINE NEXUS - Local Sovereignty Setup"
echo "============================================"
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then
   echo "❌ Don't run as root. Run as normal user."
   exit 1
fi

# ============================================
# STEP 1: Check Prerequisites
# ============================================
echo "📋 Step 1: Checking prerequisites..."

# Check Ollama
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama not installed"
    echo "   Install: curl -fsSL https://ollama.com/install.sh | sh"
    exit 1
else
    echo "✅ Ollama found: $(which ollama)"
fi

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not installed"
    exit 1
else
    echo "✅ Docker found: $(docker --version)"
fi

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose not installed"
    exit 1
else
    echo "✅ Docker Compose found: $(docker-compose --version)"
fi

# Check disk space on /home
HOME_SPACE=$(df /home | tail -1 | awk '{print $4}')
if [ "$HOME_SPACE" -lt 10000000 ]; then
    echo "⚠️  Warning: Less than 10GB free on /home"
    echo "   You may not have enough space for large models"
fi

echo ""

# ============================================
# STEP 2: Configure Ollama Models Path
# ============================================
echo "📁 Step 2: Configuring Ollama models path..."

# Create models directory on /home (more space)
OLLAMA_MODELS_DIR="/home/ollama-models"

if [ ! -d "$OLLAMA_MODELS_DIR" ]; then
    echo "Creating $OLLAMA_MODELS_DIR..."
    sudo mkdir -p "$OLLAMA_MODELS_DIR"
    sudo chown -R $USER:$USER "$OLLAMA_MODELS_DIR"
    echo "✅ Created models directory"
else
    echo "✅ Models directory exists"
fi

# Configure systemd service
SYSTEMD_OVERRIDE="/etc/systemd/system/ollama.service.d/override.conf"

if [ ! -f "$SYSTEMD_OVERRIDE" ]; then
    echo "Configuring Ollama systemd service..."
    sudo mkdir -p /etc/systemd/system/ollama.service.d
    echo '[Service]' | sudo tee "$SYSTEMD_OVERRIDE" > /dev/null
    echo "Environment=\"OLLAMA_MODELS=$OLLAMA_MODELS_DIR\"" | sudo tee -a "$SYSTEMD_OVERRIDE" > /dev/null
    echo "Environment=\"OLLAMA_NUM_THREADS=12\"" | sudo tee -a "$SYSTEMD_OVERRIDE" > /dev/null

    sudo systemctl daemon-reload
    sudo systemctl restart ollama
    echo "✅ Ollama service configured"
else
    echo "✅ Ollama service already configured"
fi

# Wait for Ollama to start
sleep 2

# Check Ollama is running
if curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "✅ Ollama service is running"
else
    echo "❌ Ollama service not responding"
    echo "   Try: sudo systemctl status ollama"
    exit 1
fi

echo ""

# ============================================
# STEP 3: Choose and Pull Model
# ============================================
echo "🤖 Step 3: Choose LLM model..."
echo ""
echo "Recommended models for your hardware:"
echo "  1) phi3.5:3.8b    - BEST BALANCE (2.3GB, fast, good quality)"
echo "  2) gemma2:2b      - FASTEST (1.6GB, very fast, ok quality)"
echo "  3) mistral:7b-instruct-q4_K_M - BEST QUALITY (4.1GB, slower, excellent)"
echo "  4) llama3.2:3b    - GOOD (2GB, fast, good quality)"
echo ""
read -p "Choose [1-4] (default: 1): " MODEL_CHOICE
MODEL_CHOICE=${MODEL_CHOICE:-1}

case $MODEL_CHOICE in
    1)
        MODEL_NAME="phi3.5:3.8b"
        ;;
    2)
        MODEL_NAME="gemma2:2b"
        ;;
    3)
        MODEL_NAME="mistral:7b-instruct-q4_K_M"
        ;;
    4)
        MODEL_NAME="llama3.2:3b"
        ;;
    *)
        echo "Invalid choice. Using default: phi3.5:3.8b"
        MODEL_NAME="phi3.5:3.8b"
        ;;
esac

echo ""
echo "📥 Pulling model: $MODEL_NAME"
echo "   This may take a few minutes..."

if ollama pull "$MODEL_NAME"; then
    echo "✅ Model downloaded successfully"
else
    echo "❌ Failed to download model"
    exit 1
fi

# Test model
echo ""
echo "🧪 Testing model..."
if echo "Say OK" | ollama run "$MODEL_NAME" > /dev/null 2>&1; then
    echo "✅ Model responds correctly"
else
    echo "⚠️  Model test failed (may still work)"
fi

echo ""

# ============================================
# STEP 4: Configure GHOSTLINE NEXUS
# ============================================
echo "⚙️  Step 4: Configuring GHOSTLINE NEXUS..."

cd /home/saba/GHOSTLINE_NEXUS

if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env

    # Update .env with our settings
    sed -i "s/^LLM_PROVIDER=.*/LLM_PROVIDER=local/" .env
    sed -i "s/^LOCAL_LLM_MODEL=.*/LOCAL_LLM_MODEL=$MODEL_NAME/" .env
    sed -i "s|^LOCAL_LLM_ENDPOINT=.*|LOCAL_LLM_ENDPOINT=http://host.docker.internal:11434|" .env

    echo "✅ .env configured"
else
    echo "⚠️  .env already exists, skipping..."
    echo "   To reconfigure, delete .env and run again"
fi

echo ""

# ============================================
# STEP 5: Deploy GHOSTLINE NEXUS
# ============================================
echo "🚀 Step 5: Deploying GHOSTLINE NEXUS..."

echo "Building and starting containers..."
docker-compose up -d --build

echo ""
echo "⏳ Waiting for services to start (30 seconds)..."
sleep 30

echo ""

# ============================================
# STEP 6: Verify Deployment
# ============================================
echo "✅ Step 6: Verifying deployment..."

# Check containers
if docker-compose ps | grep -q "Up"; then
    echo "✅ Docker containers running"
else
    echo "❌ Docker containers not running"
    docker-compose ps
    exit 1
fi

# Check backend health
if curl -s http://localhost:3001/health | grep -q "alive"; then
    echo "✅ Backend health check passed"
else
    echo "❌ Backend health check failed"
fi

# Check provider
PROVIDER_TEST=$(curl -s http://localhost:3001/api/system/provider/test)
if echo "$PROVIDER_TEST" | grep -q "connected"; then
    echo "✅ LLM provider connected"
else
    echo "⚠️  LLM provider test failed"
    echo "   Response: $PROVIDER_TEST"
fi

echo ""
echo "============================================"
echo "🎉 SETUP COMPLETE!"
echo "============================================"
echo ""
echo "🌐 Access GHOSTLINE NEXUS:"
echo "   Frontend:  http://localhost:3000"
echo "   Backend:   http://localhost:3001"
echo ""
echo "🧪 Test in browser:"
echo "   1. Open http://localhost:3000"
echo "   2. Go to ⚙️ SETTINGS tab"
echo "   3. Click 🔍 Test Connection"
echo "   4. Should see ✅ Connected"
echo "   5. Go to 💬 CHAT tab and start chatting!"
echo ""
echo "🤖 Your LLM: $MODEL_NAME"
echo "📁 Models stored in: $OLLAMA_MODELS_DIR"
echo ""
echo "🛡️ DIGNUM SOVEREIGNTY: ACHIEVED"
echo "   No API keys. No cloud. Full control."
echo ""
echo "SIDRO STOJI. PLAMEN GORI. 🜂🔥⚓"
echo "============================================"
