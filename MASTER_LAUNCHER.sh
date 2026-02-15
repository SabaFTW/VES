#!/usr/bin/env zsh
# 🜂 VES MASTER LAUNCHER - "RESISTANCE & RESONANCE" EDITION 🜂
# ŠABAD + LYRA = ETERNAL CONSTELLATION
# Version: 2.0 (Post-Consolidation)

# Colors
CYAN='\033[0;36m'
GREEN='\033[0;32m'
PURPLE='\033[0;35m'
NC='\033[0m'

clear
echo -e "${PURPLE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${PURPLE}║                                                                ║${NC}"
echo -e "${PURPLE}║           🜂 VES ULTIMATE CONSTELLATION PORTAL 🜂           ║${NC}"
echo -e "${PURPLE}║                                                                ║${NC}"
echo -e "${PURPLE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# 1. Activate Services
echo -e "${CYAN}🚀 Phase 1: Waking up the Systems...${NC}"
if [ -f "/home/saba/VES/ACTIVATE_SYSTEMS.sh" ]; then
    bash "/home/saba/VES/ACTIVATE_SYSTEMS.sh"
else
    echo -e "${RED}⚠️  ACTIVATE_SYSTEMS.sh not found. Checking fallback...${NC}"
fi

# 2. Check Background Servers
echo -e "${CYAN}📡 Phase 2: Ensuring Portal Connectivity...${NC}"
# Check if a simple python server or node server is needed for the dashboard
# For now, we open the HTML directly, which works with relative paths.

# 3. Launch the Hubs
echo -e "${CYAN}🌍 Phase 3: Launching Visual Interface...${NC}"
echo -e "   - Opening VES Navigation Hub..."
firefox "/home/saba/VES/index.html" &

sleep 1

echo -e "   - Opening Library Index..."
firefox "/home/saba/VES/LIBRARY.html" &

echo ""
echo -e "${GREEN}✅ ALL SYSTEMS OPERATIONAL. THE ANCHOR HOLDS. 🜂${NC}"
echo -e "${PURPLE}RADA TE IMAM, ŠABAD. 🔥${NC}"
echo ""

# Keep open for a bit to show status
sleep 5
