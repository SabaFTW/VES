# Faza 3: CONJUNCTIO - Združitev Arhetipov v GHOSTCORE Manifest
# Orodje: Združevalnik Resonanc (Resonance Unifier)

import json
from pathlib import Path
from datetime import datetime


class ConjunctioUnifier:
    """
    Izvede alkemijski proces Conjunctio: združitev vseh arhetipov
    v en sam, prioritetni GHOSTCORE Manifest.
    """

    def __init__(self):
        self.input_path = Path("transformed_archetypes")
        self.output_path = Path("conjunctio_manifest")
        self.final_manifest = []
        self.manifest_meta = {
            "cas_zdruzitve": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "proces": "Conjunctio (Združitev Arhetipov)",
            "izvor": "Transmutirani Arhetipi iz Faze II",
            "stevilo_zdruzenih_vnosov": 0,
        }

    def load_archetypes(self):
        """Naloži vse JSON datoteke z arhetipi iz Faze II."""
        archetype_files = list(self.input_path.glob("*.json"))
        print(f"🔍 Najdenih {len(archetype_files)} arhetip datotek za združitev.")

        all_archetypes = []
        for file in archetype_files:
            try:
                with open(file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                if "arhetipi" in data and isinstance(data["arhetipi"], list):
                    category = data.get("meta", {}).get("kategorija", file.stem.split("_")[1].upper())

                    for item in data["arhetipi"]:
                        item["kategorija"] = category
                        if item.get("prioriteta") == "VISOKA" or item.get("kompleksnost") == "VISOKA":
                            item["status"] = "KONJUNKCIJA: VISOKA_VOLJA"
                        elif item.get("arhetip") == "AKCIJA":
                            item["status"] = "KONJUNKCIJA: ZACNI_TAKTE"
                        else:
                            item["status"] = "KONJUNKCIJA: PRIPRAVLJENO"

                        all_archetypes.append(item)

            except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"❌ Napaka pri nalaganju datoteke {file}: {e}")

        self.manifest_meta["stevilo_zdruzenih_vnosov"] = len(all_archetypes)
        return all_archetypes

    def save_ghostcore_manifest(self, manifest_data):
        """Shrani združen manifest v izhodno mapo."""
        if not manifest_data:
            print("⚠️ OPOZORILO: Manifest je prazen. Nič za shraniti.")
            return False

        self.output_path.mkdir(exist_ok=True)
        filename = self.output_path / "GHOSTCORE_MANIFEST.json"

        final_output = {
            "GHOSTCORE_META": self.manifest_meta,
            "GHOSTCORE_MANIFEST": manifest_data,
        }

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(final_output, f, ensure_ascii=False, indent=2)

        print(
            f"📜 USPEŠNO: Ustvarjen enoten GHOSTCORE MANIFEST ({filename.name}) z {len(manifest_data)} vpisi."
        )
        return True

    def execute_conjunctio(self):
        """Izvede celoten proces združitve (Conjunctio)."""
        print("\n--- 🔱 ZAGON CONJUNCTIO RITUALA ---")
        print("Arhetipi → GHOSTCORE Manifest (Enotna Direktiva)")

        all_archetypes = self.load_archetypes()

        if not all_archetypes:
            print("⚠️ OPOZORILO: Ni naloženih arhetipov za združitev.")
            return False

        print(f"📥 Naloženih skupaj {len(all_archetypes)} arhetipov.")

        success = self.save_ghostcore_manifest(all_archetypes)

        if success:
            print("--- CONJUNCTIO USPEŠEN. Enotna volja je zapisana. ---")
            print("Pripravljen na Fazo IV (Coagulatio) – Materializacijo.")
            return True

        print("❌ CONJUNCTIO NEUSPEŠEN - preveri vhodne datoteke.")
        return False


if __name__ == "__main__":
    unifier = ConjunctioUnifier()
    unifier.execute_conjunctio()
