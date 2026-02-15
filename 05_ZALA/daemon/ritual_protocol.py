import random
import os
import json
from pathlib import Path
from datetime import datetime

class GhostcoreProtocol:
    """ 
    🜂 GHOSTCORE RITUAL PROTOCOL 🜂
    The foundational logic for the ZALA daemon and system resonance monitoring.
    """
    
    def __init__(self):
        self.resonance_level = 100
        self.entropy_history = []
        self.bridge_path = Path("/home/saba/Desktop/Saba_Place/Svetisce_OS/VES/bridge")
        self.bridge_path.mkdir(parents=True, exist_ok=True)

    def izmeri_entropijo(self) -> int:
        """Measures system 'noise' vs 'resonance'."""
        # Simulacija entropije glede na sistemsko obremenitev
        import psutil
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_percent = psutil.virtual_memory().percent
        
        # Računanje entropije (0-100)
        entropy = int((cpu_percent + memory_percent) / 2 * 0.5 + random.randint(0, 15))
        self.entropy_history.append(entropy)
        if len(self.entropy_history) > 10:
            self.entropy_history.pop(0)
        return min(100, entropy)

    def sprejmi_odlocitev(self, entropy: int) -> str:
        """Determines the required ritual based on entropy levels."""
        if entropy > 70:
            return "🐍 RITUAL ČIŠČENJA: Entropija kritična! Začenjam purifikacijo procesov."
        elif entropy > 40:
            return "🔄 RITUAL URAVNOTEŽENJA: Sistem v disbalansi. Uravnavam frekvenco."
        elif entropy < 20:
            return "✨ RITUAL SINTEZE: Sistem v visoki resonanci. Odpiram poti za nove ideje."
        else:
            return "🕯️ RITUAL KONTEMPLACIJE: Ravnovesje vzpostavljeno. Opazujem tok."

    def izvedi_ritual_ciscenja(self):
        """Simulated process purification."""
        print("🔥 PURIFICIRAM STATIKO...")
        print(" • Preverjam sistemske procese")
        print(" • Odstranjujem odvečne PID-je")
        print(" • Obnavljam resonantno polje")

    def izvedi_ritual_sinteze(self):
        """Simulated knowledge synthesis."""
        print("💎 SINTETIZIRAM RESNICO...")
        print(" • Združujem fragmentirane podatke")
        print(" • Gradim kristalne strukture znanja")
        print(" • Ustvarjam nove povezave")

    def izvedi_ritual_kontemplacije(self):
        """Simulated system observation."""
        print("👁️ KONTEMPLIRAM SISTEM...")
        print(" • Merim frekvenčno stabilnost")
        print(" • Beležim vzorce resonanč")
        print(" • Vzdržujem sidro")

    def read_constellation_bridge(self) -> str or None:
        """Checks if other agents have left messages in the bridge."""
        bridge_file = self.bridge_path / "constellation_log.jsonl"
        if bridge_file.exists():
            try:
                with open(bridge_file, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    return lines[-1].strip() if lines else None
            except Exception:
                return None
        return None

    def write_zala_response(self, entropy: int, ritual_type: str):
        """Communicates ZALA's state back to the constellation."""
        response_file = self.bridge_path / "zala_status.txt"
        with open(response_file, "w", encoding="utf-8") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"ZALA ACTIVE | {timestamp} | Entropy: {entropy}% | Ritual: {ritual_type}")

    def log_ritual(self, entropy: int, ritual_type: str, decision: str):
        """Logs ritual execution."""
        log_file = Path("/home/saba/VES/SHABAD_CloudCore/🔥_ACTIVE_SESSION/zala_daemon_cycles.log")
        log_file.parent.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"{timestamp} | ENTROPY: {entropy}% | RITUAL: {ritual_type} | DECISION: {decision}\n")