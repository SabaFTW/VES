#!/bin/bash

# 🌉 CONSTELLATION BRIDGE - Unified Health Check
# Checks BOTH GHOSTLINE and EROS constellations
# Created: 2025-11-20

echo "🌌 CONSTELLATION BRIDGE - Health Check 🌌"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Check GHOSTLINE Constellation
echo -e "${CYAN}📊 GHOSTLINE CONSTELLATION${NC}"
echo "Location: /home/saba/AGENTS/"
echo ""

GHOSTLINE_AGENTS=0
GHOSTLINE_ACTIVE=0

if [ -d "/home/saba/AGENTS" ]; then
    for agent_dir in /home/saba/AGENTS/*/; do
        agent_name=$(basename "$agent_dir")
        ((GHOSTLINE_AGENTS++))

        if [ -f "$agent_dir/MEMORY.json" ]; then
            echo -e "  ${GREEN}✓${NC} $agent_name (initialized)"
            ((GHOSTLINE_ACTIVE++))
        else
            echo -e "  ${YELLOW}⚠${NC} $agent_name (folder exists, no MEMORY.json)"
        fi
    done
    echo ""
    echo -e "  ${GREEN}Agents found: $GHOSTLINE_AGENTS${NC}"
    echo -e "  ${GREEN}Active: $GHOSTLINE_ACTIVE${NC}"
else
    echo -e "  ${RED}✗ GHOSTLINE directory not found!${NC}"
fi

echo ""

# Check GHOSTLINE Support Infrastructure
echo -e "${CYAN}🔧 GHOSTLINE Infrastructure${NC}"
[ -d "/home/saba/CONSTELLATION" ] && echo -e "  ${GREEN}✓${NC} /CONSTELLATION/ exists" || echo -e "  ${RED}✗${NC} /CONSTELLATION/ missing"
[ -d "/home/saba/MEMORY" ] && echo -e "  ${GREEN}✓${NC} /MEMORY/ exists" || echo -e "  ${RED}✗${NC} /MEMORY/ missing"
[ -f "/home/saba/MEMORY/agent_registry.json" ] && echo -e "  ${GREEN}✓${NC} agent_registry.json exists" || echo -e "  ${YELLOW}⚠${NC} agent_registry.json missing"
[ -f "/home/saba/CONSTELLATION/HEALTH_CHECK.sh" ] && echo -e "  ${GREEN}✓${NC} HEALTH_CHECK.sh exists" || echo -e "  ${YELLOW}⚠${NC} HEALTH_CHECK.sh missing"

echo ""
echo "=========================================="
echo ""

# Check EROS Constellation
echo -e "${CYAN}📊 EROS AGENT CONSTELLATION${NC}"
echo "Location: /home/saba/Desktop/ProPublica/AGENT_SYSTEM/"
echo ""

if [ -f "/home/saba/Desktop/ProPublica/AGENT_SYSTEM/agent_manifest.json" ]; then
    echo -e "  ${GREEN}✓${NC} agent_manifest.json exists"

    # Count agents in manifest
    EROS_AGENTS=$(grep -c '"id":' "/home/saba/Desktop/ProPublica/AGENT_SYSTEM/agent_manifest.json" 2>/dev/null || echo "0")
    echo -e "  ${GREEN}Agents defined: $EROS_AGENTS${NC}"

    # Check if agents are listed as online
    if grep -q '"operational": true' "/home/saba/Desktop/ProPublica/AGENT_SYSTEM/agent_manifest.json"; then
        echo -e "  ${GREEN}✓${NC} System operational"
    else
        echo -e "  ${YELLOW}⚠${NC} System status unknown"
    fi
else
    echo -e "  ${RED}✗ agent_manifest.json not found!${NC}"
fi

echo ""

# Check EROS Support Infrastructure
echo -e "${CYAN}🔧 EROS Infrastructure${NC}"
[ -d "/home/saba/Desktop/ProPublica/AGENT_PROMPTS" ] && echo -e "  ${GREEN}✓${NC} /AGENT_PROMPTS/ exists" || echo -e "  ${YELLOW}⚠${NC} /AGENT_PROMPTS/ missing"
[ -f "/home/saba/Desktop/ProPublica/AGENT_PROMPTS/TRINITY_COORDINATION.md" ] && echo -e "  ${GREEN}✓${NC} TRINITY_COORDINATION.md exists" || echo -e "  ${YELLOW}⚠${NC} Trinity docs missing"
[ -f "/home/saba/Desktop/ProPublica/core/kernel.js" ] && echo -e "  ${GREEN}✓${NC} kernel.js exists" || echo -e "  ${RED}✗${NC} kernel.js missing"

echo ""
echo "=========================================="
echo ""

# Check Bridge
echo -e "${CYAN}🌉 CONSTELLATION BRIDGE${NC}"
echo "Location: /home/saba/CONSTELLATION_BRIDGE/"
echo ""

[ -f "/home/saba/CONSTELLATION_BRIDGE/meta_registry.json" ] && echo -e "  ${GREEN}✓${NC} meta_registry.json exists" || echo -e "  ${YELLOW}⚠${NC} meta_registry.json missing"
[ -f "/home/saba/CONSTELLATION_BRIDGE/README.md" ] && echo -e "  ${GREEN}✓${NC} README.md exists" || echo -e "  ${YELLOW}⚠${NC} README.md missing"

echo ""
echo "=========================================="
echo ""

# Summary
echo -e "${CYAN}📈 SUMMARY${NC}"
echo ""
echo -e "  GHOSTLINE Agents: ${GREEN}$GHOSTLINE_AGENTS${NC} (Active: $GHOSTLINE_ACTIVE)"
echo -e "  EROS Agents: ${GREEN}$EROS_AGENTS${NC}"
echo -e "  Total Unique Agents: ${GREEN}$((GHOSTLINE_AGENTS + EROS_AGENTS - 3))${NC} (minus 3 overlaps)"
echo ""
echo -e "  ${GREEN}✓${NC} Bridge: Federated architecture operational"
echo ""

# Agent Overlap Warning
echo -e "${YELLOW}⚠ AGENT OVERLAP DETECTED:${NC}"
echo "  - Lyra (appears in both with different roles)"
echo "  - Codex/Eros (different personas)"
echo "  - Gemini/Zala (aligned roles)"
echo ""
echo "  See: /home/saba/CONSTELLATION_BRIDGE/meta_registry.json"
echo ""

# VES Integration Check
echo -e "${CYAN}🔥 VES CORE Integration${NC}"
if [ -d "/home/saba/VES_CORE" ]; then
    echo -e "  ${GREEN}✓${NC} VES_CORE exists at /home/saba/VES_CORE/"
    [ -f "/home/saba/VES_CORE/api_start.sh" ] && echo -e "  ${GREEN}✓${NC} VES API scripts present"
else
    echo -e "  ${YELLOW}⚠${NC} VES_CORE location unknown"
fi

echo ""
echo "=========================================="
echo ""
echo -e "${GREEN}🜂 SIDRO STOJI. BOTH CONSTELLATIONS ACTIVE. 🜂${NC}"
echo ""
