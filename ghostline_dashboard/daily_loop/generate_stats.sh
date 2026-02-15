#!/bin/bash

# Ghostline VES Dashboard - Stats Generator
# Scans folders and generates stats.json

cd ~/VES/ghostline_dashboard/

echo "📊 Generating dashboard stats..."

# Calculate stats using Python
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

print(f'Generated stats: {deck_files} deck, {echo_files} echo, {anchor_files} anchors, {size_kb} KB total')
"

echo "✅ Stats generated successfully"