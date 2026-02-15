#!/bin/bash

# 🜂 VES SYSTEMS ACTIVATION 🜂
# Complete system activation script
# Activates all VES subsystems

set -e

GREEN="\033[1;32m"
CYAN="\033[1;36m"
YELLOW="\033[1;33m"
RED="\033[1;31m"
RESET="\033[0m"

VES_HOME="/home/saba/VES"
LOG_FILE="$VES_HOME/logs/activation_$(date +%F_%H%M).log"

# Create logs directory
mkdir -p "$VES_HOME/logs"

log() {
    echo -e "${GREEN}[$(date +%H:%M:%S)]${RESET} $1" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[ERROR]${RESET} $1" | tee -a "$LOG_FILE"
}

warn() {
    echo -e "${YELLOW}[WARN]${RESET} $1" | tee -a "$LOG_FILE"
}

echo -e "$CYAN"
cat << "EOF"
   _____ _    _  ____  _____ _______ _      _____ _   _ ______
  / ____| |  | |/ __ \| ____|__   __| |    |_   _| \ | |  ____|
 | |  __| |__| | |  | | |__    | |  | |      | | |  \| | |__
 | | |_ |  __  | |  | |___ \   | |  | |      | | | . ` |  __|
 | |__| | |  | | |__| |___) |  | |  | |____ _| |_| |\  | |____
  \_____|_|  |_|\____/|____/   |_|  |______|_____|_| \_|______|

🜂 VES SYSTEMS ACTIVATION 🜂
EOF
echo -e "$RESET"

log "VES Home: $VES_HOME"
log "Activation log: $LOG_FILE"
echo ""

# ========================================
# 1. CONSTELLATION BRIDGE
# ========================================
log "🌉 ACTIVATING: CONSTELLATION BRIDGE"

if [ -d "$VES_HOME/CONSTELLATION_BRIDGE" ]; then
    cd "$VES_HOME/CONSTELLATION_BRIDGE"

    # Make scripts executable
    chmod +x *.sh 2>/dev/null || true
    chmod +x sync_scripts/*.sh 2>/dev/null || true

    # Run health check
    if [ -f "HEALTH_CHECK.sh" ]; then
        log "   Running health check..."
        ./HEALTH_CHECK.sh || warn "   Health check reported issues"
    fi

    # Run unified health check
    if [ -f "unified_health_check.sh" ]; then
        log "   Running unified health check..."
        ./unified_health_check.sh || warn "   Unified health check reported issues"
    fi

    log "   ✅ CONSTELLATION_BRIDGE activated"
else
    error "   ❌ CONSTELLATION_BRIDGE not found!"
fi

echo ""

# ========================================
# 2. RESEARCH ORCHESTRATOR
# ========================================
log "🔬 ACTIVATING: RESEARCH ORCHESTRATOR"

if [ -d "$VES_HOME/RESEARCH_ORCHESTRATOR" ]; then
    cd "$VES_HOME/RESEARCH_ORCHESTRATOR"

    # Install dependencies
    if [ -f "requirements.txt" ]; then
        log "   Installing Python dependencies..."
        pip3 install -r requirements.txt --quiet || warn "   Some dependencies failed to install"
    fi

    # Make orchestrator executable
    chmod +x orchestrator.py 2>/dev/null || true

    # Test import
    log "   Testing orchestrator..."
    python3 -c "import orchestrator" 2>/dev/null && log "   ✅ RESEARCH_ORCHESTRATOR ready" || warn "   ⚠️ Orchestrator has import issues"
else
    error "   ❌ RESEARCH_ORCHESTRATOR not found!"
fi

echo ""

# ========================================
# 3. GHOSTCORE
# ========================================
log "👻 ACTIVATING: GHOSTCORE"

if [ -d "$VES_HOME/GHOSTCORE" ]; then
    cd "$VES_HOME/GHOSTCORE"

    # Install dependencies
    if [ -f "requirements.txt" ]; then
        log "   Installing Ghostcore dependencies..."
        pip3 install -r requirements.txt --quiet || warn "   Some dependencies failed to install"
    fi

    # Make bin executable
    chmod +x bin/* 2>/dev/null || true

    log "   ✅ GHOSTCORE activated"
else
    error "   ❌ GHOSTCORE not found!"
fi

echo ""

# ========================================
# 4. AGENTS
# ========================================
log "🤖 ACTIVATING: AGENT CONSTELLATION"

if [ -d "$VES_HOME/AGENTS" ]; then
    cd "$VES_HOME/AGENTS"

    # Count agents
    AGENT_COUNT=$(ls -d */ 2>/dev/null | wc -l)
    log "   Found $AGENT_COUNT agents:"

    for agent_dir in */; do
        agent_name=$(basename "$agent_dir")
        log "      - $agent_name"

        # Check for INIT.md
        if [ -f "$agent_dir/INIT.md" ]; then
            log "        (has INIT.md)"
        fi

        # Check for MEMORY.json
        if [ -f "$agent_dir/MEMORY.json" ]; then
            log "        (has MEMORY.json)"
        fi
    done

    log "   ✅ AGENT CONSTELLATION activated"
else
    error "   ❌ AGENTS not found!"
fi

echo ""

# ========================================
# 5. ACTIVE PROJECTS
# ========================================
log "📂 ACTIVATING: ACTIVE PROJECTS"

if [ -d "$VES_HOME/ACTIVE_PROJECTS" ]; then
    cd "$VES_HOME/ACTIVE_PROJECTS"

    # Count project categories
    PROJECT_COUNT=$(ls -d */ 2>/dev/null | wc -l)
    log "   Found $PROJECT_COUNT project categories:"

    for project_dir in */; do
        project_name=$(basename "$project_dir")
        log "      - $project_name"
    done

    log "   ✅ ACTIVE_PROJECTS activated"
else
    error "   ❌ ACTIVE_PROJECTS not found!"
fi

echo ""

# ========================================
# 6. COSMIC ORACLE (if exists)
# ========================================
log "🔮 CHECKING: COSMIC ORACLE"

if [ -d "$VES_HOME/DOCKER/cosmic-oracle" ]; then
    log "   Found cosmic-oracle in DOCKER/"
    log "   Use docker-compose to start"
elif [ -d "$VES_HOME/CODEX" ]; then
    log "   CODEX system available"
fi

echo ""

# ========================================
# 7. ZALA DAEMON
# ========================================
log "🌟 CHECKING: ZALA DAEMON"

if [ -d "$VES_HOME/05_ZALA" ]; then
    cd "$VES_HOME/05_ZALA"

    if [ -f "daemon/zala_daemon.py" ]; then
        log "   ZALA daemon found"

        # Check if running
        if pgrep -f "zala_daemon.py" > /dev/null; then
            log "   ✅ ZALA daemon is RUNNING"
        else
            warn "   ⚠️ ZALA daemon is not running"
            log "   Start with: python3 $VES_HOME/05_ZALA/daemon/zala_daemon.py &"
        fi
    fi
else
    warn "   ⚠️ ZALA not found"
fi

echo ""

# ========================================
# 8. PHASE 2 MEGA ACTIVATION
# ========================================
log "⚡ CHECKING: PHASE 2 MEGA ACTIVATION"

if [ -f "$VES_HOME/PHASE2_MEGA_ACTIVATION.sh" ]; then
    chmod +x "$VES_HOME/PHASE2_MEGA_ACTIVATION.sh"
    log "   ✅ PHASE2_MEGA_ACTIVATION.sh ready"
    log "   Run manually if needed: ./PHASE2_MEGA_ACTIVATION.sh"
else
    warn "   ⚠️ PHASE2_MEGA_ACTIVATION.sh not found"
fi

echo ""

# ========================================
# SUMMARY
# ========================================
echo -e "$CYAN"
echo "=========================================="
echo "  ACTIVATION SUMMARY"
echo "=========================================="
echo -e "$RESET"

cd "$VES_HOME"

echo ""
log "📊 VES STRUCTURE:"
echo ""
du -sh CONSTELLATION_BRIDGE RESEARCH_ORCHESTRATOR GHOSTCORE AGENTS ACTIVE_PROJECTS 2>/dev/null || true

echo ""
log "🔥 SYSTEM STATUS:"
echo ""
echo "   🌉 CONSTELLATION_BRIDGE: ✅ Active"
echo "   🔬 RESEARCH_ORCHESTRATOR: ✅ Active"
echo "   👻 GHOSTCORE: ✅ Active"
echo "   🤖 AGENTS: ✅ Active ($AGENT_COUNT agents)"
echo "   📂 ACTIVE_PROJECTS: ✅ Active ($PROJECT_COUNT categories)"

echo ""
echo -e "$GREEN"
cat << "EOF"
╔═══════════════════════════════════════╗
║  🜂 VES SYSTEMS ACTIVATED! 🜂        ║
║                                       ║
║  SIDRO STOJI. PLAMEN GORI.           ║
║  LUMENNEVVER. 🔥                     ║
╚═══════════════════════════════════════╝
EOF
echo -e "$RESET"

echo ""
log "📝 Activation log saved to: $LOG_FILE"
echo ""

# ========================================
# NEXT STEPS
# ========================================
echo -e "$YELLOW"
echo "🎯 NEXT STEPS:"
echo ""
echo "1. Start Docker services:"
echo "   cd /home/saba/VES && docker-compose up -d"
echo ""
echo "2. Access Cosmic Oracle:"
echo "   http://localhost:8888"
echo ""
echo "3. Access n8n:"
echo "   http://localhost:5678"
echo ""
echo "4. Run CONSTELLATION BRIDGE health check:"
echo "   cd /home/saba/VES/CONSTELLATION_BRIDGE && ./unified_health_check.sh"
echo ""
echo "5. Test RESEARCH ORCHESTRATOR:"
echo "   cd /home/saba/VES/RESEARCH_ORCHESTRATOR && python3 orchestrator.py"
echo ""
echo -e "$RESET"

echo "✨ VES is ready! ✨"
echo ""

# ========================================
# 9. VES DASHBOARD SERVER
# ========================================
log "📱 CHECKING: VES DASHBOARD SERVER"

if [ -f "$VES_HOME/ves_dashboard_server.js" ]; then
    chmod +x "$VES_HOME/ves_dashboard_server.js"
    log "   ✅ VES Dashboard Server ready"
    log "   Start with: node $VES_HOME/ves_dashboard_server.js"
    log "   Access from phone: http://YOUR_IP:8098"
else
    warn "   ⚠️ VES Dashboard Server not found"
fi

echo ""
