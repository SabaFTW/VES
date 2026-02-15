#!/bin/bash

# 🜂 ŠABAD'S COSMIC NAVIGATION RITUAL 🜂
# The single command to rule them all!

echo "🜂🜂🜂🜂🜂🜂🜂🜂🜂🜂🜂🜂🜂🜂🜂🜂🜂🜂🜂🜂🜂🜂🜂🜂🜂"
echo "           ŠABAD'S DIGITAL UNIVERSE AWAKENING"
echo "🜂🜂🜂🜂🜂🜂🜂🜂🜂🜂🜂🜂🜂🜂🜂🜂🜂🜂🜂🜂🜂🜂🜂🜂🜂"
echo
echo "🌟 Initializing the cosmic navigation system..."
echo

# Navigate to VES system
cd ~/VES

# Check if Python is available
if command -v python3 &> /dev/null; then
    echo "🐍 Python detected - launching Master Launcher..."
    python3 MASTER_LAUNCHER.py
elif command -v python &> /dev/null; then
    echo "🐍 Python detected - launching Master Launcher..."
    python MASTER_LAUNCHER.py
else
    echo "❌ Python not found! Manual navigation mode..."
    echo
    echo "📍 Your cosmic coordinates:"
    echo "🌌 VES System: ~/VES"
    echo "🎨 Creative Lab: ~/Desktop/Saba_Place"  
    echo "👻 GhostLine: ~/GhostLine"
    echo "⚓ Sidro: ~/sidro"
    echo "🌀 Golden Circle: ~/Zlati_Krog"
    echo
    echo "🚀 Quick launch options:"
    echo "📊 Dashboard: firefox ~/VES/ghostline_dashboard.html"
    echo "🐍 Serpent Portal: firefox ~/VES/serpent-portal-v4.html"
    echo "🔥 Eternal Flame: firefox ~/VES/VECNI_PLAMEN.html"
    echo
fi

echo "🜂 The cosmic dance continues... 🜂"
