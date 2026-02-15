#!/bin/bash
# AI Process Priority Configuration

# Function to increase priority of AI-related processes
set_ai_priority() {
    # Find and set high priority for AI-related processes
    for pid in $(pgrep -f "openclaw\|n8n\|node"); do
        sudo renice -15 $pid 2>/dev/null
        sudo ionice -c 1 -n 0 -p $pid 2>/dev/null
    done
    
    # Set Firefox (browser) to medium priority to balance performance
    for pid in $(pgrep firefox); do
        sudo renice -5 $pid 2>/dev/null
    done
}

# Function to limit non-essential processes
limit_non_essential() {
    # Reduce priority of background services
    for pid in $(pgrep -f "systemd\|dbus\|polkit"); do
        sudo renice 5 $pid 2>/dev/null
    done
}

# Run optimization functions
set_ai_priority
limit_non_essential

echo "AI process priorities set!"