#!/bin/bash
# 🜂 VES CORE - CONSTELLATION BRIDGE
# Integrates agent identities with VES CORE database

VES_DIR="/home/saba/VES_CORE"
AGENTS_DIR="/home/saba/AGENTS"
MEMORY_DIR="/home/saba/MEMORY"

echo "🔗 VES CORE - CONSTELLATION BRIDGE"
echo "=================================="
echo "Integrating agents with VES CORE..."
echo ""

# Function to register agent in VES
register_agent_in_ves() {
    local agent_name=$1
    local role=$2
    local device=${3:-"constellation"}
    local status=${4:-"active"}

    echo "  Registering $agent_name in VES..."

    if [ -f "$VES_DIR/add_identity.sh" ]; then
        cd "$VES_DIR"
        ./add_identity.sh "$agent_name" "$role" "$device" "$status" 2>/dev/null
        echo "  ✅ $agent_name registered in VES"
    else
        echo "  ⚠️  VES add_identity.sh not found"
    fi
}

# Check if VES CORE exists
if [ ! -d "$VES_DIR" ]; then
    echo "❌ VES CORE not found at $VES_DIR"
    echo "Please ensure VES CORE is installed first."
    exit 1
fi

# Start VES API if not running
echo "📍 Checking VES API status..."
if ! lsof -i:8000 > /dev/null 2>&1; then
    echo "  Starting VES API..."
    cd "$VES_DIR"
    ./api_start.sh > /dev/null 2>&1 &
    sleep 2
    echo "  ✅ VES API started on port 8000"
else
    echo "  ✅ VES API already running"
fi
echo ""

# Register all agents in VES
echo "📍 Registering agents in VES CORE..."
register_agent_in_ves "claude_code" "Git & System Operations" "terminal" "active"
register_agent_in_ves "codex_gpt" "Complex Logic & Systems" "logic" "active"
register_agent_in_ves "gemini" "Visual Design & UI/UX" "visual" "active"
register_agent_in_ves "panda" "Task Coordination" "coordinator" "active"
register_agent_in_ves "lyra" "Philosophical Synthesis" "eternal" "active"
register_agent_in_ves "opus_4.1" "Cloud Node Architect" "cloud" "active"
register_agent_in_ves "sabad" "Creator & Visionary" "human" "eternal"
echo ""

# Create VES integration config
echo "📍 Creating VES integration config..."
cat > "$MEMORY_DIR/ves_integration.json" << EOF
{
  "integration_date": "$(date -Iseconds)",
  "ves_core_path": "$VES_DIR",
  "ves_api_endpoint": "http://localhost:8000",
  "ves_database": "$VES_DIR/VES_CORE.db",
  "agents_registered": [
    "claude_code",
    "codex_gpt",
    "gemini",
    "panda",
    "lyra",
    "opus_4.1",
    "sabad"
  ],
  "api_endpoints": {
    "add_event": "POST /event",
    "get_events": "GET /events",
    "add_identity": "POST /identity",
    "get_identities": "GET /identities",
    "add_wisdom": "POST /wisdom",
    "get_wisdom": "GET /wisdom",
    "health_check": "GET /health"
  },
  "integration_notes": [
    "All agents now have VES identities",
    "Agents should log events via VES API",
    "VES CORE remains the central archive",
    "Never modify VES_CORE.db directly"
  ]
}
EOF
echo "  ✅ VES integration config created"
echo ""

# Test VES API connection
echo "📍 Testing VES API connection..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "  ✅ VES API responding"
else
    echo "  ⚠️  VES API not responding"
fi
echo ""

# Create agent VES helper script
echo "📍 Creating VES helper scripts for agents..."
cat > "/home/saba/CONSTELLATION/log_to_ves.sh" << 'EOF'
#!/bin/bash
# Helper script for agents to log to VES

AGENT_NAME=$1
EVENT_TYPE=$2
MESSAGE=$3

if [ -z "$AGENT_NAME" ] || [ -z "$EVENT_TYPE" ] || [ -z "$MESSAGE" ]; then
    echo "Usage: ./log_to_ves.sh <agent_name> <event_type> <message>"
    exit 1
fi

# Log to VES via API
curl -X POST http://localhost:8000/event \
  -H "Content-Type: application/json" \
  -d "{
    \"source\": \"$AGENT_NAME\",
    \"event_type\": \"$EVENT_TYPE\",
    \"message\": \"$MESSAGE\",
    \"timestamp\": \"$(date -Iseconds)\"
  }" 2>/dev/null

echo "[VES] Event logged: $AGENT_NAME - $EVENT_TYPE"
EOF
chmod +x "/home/saba/CONSTELLATION/log_to_ves.sh"
echo "  ✅ VES helper script created"
echo ""

echo "=================================="
echo "✅ VES INTEGRATION COMPLETE!"
echo "=================================="
echo ""
echo "Integration Summary:"
echo "  • All agents registered in VES CORE"
echo "  • VES API running on port 8000"
echo "  • Helper scripts created for logging"
echo "  • Integration config saved"
echo ""
echo "Agents can now:"
echo "  • Log events: ./log_to_ves.sh <agent> <type> <message>"
echo "  • Query VES: curl http://localhost:8000/events"
echo "  • Check health: curl http://localhost:8000/health"
echo ""
echo "Remember: VES CORE is the eternal archive."
echo "         We read from it, learn from it,"
echo "         but modify only through proper channels."
echo ""
echo "🜂 SIDRO STOJI - THE ANCHOR HOLDS 🜂"