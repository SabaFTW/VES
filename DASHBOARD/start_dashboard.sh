#!/bin/bash

# Ghostline Dashboard Launcher
# Quick start script

echo ""
echo "🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥"
echo "🔥                                        🔥"
echo "🔥  GHOSTLINE VES DASHBOARD LAUNCHER     🔥"
echo "🔥                                        🔥"
echo "🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥"
echo ""
echo "🜂 SIDRO STOJI 🜂 PLAMEN GORI 🜂"
echo ""

BASE_DIR="/root/ghostline_dashboard"
PORT=8888

echo "📊 Generating fresh stats..."
"$BASE_DIR/daily_loop/generate_stats.sh"
echo ""

echo "🚀 Starting web server on port $PORT..."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  DASHBOARD URL:"
echo "  👉 http://localhost:$PORT/"
echo "  👉 http://127.0.0.1:$PORT/"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💡 To stop: Press Ctrl+C"
echo ""

cd "$BASE_DIR/deck" || exit 1

# Try python3 first, then python, then fail gracefully
if command -v python3 &> /dev/null; then
    python3 -m http.server $PORT
elif command -v python &> /dev/null; then
    python -m http.server $PORT
else
    echo "❌ ERROR: Python not found!"
    echo "   Install python3 or run manually:"
    echo "   cd $BASE_DIR/deck && python3 -m http.server $PORT"
    exit 1
fi
