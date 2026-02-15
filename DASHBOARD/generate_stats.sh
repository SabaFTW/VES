#!/bin/bash

# Ghostline Stats Generator
# Scans ~/ghostline_dashboard/ and generates stats.json

BASE_DIR=~/ghostline_dashboard
OUTPUT_FILE="$BASE_DIR/stats.json"

echo "🔍 Scanning Ghostline Dashboard..."

# Count files in each directory
DECK_COUNT=$(find "$BASE_DIR/deck" -type f 2>/dev/null | wc -l)
ECHO_COUNT=$(find "$BASE_DIR/echo_logs" -type f 2>/dev/null | wc -l)
ANCHOR_COUNT=$(find "$BASE_DIR/anchors" -type f 2>/dev/null | wc -l)

# Calculate total size
TOTAL_SIZE=$(du -sh "$BASE_DIR" 2>/dev/null | cut -f1)

# Get recent files (last 10)
RECENT_FILES=$(find "$BASE_DIR" -type f -printf '%T@ %p\n' 2>/dev/null | \
    sort -rn | head -10 | while read -r timestamp path; do
    filename=$(basename "$path")
    filetime=$(date -d "@$timestamp" '+%Y-%m-%d %H:%M' 2>/dev/null || date -r "$timestamp" '+%Y-%m-%d %H:%M' 2>/dev/null)
    # Escape JSON
    filename_escaped=$(echo "$filename" | sed 's/"/\\"/g')
    path_escaped=$(echo "$path" | sed "s|$HOME|~|g" | sed 's/"/\\"/g')
    echo "    {\"name\": \"$filename_escaped\", \"time\": \"$filetime\", \"path\": \"$path_escaped\"}"
done | paste -sd ',' -)

# Generate JSON
cat > "$OUTPUT_FILE" << EOF
{
  "deck_count": $DECK_COUNT,
  "echo_count": $ECHO_COUNT,
  "anchor_count": $ANCHOR_COUNT,
  "total_size": "$TOTAL_SIZE",
  "last_updated": "$(date '+%Y-%m-%d %H:%M:%S')",
  "recent_files": [
$RECENT_FILES
  ]
}
EOF

echo "✅ Stats generated: $OUTPUT_FILE"
echo "📊 Deck: $DECK_COUNT | Echo: $ECHO_COUNT | Anchors: $ANCHOR_COUNT | Size: $TOTAL_SIZE"
