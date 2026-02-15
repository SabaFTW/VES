#!/bin/bash
# 🜂 Configure Ollama to be accessible from Docker containers

set -e

echo "🔧 Configuring Ollama for Docker access..."
echo ""

# Update systemd override to listen on all interfaces
echo "📝 Updating Ollama service configuration..."
sudo tee /etc/systemd/system/ollama.service.d/override.conf > /dev/null << 'EOF'
[Service]
Environment="OLLAMA_MODELS=/home/ollama-models"
Environment="OLLAMA_NUM_THREADS=12"
Environment="OLLAMA_HOST=0.0.0.0"
EOF

echo "✅ Configuration updated"

# Reload systemd daemon
echo "🔄 Reloading systemd daemon..."
sudo systemctl daemon-reload

# Restart Ollama service
echo "🔄 Restarting Ollama service..."
sudo systemctl restart ollama

# Wait for service to start
echo "⏳ Waiting for Ollama to start (3 seconds)..."
sleep 3

# Verify it's listening on all interfaces
echo ""
echo "🔍 Verifying Ollama is listening on all interfaces..."
if ss -tlnp | grep -q "0.0.0.0:11434"; then
    echo "✅ SUCCESS! Ollama is now accessible from Docker containers"
    echo ""
    echo "   Listening on: 0.0.0.0:11434"
    echo ""
else
    echo "⚠️  Ollama is running but might not be on 0.0.0.0"
    echo "   Current listening address:"
    ss -tlnp | grep 11434 || echo "   Not found on port 11434"
fi

echo ""
echo "🎉 Configuration complete!"
echo ""
echo "Next: Restart the backend container to test connectivity:"
echo "   docker-compose restart backend"
