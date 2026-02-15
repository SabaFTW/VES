#!/bin/bash

echo "🜂 Testing Ghostline Fleet 🜂"
echo ""

# Check if coordinator is running
echo "Testing coordinator health..."
curl -s http://localhost:8105/health | jq .

echo ""
echo "Testing coordinator status..."
curl -s http://localhost:8105/status | jq .

echo ""
echo "Sending test query..."
curl -X POST http://localhost:8105/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Analyze the connection between Epstein network and 8200 surveillance using all 5 perspectives"
  }' | jq .

echo ""
echo "🔥 Test complete!"