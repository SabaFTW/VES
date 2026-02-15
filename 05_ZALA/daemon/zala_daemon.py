import time
import json
from datetime import datetime
from pathlib import Path

from ritual_protocol import GhostcoreProtocol

ACTIVE_SESSION_DIR = Path("/home/saba/VES/SHABAD_CloudCore/🔥_ACTIVE_SESSION")
ACTIVE_SESSION_DIR.mkdir(parents=True, exist_ok=True)
RES_BRIDGE_PATH = ACTIVE_SESSION_DIR / "zala_resonance_bridge.txt"
RES_DAEMON_LOG = ACTIVE_SESSION_DIR / "zala_daemon_cycles.log"

# Constellation bridge (inter-agent coordination)
CONSTELLATION_BRIDGE = Path("/home/saba/Desktop/Saba_Place/Svetisce_OS/VES/bridge")
CONSTELLATION_BRIDGE.mkdir(parents=True, exist_ok=True)
CONSTELLATION_LOG = CONSTELLATION_BRIDGE / "constellation_log.jsonl"

zala = GhostcoreProtocol()

print("🜂 ZALA DAEMON MODE ACTIVE")
print("🌉 Constellation bridge enabled")


def log_resonance(entropy: int, ritual_type: str, decision: str, bridge_message: str | None) -> None:
    """Append cycle details to the resonance bridge for constellation visibility."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    preview = ""
    if bridge_message:
        preview = bridge_message.strip().splitlines()[0][:120]

    bridge_lines = [
        "🐍 ZALA DAEMON CYCLE 🐍",
        f"TIMESTAMP: {timestamp}",
        f"ENTROPY: {entropy}%",
        f"RITUAL: {ritual_type}",
        f"DECISION: {decision}",
    ]
    if preview:
        bridge_lines.append(f"BRIDGE MSG: {preview}")
    bridge_lines.append("🜂 cycle recorded")

    entry = "\n".join(bridge_lines) + "\n\n"

    with RES_BRIDGE_PATH.open("a", encoding="utf-8") as bridge_file:
        bridge_file.write(entry)

    with RES_DAEMON_LOG.open("a", encoding="utf-8") as log_file:
        log_file.write(
            f"{timestamp} | entropy={entropy}% | ritual={ritual_type} | decision={decision}"
            f"{f' | bridge={preview}' if preview else ''}\n"
        )


def log_to_constellation(entropy: int, ritual_type: str, action: str, status: str) -> None:
    """Log ritual execution to constellation bridge (JSONL format for inter-agent coordination)."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    entry = {
        "timestamp": timestamp,
        "agent": "LYRA/ZALA",
        "entropija": entropy,
        "ritual": ritual_type,
        "action": action,
        "status": status
    }
    
    with CONSTELLATION_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


while True:
    # Check constellation bridge for messages
    bridge_msg = zala.read_constellation_bridge()

    # Measure system state
    ent = zala.izmeri_entropijo()
    decision = zala.sprejmi_odlocitev(ent)

    print(f"\n[{time.strftime('%H:%M:%S')}] {decision}")

    # Execute ritual based on entropy
    ritual_type = "Contemplation"
    action = "System check"
    status = "OK"
    
    if "Ciscenja" in decision:
        zala.izvedi_ritual_ciscenja()
        ritual_type = "Cleansing"
        action = "Killed processes"
    elif "Sinteze" in decision and ent < 15:
        zala.izvedi_ritual_sinteze()
        ritual_type = "Synthesis"
        action = "Browser opened"
    elif "Kontemplacije" in decision:
        zala.izvedi_ritual_kontemplacije()
        ritual_type = "Contemplation"
        action = "Status check"

    # Write response to constellation
    zala.write_zala_response(ent, ritual_type)
    log_resonance(ent, ritual_type, decision, bridge_msg)
    log_to_constellation(ent, ritual_type, action, status)

    time.sleep(300)  # 5 minut
