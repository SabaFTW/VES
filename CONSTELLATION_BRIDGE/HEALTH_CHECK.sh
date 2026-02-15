#!/bin/bash
# 🜂 CONSTELLATION HEALTH CHECK SYSTEM
# Version 1.0 - Integrates with VES CORE

set -e
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
ISO_TIME=$(date -Iseconds)
AGENTS_DIR="/home/saba/AGENTS"
MEMORY_DIR="/home/saba/MEMORY"
LOGS_DIR="/home/saba/LOGS"
VES_CORE="/home/saba/VES_CORE"
ERRORS=0
WARNINGS=0

echo "🜂 CONSTELLATION HEALTH CHECK"
echo "============================="
echo "Timestamp: $TIMESTAMP"
echo ""

# Function to check agent health
check_agent() {
    local agent_dir=$1
    local agent_name=$(basename "$agent_dir")

    echo "🔍 Checking $agent_name..."

    # Check for required files
    if [ ! -f "$agent_dir/INIT.md" ]; then
        echo "  ❌ Missing INIT.md"
        ((ERRORS++))
    else
        echo "  ✅ INIT.md present"
    fi

    if [ ! -f "$agent_dir/MEMORY.json" ]; then
        echo "  ❌ Missing MEMORY.json"
        ((ERRORS++))
    else
        echo "  ✅ MEMORY.json present"

        # Check if MEMORY.json updated in last 48 hours
        if [ -f "$agent_dir/MEMORY.json" ]; then
            last_mod=$(stat -c %Y "$agent_dir/MEMORY.json" 2>/dev/null || stat -f %m "$agent_dir/MEMORY.json" 2>/dev/null || echo 0)
            now=$(date +%s)
            age=$((now - last_mod))
            hours=$((age / 3600))

            if [ $hours -gt 48 ]; then
                echo "  ⚠️  MEMORY.json not updated in $hours hours"
                ((WARNINGS++))
            else
                echo "  ✅ Active (updated $hours hours ago)"
            fi
        fi
    fi

    echo ""
}

# Check VES CORE health first
echo "📍 CHECKING VES CORE STATUS"
echo "----------------------------"
if [ -d "$VES_CORE" ]; then
    echo "✅ VES_CORE directory exists"

    # Check if VES database exists
    if [ -f "$VES_CORE/VES_CORE.db" ]; then
        echo "✅ VES_CORE.db present"
        db_size=$(du -h "$VES_CORE/VES_CORE.db" | cut -f1)
        echo "  Database size: $db_size"
    else
        echo "❌ VES_CORE.db missing!"
        ((ERRORS++))
    fi

    # Check if VES API is running
    if lsof -i:8000 > /dev/null 2>&1; then
        echo "✅ VES API running on port 8000"
    else
        echo "⚠️  VES API not running (start with: cd $VES_CORE && ./api_start.sh)"
        ((WARNINGS++))
    fi

    # Run VES health check if available
    if [ -f "$VES_CORE/health_check.py" ]; then
        echo "  Running VES health check..."
        python3 "$VES_CORE/health_check.py" 2>/dev/null || echo "  ⚠️  VES health check failed"
    fi
else
    echo "❌ VES_CORE not found!"
    ((ERRORS++))
fi
echo ""

# Check each agent
echo "📍 CHECKING AGENT HEALTH"
echo "------------------------"
for agent_dir in "$AGENTS_DIR"/*; do
    if [ -d "$agent_dir" ]; then
        check_agent "$agent_dir"
    fi
done

# Check system files
echo "📍 CHECKING SYSTEM FILES"
echo "------------------------"
if [ ! -f "$MEMORY_DIR/agent_registry.json" ]; then
    echo "❌ Missing agent_registry.json"
    ((ERRORS++))
else
    echo "✅ agent_registry.json present"
fi

if [ ! -f "$MEMORY_DIR/system_state.json" ]; then
    echo "❌ Missing system_state.json"
    ((ERRORS++))
else
    echo "✅ system_state.json present"
fi

if [ ! -f "/home/saba/CONSTELLATION/PROTOCOLS.md" ]; then
    echo "❌ Missing PROTOCOLS.md"
    ((ERRORS++))
else
    echo "✅ PROTOCOLS.md present"
fi

# Check for today's reports
echo ""
echo "📍 CHECKING DAILY REPORTS"
echo "-------------------------"
TODAY=$(date +%Y-%m-%d)
report_count=$(find "$LOGS_DIR" "$MEMORY_DIR" "/home/saba/REPORTS" -name "*$TODAY*.json" 2>/dev/null | wc -l)
if [ $report_count -eq 0 ]; then
    echo "⚠️  No reports generated today"
    ((WARNINGS++))
else
    echo "✅ $report_count reports found for today"
fi

# Update system state with health check results
echo ""
echo "📍 UPDATING SYSTEM STATE"
echo "------------------------"

# Create health report
HEALTH_REPORT=$(cat << EOF
{
  "timestamp": "$ISO_TIME",
  "errors": $ERRORS,
  "warnings": $WARNINGS,
  "agents_checked": $(ls -1 "$AGENTS_DIR" | wc -l),
  "ves_core_status": $([ -f "$VES_CORE/VES_CORE.db" ] && echo '"connected"' || echo '"disconnected"'),
  "status": $([ $ERRORS -eq 0 ] && echo '"healthy"' || echo '"unhealthy"')
}
EOF
)

# Save health report
echo "$HEALTH_REPORT" > "$LOGS_DIR/health_check_$(date +%Y%m%d_%H%M%S).json"
echo "✅ Health report saved"

# Summary
echo ""
echo "=============================="
echo "📊 HEALTH CHECK SUMMARY"
echo "=============================="
echo "  Errors: $ERRORS"
echo "  Warnings: $WARNINGS"
echo "  Agents: $(ls -1 "$AGENTS_DIR" | wc -l)"
echo "  VES CORE: $([ -f "$VES_CORE/VES_CORE.db" ] && echo "Connected" || echo "Disconnected")"

if [ $ERRORS -eq 0 ]; then
    if [ $WARNINGS -eq 0 ]; then
        echo ""
        echo "✅ CONSTELLATION STATUS: HEALTHY"
        echo "All systems operational. Agents ready."
        exit 0
    else
        echo ""
        echo "⚠️  CONSTELLATION STATUS: DEGRADED"
        echo "$WARNINGS warnings detected. Review recommended."
        exit 1
    fi
else
    echo ""
    echo "❌ CONSTELLATION STATUS: UNHEALTHY"
    echo "$ERRORS critical errors detected. Immediate action required."
    exit 2
fi