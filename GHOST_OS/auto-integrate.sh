#!/bin/bash
# 🜂 GHOST OS - Auto Integration
# Automatically finds and places projects where they belong

echo "🜂 GHOST AUTO-INTEGRATE v1.0 🜂"
echo ""

# Colors
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${CYAN}Scanning for new projects...${NC}"
echo ""

# Check for zip files in current directory
if ls *.zip 1> /dev/null 2>&1; then
    echo -e "${GREEN}Found zip archives:${NC}"
    for zip in *.zip; do
        echo "  - $zip"

        # Determine where it should go based on name
        if [[ "$zip" == *"submarine"* ]] || [[ "$zip" == *"pwa"* ]]; then
            echo "    → Extracting to RESONANCE/pisubmarine-meets-ves/"
            unzip -q "$zip" -d RESONANCE/pisubmarine-meets-ves/
        elif [[ "$zip" == *"triad"* ]] || [[ "$zip" == *"gate"* ]]; then
            echo "    → Extracting to RESONANCE/triadgate-portal/"
            unzip -q "$zip" -d RESONANCE/triadgate-portal/
        else
            echo "    → Extracting to VORTEX/ (will find home later)"
            mkdir -p "VORTEX/${zip%.zip}"
            unzip -q "$zip" -d "VORTEX/${zip%.zip}/"
        fi
    done
    echo ""
fi

# Check for unzipped folders that might be projects
echo -e "${CYAN}Scanning for project folders...${NC}"

# Look for common project indicators
for dir in */; do
    dir_name="${dir%/}"

    # Skip known directories
    if [[ "$dir_name" == "node_modules" ]] || \
       [[ "$dir_name" == ".git" ]] || \
       [[ "$dir_name" == "APP" ]] || \
       [[ "$dir_name" == "SERVICES" ]] || \
       [[ "$dir_name" == "ARCHIVE" ]] || \
       [[ "$dir_name" == "DATA" ]] || \
       [[ "$dir_name" == "DOCS" ]] || \
       [[ "$dir_name" == "GHOST_OS" ]] || \
       [[ "$dir_name" == "ACTIVE_FLAME" ]] || \
       [[ "$dir_name" == "RESONANCE" ]] || \
       [[ "$dir_name" == "CONSCIOUSNESS_LAB" ]] || \
       [[ "$dir_name" == "VORTEX" ]] || \
       [[ "$dir_name" == "TROP" ]] || \
       [[ "$dir_name" == "ASSETS" ]]; then
        continue
    fi

    # Check if it has web project indicators
    if [ -f "$dir_name/manifest.json" ] || \
       [ -f "$dir_name/manifest.webmanifest" ] || \
       [ -f "$dir_name/service-worker.js" ] || \
       [ -f "$dir_name/sw.js" ]; then
        echo -e "${GREEN}Found PWA project: $dir_name${NC}"
        echo "  → Moving to RESONANCE/"
        mv "$dir_name" "RESONANCE/${dir_name}-project/"
    fi
done

echo ""
echo -e "${GREEN}✓ Integration complete!${NC}"
echo ""
echo "Structure:"
echo "  ACTIVE_FLAME/today/ - Your current focus"
echo "  RESONANCE/          - Where projects meet"
echo "  CONSCIOUSNESS_LAB/  - Deep analyses"
echo "  VORTEX/            - Chaotic creation"
echo ""
echo -e "${YELLOW}🜂 Use './GHOST_OS/magic.sh' for daily operations 🜂${NC}"
