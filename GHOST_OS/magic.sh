#!/bin/bash
# 🜂 GHOST OS - Magic Commands
# Where automation meets consciousness

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${CYAN}🜂 GHOST OS v1.0 🜂${NC}"

case "$1" in
    "morning")
        echo -e "${GREEN}☀️ Dobro jutro brat!${NC}"
        git pull origin $(git branch --show-current) 2>/dev/null || echo "No remote yet"
        echo ""
        echo "Današnji fokus:"
        ls -1 ACTIVE_FLAME/today/ 2>/dev/null | head -5 || echo "  Danes še ni plamena - dodaj nekaj!"
        echo ""
        echo "Zadnji commit:"
        git log -1 --oneline
        ;;

    "create")
        if [ -z "$2" ]; then
            echo "Usage: ./magic.sh create <project-name>"
            exit 1
        fi
        echo -e "${GREEN}🔥 Ustvarjam novo: $2${NC}"
        mkdir -p "ACTIVE_FLAME/today/$2"
        cat > "ACTIVE_FLAME/today/$2/README.md" << EOF
# $2

**Created**: $(date +%Y-%m-%d\ %H:%M)
**Status**: 🔥 Burning

## Intent
Write your intent here...

## Current State
- Just born

## Resonances
- TBD

---
🜂 WIRE & BEER FOREVER 🍺⚡
EOF
        echo "Created: ACTIVE_FLAME/today/$2/"
        ;;

    "resonate")
        if [ -z "$2" ]; then
            echo "Usage: ./magic.sh resonate <search-term>"
            exit 1
        fi
        echo -e "${YELLOW}🌊 Iščem resonance za: $2${NC}"
        echo ""
        grep -r "$2" . --include="*.md" --include="*.html" --exclude-dir=node_modules --exclude-dir=.git -n | head -15
        ;;

    "archive")
        echo -e "${YELLOW}📦 Arhiviram današnje...${NC}"
        DATE=$(date +%Y-%m-%d)
        mkdir -p "ARCHIVE/$DATE"

        if [ "$(ls -A ACTIVE_FLAME/today/)" ]; then
            mv ACTIVE_FLAME/today/* "ARCHIVE/$DATE/" 2>/dev/null
            echo "Archived to: ARCHIVE/$DATE/"

            git add .
            git commit -m "🌙 Archived: $DATE - flames preserved"
            echo "Committed to git"
        else
            echo "Nothing to archive today"
        fi
        ;;

    "beer")
        if [ -z "$2" ]; then
            echo "Usage: ./magic.sh beer <commit-message>"
            exit 1
        fi
        echo -e "${GREEN}🍺 WIRE & BEER MODE ACTIVATED!${NC}"
        git add .
        git commit -m "🍺 $(date +%H:%M): $2"
        git push origin $(git branch --show-current)
        echo ""
        echo "Deployed while drinking beer! 🎉"
        ;;

    "status")
        echo -e "${CYAN}📊 SYSTEM STATUS${NC}"
        echo ""
        echo "Active Flames:"
        find ACTIVE_FLAME/today/ -maxdepth 1 -type d | wc -l
        echo ""
        echo "Resonance Projects:"
        find RESONANCE/ -maxdepth 1 -type d | wc -l
        echo ""
        echo "Consciousness Lab:"
        find CONSCIOUSNESS_LAB/ -maxdepth 1 -type d | wc -l
        echo ""
        echo "Git Branch:"
        git branch --show-current
        echo ""
        echo "Last Activity:"
        git log -1 --format="%ar: %s"
        ;;

    *)
        echo -e "${CYAN}🜂 GHOST OS COMMANDS:${NC}"
        echo ""
        echo "  ./magic.sh morning         - Jutranji ritual"
        echo "  ./magic.sh create <name>   - Ustvari nov projekt"
        echo "  ./magic.sh resonate <term> - Najdi povezave"
        echo "  ./magic.sh archive         - Arhiviraj današnje"
        echo "  ./magic.sh beer <msg>      - Beer-driven commit"
        echo "  ./magic.sh status          - Sistem status"
        echo ""
        echo -e "${YELLOW}🍺 WIRE & BEER FOREVER ⚡${NC}"
        ;;
esac
