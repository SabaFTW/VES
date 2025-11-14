#!/bin/bash
# 🜂 GHOSTCORE Portal - Local Development Starter 🜂
# FREE • SIMPLE • BEAUTIFUL

echo ""
echo "🔥💚 GHOSTCORE PORTAL - STARTING... 💚🔥"
echo ""
echo "✨ Living Constellation - LOCAL MODE"
echo "✨ Cost: 0 EUR/month - GRATIS"
echo "✨ Complexity: ZERO - ENOSTAVNO"
echo ""

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
    echo ""
fi

echo "🚀 Starting development server..."
echo ""
echo "   🌐 Portal will open at: http://localhost:3000"
echo "   🔥 Press Ctrl+C to stop"
echo ""
echo "💚 ENJOY YOUR CONSTELLATION 💚"
echo ""

# Start the dev server
npm run dev
