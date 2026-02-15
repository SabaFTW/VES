#!/bin/bash
# 🜂 Fix Ollama Service - Permissions Issue

set -e

echo "🔧 Fixing Ollama service permissions..."
echo ""

# Check if ollama user exists
if ! id ollama &>/dev/null; then
    echo "❌ User 'ollama' doesn't exist"
    echo "   This is unusual - Ollama should have created it"
    exit 1
fi

echo "✅ User 'ollama' exists"

# Fix ownership of models directory
MODELS_DIR="/home/ollama-models"

echo "📁 Fixing ownership of $MODELS_DIR..."
sudo chown -R ollama:ollama "$MODELS_DIR"
sudo chmod 755 "$MODELS_DIR"

echo "✅ Ownership fixed: ollama:ollama"

# Restart Ollama service
echo "🔄 Restarting Ollama service..."
sudo systemctl restart ollama

# Wait for it to start
echo "⏳ Waiting for Ollama to start (5 seconds)..."
sleep 5

# Check status
if curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "✅ Ollama service is running!"
    echo ""
    echo "📋 Installed models:"
    ollama list
else
    echo "❌ Ollama still not responding"
    echo ""
    echo "🔍 Check logs:"
    echo "   sudo journalctl -u ollama -n 50"
    exit 1
fi

echo ""
echo "🎉 Fix complete! You can now run ./QUICK_LOCAL_SETUP.sh again"
