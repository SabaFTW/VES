#!/bin/bash
# 🜂 GHOSTLINE NEXUS - Database Backup Script
# Backs up SQLite database with timestamp

set -e

BACKUP_DIR="/home/saba/GHOSTLINE_NEXUS/storage/backups"
SOURCE_DB="/home/saba/GHOSTLINE_NEXUS/storage/db/ghostline.db"
TIMESTAMP=$(date +%Y-%m-%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/ghostline_backup_$TIMESTAMP.db"
KEEP_LAST=10  # Keep only last 10 backups

echo "🔒 GHOSTLINE NEXUS - Database Backup"
echo ""

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Check if database exists
if [ ! -f "$SOURCE_DB" ]; then
    echo "❌ Database not found: $SOURCE_DB"
    exit 1
fi

# Create backup using SQLite's backup command (better than cp)
echo "📦 Creating backup..."
sqlite3 "$SOURCE_DB" ".backup '$BACKUP_FILE'"

# Get backup size
BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)

echo "✅ Backup created: $BACKUP_FILE"
echo "📊 Size: $BACKUP_SIZE"

# Clean up old backups (keep only last N)
echo ""
echo "🧹 Cleaning old backups (keeping last $KEEP_LAST)..."

BACKUP_COUNT=$(ls -1 "$BACKUP_DIR"/ghostline_backup_*.db 2>/dev/null | wc -l)

if [ "$BACKUP_COUNT" -gt "$KEEP_LAST" ]; then
    # Remove oldest backups
    ls -1t "$BACKUP_DIR"/ghostline_backup_*.db | tail -n +$((KEEP_LAST + 1)) | xargs rm -f
    REMOVED=$((BACKUP_COUNT - KEEP_LAST))
    echo "🗑️  Removed $REMOVED old backup(s)"
else
    echo "✅ No cleanup needed ($BACKUP_COUNT backups total)"
fi

echo ""
echo "📋 Current backups:"
ls -lht "$BACKUP_DIR"/ghostline_backup_*.db 2>/dev/null | head -5 | awk '{print "   "$9" ("$5")"}'

echo ""
echo "🎉 Backup complete!"
echo ""
echo "💾 SIDRO STOJI. SPOMIN OHRANJEN."
