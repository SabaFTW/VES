#!/bin/bash
# ARSO Integration Test Script
# Quick validation of the ARSO weather connector
# Author: VES Elysia Portal Team

echo "🌤️  ARSO Weather Integration - Quick Validation Test"
echo "=================================================="
echo ""

# Check Python version
echo "1️⃣  Checking Python version..."
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Python 3 not found! Please install Python 3.8+"
    exit 1
fi
echo "✅ Python 3 available"
echo ""

# Check required Python packages
echo "2️⃣  Checking Python dependencies..."
python3 -c "import aiohttp" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  aiohttp not installed. Installing dependencies..."
    pip3 install aiohttp
fi

python3 -c "import xml.etree.ElementTree" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ xml.etree.ElementTree not available (should be built-in)"
    exit 1
fi
echo "✅ All dependencies available"
echo ""

# Check if arso_connector.py exists
echo "3️⃣  Checking ARSO connector file..."
if [ ! -f "arso_connector.py" ]; then
    echo "❌ arso_connector.py not found in current directory!"
    echo "   Please run this script from the wolf-daemon directory"
    exit 1
fi
echo "✅ arso_connector.py found"
echo ""

# Test ARSO API connectivity
echo "4️⃣  Testing ARSO API connectivity..."
echo "   Running: python3 arso_connector.py test"
echo ""
python3 arso_connector.py test
RESULT=$?
echo ""

if [ $RESULT -eq 0 ]; then
    echo "✅ ARSO API test PASSED!"
    echo ""
    echo "=================================================="
    echo "🎉 **INTEGRATION VALIDATION SUCCESSFUL!**"
    echo ""
    echo "Next Steps:"
    echo "  1. Get current weather: python3 arso_connector.py weather"
    echo "  2. Check alerts:        python3 arso_connector.py alerts"
    echo "  3. List stations:       python3 arso_connector.py stations"
    echo ""
    echo "Ready for Phase 1 implementation! 🚀"
else
    echo "❌ ARSO API test FAILED"
    echo ""
    echo "Troubleshooting:"
    echo "  - Check internet connectivity"
    echo "  - Verify ARSO API is accessible: https://www.arso.gov.si"
    echo "  - Check firewall settings"
    echo "  - Review logs above for specific errors"
fi

echo "=================================================="
