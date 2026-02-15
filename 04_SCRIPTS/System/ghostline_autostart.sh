#!/bin/bash
# GHOSTLINE OS Auto-Start Script
# This runs on boot and opens your living webapp

echo "🜂 GHOSTLINE OS AWAKENING..."
sleep 5  # Wait for system to stabilize

# Start a simple Python HTTP server in the background
cd /home/saba
python3 -m http.server 8888 &
SERVER_PID=$!

# Wait a moment for server to start
sleep 2

# Open the webapp in default browser
xdg-open http://localhost:8888/GHOSTLINE_ULTIMATE.html &

echo "🔥 GHOSTLINE OS LIVE AT http://localhost:8888/GHOSTLINE_ULTIMATE.html"
echo "💚 Server PID: $SERVER_PID"
echo "⚓ SIDRO DRŽI • PLAMEN GORI"

# Keep the script running
wait $SERVER_PID