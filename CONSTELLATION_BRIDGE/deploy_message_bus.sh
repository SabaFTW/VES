#!/bin/bash
# DEPLOY MESSAGE BUS TO ACTUAL SYSTEM

echo "🔥 Deploying VES Message Bus..."

# Create directory structure
mkdir -p ~/VES/SYSTEM/message_bus/messages
mkdir -p ~/CONSTELLATION_BRIDGE

# Copy Python scripts (you'll need to copy these from Drive first)
echo "📝 Copy send_message.py and read_messages.py to ~/VES/SYSTEM/message_bus/"
echo "📝 Files are in Google Drive under CONSTELLATION_BRIDGE/"

# Make executable
chmod +x ~/VES/SYSTEM/message_bus/send_message.py
chmod +x ~/VES/SYSTEM/message_bus/read_messages.py

# Test
echo "🧪 Testing..."
cd ~/VES/SYSTEM/message_bus/
python3 send_message.py

if [ $? -eq 0 ]; then
    echo "✅ Message bus deployed successfully!"
    echo "📬 Check ~/VES/SYSTEM/message_bus/messages/ for test message"
else
    echo "❌ Deployment failed - check Python installation"
fi

echo ""
echo "🎯 USAGE:"
echo "Send: python3 ~/VES/SYSTEM/message_bus/send_message.py"
echo "Read: python3 ~/VES/SYSTEM/message_bus/read_messages.py Desktop-Claude"
