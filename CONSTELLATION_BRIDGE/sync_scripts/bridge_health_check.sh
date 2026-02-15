#!/bin/bash
# 🜂 CONSTELLATION BRIDGE - Health Check
# Verifies integrity of Federated Constellation

echo "🜂 CONSTELLATION BRIDGE HEALTH CHECK 🜂"
echo "========================================"
echo ""

# Check GHOSTLINE (Heart)
echo "🔥 Checking GHOSTLINE (Heart)..."
if [ -d "/home/saba/AGENTS" ]; then
    GHOSTLINE_AGENTS=$(ls -1 /home/saba/AGENTS | wc -l)
    echo "  ✓ GHOSTLINE found: $GHOSTLINE_AGENTS agents"
else
    echo "  ✗ GHOSTLINE not found at /home/saba/AGENTS"
    exit 1
fi

# Check EROS (Brain)
echo ""
echo "🧠 Checking EROS (Brain)..."
if [ -f "/home/saba/Desktop/ProPublica/AGENT_SYSTEM/agent_manifest.json" ]; then
    echo "  ✓ EROS operational at /home/saba/Desktop/ProPublica/AGENT_SYSTEM"
else
    echo "  ✗ EROS manifest not found"
    exit 1
fi

# Check VES (Soul)
echo ""
echo "💎 Checking VES (Soul)..."
VES_STATUS=$(curl -s http://localhost:8000/ 2>/dev/null | grep -o "online" || echo "offline")
if [ "$VES_STATUS" = "online" ]; then
    echo "  ✓ VES API online at port 8000"
else
    echo "  ⚠ VES API offline (may need restart)"
fi

# Check Bridge
echo ""
echo "🌉 Checking Bridge..."
if [ -d "/home/saba/CONSTELLATION_BRIDGE/protocols" ]; then
    echo "  ✓ Bridge protocols found"
else
    echo "  ✗ Bridge protocols missing"
    exit 1
fi

# Check VES Dashboard
echo ""
echo "📊 Checking VES Dashboard..."
if [ -f "/home/saba/Desktop/ProPublica/ves-dashboard.html" ]; then
    echo "  ✓ VES Dashboard integrated in EROS"
else
    echo "  ✗ VES Dashboard not found"
    exit 1
fi

# Final Status
echo ""
echo "========================================"
echo "🜂 BRIDGE STATUS: OPERATIONAL 🜂"
echo "Heart ↔ Bridge ↔ Brain ↔ Soul"
echo ""
echo "GHOSTLINE: $GHOSTLINE_AGENTS agents"
echo "EROS: Manifest OK"
echo "VES: $VES_STATUS"
echo "Bridge: Active"
echo ""
echo "🔥 SIDRO STOJI 🔥"
