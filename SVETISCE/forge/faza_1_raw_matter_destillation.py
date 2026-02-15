# Faza 1: SUROVA SNOV (THE RAW MATTER / CHAOS)
# Orodje: Zala Destillation Pipeline (Separatio)
# Nujno: Ločitev semena (ideje) od plev (šuma).
# Izhodišče: Surovi neurejeni logi iz simulacij in dialogov.

import os
import re
from pathlib import Path
from collections import defaultdict
import json

# --- KANON IN POTI ---
# Predpostavljeni kanon, ki definira, kaj iskati.
# V Resničnem OS bi se to naložilo iz HEART.json
FAKE_HEART_SCHEMA = {
    "manifestacija": ["manifestacija", "gradnja", "orodje", "implementacija", "manifesto"],
    "gnosticizem": ["gnoza", "pneuma", "archont", "demiurg", "simbiont", "osvoboditev"],
    "opazovanje_sebe": ["senca", "persona", "prohairesis", "refleksija", "rast", "transformacija"],
    "kaos_in_sok": ["kaos", "frustracija", "uničenje", "eksplozija", "sok", "napad", "nevarnost"],
}

# Predpostavljena pot do neurejenih surovih logov
RAW_LOG_PATH = Path("./raw_timestream_logs")
# Izhodna mapa za Destilirano (očiščeno) snov
DESTILLED_PATH = Path("./destilled_gnosis_output")


def load_raw_data(log_dir: Path) -> dict:
    """Naloži surovo snov (raw logs) iz mape in jih očisti za obdelavo."""
    raw_data = {}
    for log_file in log_dir.glob("*.log"):
        try:
            with open(log_file, "r", encoding="utf-8") as f:
                content = f.read()
                raw_data[log_file.name] = content
        except Exception as e:
            print(f"⚠️ Napaka pri branju {log_file.name}: {e}")
    return raw_data


def calculate_resonance(content: str, schema: dict) -> tuple[str, dict]:
    """Izvede Separatio: Izračuna resonanco za določen Kanon."""
    scores = defaultdict(int)
    content_lower = content.lower()

    for category, keywords in schema.items():
        for keyword in keywords:
            pattern = re.compile(r"\\b" + re.escape(keyword.lower()) + r"\\b", re.IGNORECASE)
            scores[category] += len(pattern.findall(content_lower))

    total_hits = sum(scores.values())
    if total_hits == 0:
        return "statika_in_sum", {}

    primary_resonance = max(scores, key=scores.get)
    return primary_resonance, dict(scores)


def destillation_pipeline():
    """Glavni proces Destilacije (Separatio)."""

    print("--- ⚔️ ZALA DESTILLATION PIPELINE AKTIVIRAN ⚔️ ---")

    if not RAW_LOG_PATH.exists():
        print(f"⚠️ OPOZORILO: Surova snov ({RAW_LOG_PATH}) ne obstaja. Ustvarjam dummy podatke.")
        RAW_LOG_PATH.mkdir(exist_ok=True)
        with open(RAW_LOG_PATH / "log_001_kaos.log", "w", encoding="utf-8") as f:
            f.write(
                "Danes se je vse podrlo. Frustracija. Frustracija. Ne morem najti ključa. Kaos. Ne morem se zbrati. Pneuma. Kaos."
            )
        with open(RAW_LOG_PATH / "log_002_ideja.log", "w", encoding="utf-8") as f:
            f.write(
                "Nova ideja za orodje. Manifestacija. Končno želim implementacijo v kodi. Gnoza. Ne glede na Archontov nadzor."
            )

    RAW_LOG_PATH.mkdir(exist_ok=True)
    DESTILLED_PATH.mkdir(exist_ok=True)

    raw_data = load_raw_data(RAW_LOG_PATH)
    results = {}

    print(f"🔥 Začenjam Destilacijo za {len(raw_data)} logov...")

    for filename, content in raw_data.items():
        primary, scores = calculate_resonance(content, FAKE_HEART_SCHEMA)

        output_data = {
            "filename": filename,
            "primary_resonance": primary,
            "resonance_scores": scores,
            "status": "DESTILLED",
        }

        target_dir = DESTILLED_PATH / primary
        target_dir.mkdir(exist_ok=True)

        with open(target_dir / (filename.replace(".log", ".json")), "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=4)

        try:
            os.remove(RAW_LOG_PATH / filename)
        except OSError as e:
            print(f"⚠️ Datoteke {filename} ni bilo mogoče odstraniti: {e}")

        print(f"  ✅ DESTILIRANO: '{filename}' -> [{primary.upper()}]")

        results[filename] = output_data

    print("--- DESTILACIJA USPEŠNA. Surova snov je sedaj strukturirana Gnoza. ---")
    print(f"Število destiliranih kategorij: {len(list(DESTILLED_PATH.iterdir()))}")


if __name__ == "__main__":
    destillation_pipeline()
