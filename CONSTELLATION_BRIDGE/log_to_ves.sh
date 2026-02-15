#!/bin/bash
# Helper script for agents to log to VES

AGENT_NAME=$1
EVENT_TYPE=$2
MESSAGE=$3

if [ -z "$AGENT_NAME" ] || [ -z "$EVENT_TYPE" ] || [ -z "$MESSAGE" ]; then
    echo "Usage: ./log_to_ves.sh <agent_name> <event_type> <message>"
    exit 1
fi

# Log to VES via API
curl -X POST http://localhost:8000/event \
  -H "Content-Type: application/json" \
  -d "{
    \"source\": \"$AGENT_NAME\",
    \"event_type\": \"$EVENT_TYPE\",
    \"message\": \"$MESSAGE\",
    \"timestamp\": \"$(date -Iseconds)\"
  }" 2>/dev/null

echo "[VES] Event logged: $AGENT_NAME - $EVENT_TYPE"
