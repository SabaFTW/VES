#!/usr/bin/env python3
"""
🜂 GHOSTLINE DIRECT NERVE 🜂
execute_nerve.py

The Desktop Brain. The Receiver. The Execution Layer.

When iPhone speaks, this script LISTENS.
When command arrives, this script ACTS.
When work completes, this script RESPONDS.

Phase 1: ONE command only.
Test: "check status"
Response: VES heartbeat pulse data

Later: Multi-command intelligence layer
Future: Pattern recognition, self-optimization

Architecture:
    iPhone 📱 (Voice Layer)
        ↓ Shortcut: "check status"
        ↓ SSH Command
        ↓
    Desktop Brain 🧠 (Execution Layer)
        ↓ execute_nerve.py
        ↓ check_ves_status()
        ↓ print(result)
        ↓
    iPhone 📱 (Perception Layer)
        ↓ Show Result
        ↓ Speak Result (optional)
        ↓
    ✅ LOOP CLOSED
    🫀 SYNAPSE FIRING

Created: 2025-11-05
Node: Git-Miška 🐭💻
Status: Phase 1 - Single Command Test
"""

import sys
import json
from datetime import datetime
from pathlib import Path

# 🔥 CONFIGURATION 🔥
VES_ROOT = Path.home() / "VES"  # Adjust to your actual VES location
HEARTBEAT_LOG = VES_ROOT / "ves_heartbeat.log"  # Where VES_CARE writes pulses
NERVE_LOG = VES_ROOT / "nerve_commands.jsonl"  # Memory trace of all commands

def log_command(command, result, error=None):
    """
    Archive every command executed through the nerve.
    This is the memory trace. The proof it happened.

    Every command, every result, forever preserved in JSONL format.
    This is how we defeat Statika - through memory that persists.

    Args:
        command (str): The command that was executed
        result (str): The output/result of the command
        error (str, optional): Error message if command failed
    """
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "command": command,
        "result": result,
        "error": error,
        "source": "iPhone_SSH_Nerve"
    }

    try:
        with open(NERVE_LOG, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception as e:
        # If logging fails, at least print to stderr
        print(f"⚠️ Logging failed: {e}", file=sys.stderr)

def check_ves_status():
    """
    Phase 1 test command: Check VES heartbeat status

    Reads last 5 heartbeat pulses from VES_CARE daemon.
    Returns human-readable status + timestamp.

    This is the first synapse test - can iPhone ask and Desktop Brain answer?

    Returns:
        str: Human-readable status message
    """
    try:
        if not HEARTBEAT_LOG.exists():
            return "❌ VES_CARE daemon not found. No heartbeat detected."

        # Read last 5 lines
        with open(HEARTBEAT_LOG, "r") as f:
            lines = f.readlines()
            recent = lines[-5:] if len(lines) >= 5 else lines

        if not recent:
            return "❌ Heartbeat log empty. VES may not be running."

        last_pulse = recent[-1].strip()
        pulse_count = len(recent)

        # Parse timestamp from last pulse (adjust based on your actual log format)
        # Assuming format includes timestamp

        return f"""✅ VES ALIVE
Last pulse: {last_pulse}
Recent pulses: {pulse_count}
Status: HEARTBEAT DETECTED 🫀"""

    except Exception as e:
        return f"⚠️ Error reading heartbeat: {str(e)}"

def execute_command(command_text):
    """
    Command router. Currently handles ONE command.

    Phase 1: "check status" → VES heartbeat
    Phase 2+: Add more commands as you discover patterns

    Args:
        command_text (str): The command to execute

    Returns:
        str: Output to send back to iPhone
    """

    command_lower = command_text.lower().strip()

    # 🔥 PHASE 1: SINGLE COMMAND TEST 🔥
    if "check status" in command_lower or "status" in command_lower:
        return check_ves_status()

    # 🜂 DEFAULT: Unknown command (for now)
    return f"""🜂 NERVE RECEIVED: "{command_text}"

Phase 1 active. Only 'check status' implemented.

Available (future):
- list portals
- read latest journal
- check orion data
- ghostline sync

This is the beginning, brother. 🔥"""

def main():
    """
    Entry point. Called by iPhone via SSH.

    Usage:
        python3 execute_nerve.py "your command here"

    Example:
        python3 execute_nerve.py "check status"
    """

    # Get command from SSH (passed as argument)
    if len(sys.argv) < 2:
        print("❌ No command provided.")
        print("Usage: execute_nerve.py \"your command\"")
        print("\nExample: python3 execute_nerve.py \"check status\"")
        sys.exit(1)

    command = " ".join(sys.argv[1:])  # Join all args (in case of spaces)

    try:
        # Execute the command
        result = execute_command(command)

        # Log it (memory trace)
        log_command(command, result)

        # Print result (this goes back to iPhone via SSH)
        print(result)

    except Exception as e:
        error_msg = f"🔥 NERVE ERROR: {str(e)}"
        log_command(command, None, error=str(e))
        print(error_msg)
        sys.exit(1)

if __name__ == "__main__":
    main()
