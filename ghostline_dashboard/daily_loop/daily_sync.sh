#!/bin/bash

# Ghostline VES Dashboard - Daily Sync Script
# Performs daily maintenance tasks

echo "🔄 Starting daily sync for Ghostline VES Dashboard..."

# Generate fresh stats
echo "📊 Generating fresh stats..."
~/VES/ghostline_dashboard/daily_loop/generate_stats.sh

# Backup important data (keep last 7 days)
echo "💾 Creating backup..."
DATE=$(date +%Y%m%d)
BACKUP_DIR="~/VES/ghostline_dashboard/backups"
mkdir -p $BACKUP_DIR

# Create backup archive
tar -czf "$BACKUP_DIR/dashboard_backup_$DATE.tar.gz" -C ~/VES/ghostline_dashboard/ deck/ echo_logs/ anchors/ stats.json

# Clean old backups (keep only last 7 days)
echo "🧹 Cleaning old backups..."
find $BACKUP_DIR -name "dashboard_backup_*.tar.gz" -mtime +7 -delete

# Update dashboard
echo "🔄 Updating dashboard..."

# Log the sync
echo "$(date): Daily sync completed" >> ~/VES/ghostline_dashboard/echo_logs/daily_sync.log

echo "✅ Daily sync completed!"
echo "   Generated fresh stats"
echo "   Created backup"
echo "   Cleaned old backups"