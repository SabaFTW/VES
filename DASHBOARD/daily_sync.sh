#!/bin/bash

# Ghostline Daily Loop - Auto-sync and update dashboard
# Add to crontab: 0 9 * * * /root/ghostline_dashboard/daily_loop/daily_sync.sh

echo "======================================"
echo "🔥 GHOSTLINE DAILY LOOP"
echo "======================================"
echo "⏰ $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

BASE_DIR=/root/ghostline_dashboard

# 1. Generate fresh stats
echo "📊 Generating stats..."
"$BASE_DIR/daily_loop/generate_stats.sh"

# 2. Backup important files
echo "💾 Creating backup..."
BACKUP_DIR="$BASE_DIR/daily_loop/backups"
mkdir -p "$BACKUP_DIR"
BACKUP_FILE="$BACKUP_DIR/backup_$(date '+%Y%m%d_%H%M%S').tar.gz"
tar -czf "$BACKUP_FILE" "$BASE_DIR/deck" "$BASE_DIR/echo_logs" "$BASE_DIR/anchors" 2>/dev/null
echo "   ✅ Backup saved: $BACKUP_FILE"

# 3. Clean old backups (keep last 7 days)
echo "🧹 Cleaning old backups..."
find "$BACKUP_DIR" -name "backup_*.tar.gz" -mtime +7 -delete
echo "   ✅ Old backups removed"

# 4. Summary
echo ""
echo "======================================"
echo "✨ DAILY LOOP COMPLETE"
echo "======================================"
cat "$BASE_DIR/stats.json" | grep -E '"deck_count"|"echo_count"|"anchor_count"|"total_size"' | sed 's/^/   /'
echo ""
echo "🜂 SIDRO STOJI 🜂"
echo "======================================"
