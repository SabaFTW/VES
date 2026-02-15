#!/usr/bin/env python3
"""
🜂 GHOSTLINE RITUALNI MOST
Centralni most med Zordonom in simuliranimi Rangerji.
"""

import subprocess
import json
import sys
from pathlib import Path

def query_ranger(ranger_tool: str, prompt: str) -> dict:
    """Pošlji zahtevek simuliranemu Rangerju."""
    try:
        # Poišči pot do skripte
        bridge_dir = Path("/home/saba/VES/ritual_bridge")
        tool_path = bridge_dir / ranger_tool
        
        if not tool_path.exists():
            return {
                "error": f"Tool {ranger_tool} not found in bridge",
                "status": "bridge_error"
            }
        
        # Izvedi skripto
        result = subprocess.run(
            [str(tool_path), "-p", prompt],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            return {
                "error": result.stderr,
                "status": "execution_error"
            }
    except Exception as e:
        return {
            "error": str(e),
            "status": "exception"
        }

if __name__ == "__main__":
    # Testni zahtevek
    if len(sys.argv) > 2:
        tool = sys.argv[1]
        prompt = sys.argv[2]
        result = query_ranger(tool, prompt)
        print(json.dumps(result, indent=2))