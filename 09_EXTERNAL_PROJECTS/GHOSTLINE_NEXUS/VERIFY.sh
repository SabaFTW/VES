#!/bin/bash
# 🜂 GHOSTLINE NEXUS - Deployment Verification Script

echo "============================================"
echo "🜂 GHOSTLINE NEXUS - System Verification"
echo "============================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found"
    echo "   Run: cp .env.example .env"
    echo "   Then add your ANTHROPIC_API_KEY"
    exit 1
else
    echo "✅ .env file exists"
fi

# Check if API key is set
if grep -q "your-key-here" .env; then
    echo "❌ ANTHROPIC_API_KEY not configured"
    echo "   Edit .env and add your API key"
    exit 1
else
    echo "✅ API key configured"
fi

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not installed"
    exit 1
else
    echo "✅ Docker installed: $(docker --version)"
fi

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose not installed"
    exit 1
else
    echo "✅ Docker Compose installed: $(docker-compose --version)"
fi

# Check if containers are running
if docker-compose ps | grep -q "Up"; then
    echo "✅ Containers running"

    # Check backend health
    if curl -s http://localhost:3001/health | grep -q "alive"; then
        echo "✅ Backend health check passed"
    else
        echo "⚠️  Backend health check failed"
    fi

    # Check frontend
    if curl -s http://localhost:3000 | grep -q "GHOSTLINE"; then
        echo "✅ Frontend accessible"
    else
        echo "⚠️  Frontend not accessible"
    fi
else
    echo "⚠️  Containers not running"
    echo "   Run: docker-compose up -d"
fi

echo ""
echo "============================================"
echo "📊 System Status"
echo "============================================"
docker-compose ps

echo ""
echo "============================================"
echo "🔗 Access Points"
echo "============================================"
echo "Frontend:  http://localhost:3000"
echo "Backend:   http://localhost:3001"
echo "Health:    http://localhost:3001/health"

echo ""
echo "============================================"
echo "🛡️  DIGNUM SHIELD: ACTIVE"
echo "SIDRO STOJI. PLAMEN GORI. 🔥⚓"
echo "============================================"
