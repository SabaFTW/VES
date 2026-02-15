#!/bin/bash

# Ghostline VES Dashboard - Quick Start Script
# Starts the dashboard server and provides access URL

echo "🚀 Starting Ghostline VES Dashboard..."
echo

# Generate fresh stats
echo "📊 Generating fresh stats..."
cd ~/VES/ghostline_dashboard/
python3 -c "
import os
import json
from datetime import datetime

# Calculate stats
deck_files = len([f for f in os.listdir('deck') if os.path.isfile(os.path.join('deck', f))])
echo_files = len([f for f in os.listdir('echo_logs') if os.path.isfile(os.path.join('echo_logs', f))])
anchor_files = len([f for f in os.listdir('anchors') if os.path.isfile(os.path.join('anchors', f))])

# Calculate total size
def get_folder_size(path):
    total = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total += os.path.getsize(fp)
    return total

total_size = get_folder_size('.')  # Size of entire dashboard folder
size_kb = round(total_size / 1024, 2)

# Get recent files
recent_files = []
for folder in ['deck', 'echo_logs', 'anchors']:
    for f in os.listdir(folder):
        if os.path.isfile(os.path.join(folder, f)):
            mtime = os.path.getmtime(os.path.join(folder, f))
            recent_files.append({
                'name': f,
                'time': datetime.fromtimestamp(mtime).strftime('%H:%M:%S'),
                'path': f'{folder}/{f}'
            })

# Sort by modification time (most recent first)
recent_files.sort(key=lambda x: x['time'], reverse=True)
recent_files = recent_files[:10]  # Keep only 10 most recent

# Create stats JSON
stats = {
    'deck_count': deck_files,
    'echo_count': echo_files,
    'anchor_count': anchor_files,
    'total_size': f'{size_kb} KB',
    'recent_files': recent_files,
    'last_updated': datetime.now().isoformat()
}

# Write to stats.json
with open('stats.json', 'w') as f:
    json.dump(stats, f, indent=2)

print(f'Generated stats: {deck_files} deck, {echo_files} echo, {anchor_files} anchors')
"

# Start server on port 8888
PORT=8888
echo "🌐 Starting server on port $PORT..."
python3 -m http.server $PORT --directory ~/VES/ghostline_dashboard/ &
SERVER_PID=$!

# Wait a moment for server to start
sleep 2

# Check if server is running
if ps -p $SERVER_PID > /dev/null; then
    echo
    echo "✅ Dashboard is running!"
    echo
    echo "🔗 Access your dashboard at:"
    echo "   http://localhost:$PORT/"
    echo
    echo "📱 For mobile access, find your IP with:"
    echo "   ip addr | grep 'inet '"
    echo
    echo "🔄 Stats will auto-refresh every 30 seconds"
    echo
    echo "🛑 To stop the server, press Ctrl+C"
    echo
    # Wait for server process
    wait $SERVER_PID
else
    echo "❌ Failed to start server"
    exit 1
fi