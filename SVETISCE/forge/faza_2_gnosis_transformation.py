# Faza 2: TRANSFORMATIO GNOSIS → ARHETIPI
# Orodje: Alkemijska Preobrazba (Transmutatio)

import json
from pathlib import Path
from datetime import datetime


class GnosisTransmutator:
    def __init__(self):
        self.input_path = Path("destilled_gnosis_output/statika_in_sum")
        self.output_path = Path("transformed_archetypes")

    def load_destilled_gnosis(self):
        """Naloži destilirano gnozo iz Faze I."""
        gnosis_files = list(self.input_path.glob("*.json"))
        print(f"🔍 Najdenih {len(gnosis_files)} destiliranih gnoz datotek")

        all_entries = []
        for file in gnosis_files:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    all_entries.extend(data)
                else:
                    all_entries.append(data)
        return all_entries

    def transmute_to_archetypes(self, gnosis_entries):
        """Transformiraj gnozo v praktične arhetipe."""
        archetypes = {
            "PROJEKTI": [],
            "AKCIJE": [],
            "IDEJE": [],
            "SISTEMI": [],
        }

        for entry in gnosis_entries:
            content = (entry.get("content") or "").lower()

            if any(word in content for word in ["naredi", "zagon", "build", "create"]):
                archetypes["AKCIJE"].append(
                    {
                        "arhetip": "AKCIJA",
                        "vsebina": entry.get("content"),
                        "vir": entry.get("id"),
                        "prioriteta": "VISOKA" if "hitro" in content else "SREDNJA",
                    }
                )
            elif any(word in content for word in ["sistem", "organiziraj", "structure"]):
                archetypes["SISTEMI"].append(
                    {
                        "arhetip": "SISTEM",
                        "vsebina": entry.get("content"),
                        "kompleksnost": "VISOKA" if "kompleks" in content else "OSNOVNA",
                    }
                )
            elif any(word in content for word in ["projekt", "idea", "koncept"]):
                archetypes["PROJEKTI"].append(
                    {
                        "arhetip": "PROJEKT",
                        "vsebina": entry.get("content"),
                        "faza": "ZAČETNA" if "nov" in content else "RAZVOJ",
                    }
                )
            else:
                archetypes["IDEJE"].append(
                    {
                        "arhetip": "IDEJA",
                        "vsebina": entry.get("content"),
                        "kategorija": "INSPIRACIJA",
                    }
                )

        return archetypes

    def save_archetypes(self, archetypes):
        """Shrani transformirane arhetipe."""
        self.output_path.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        categories_written = 0

        for category, items in archetypes.items():
            if items:
                categories_written += 1
                filename = self.output_path / f"archetypes_{category.lower()}_{timestamp}.json"
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(
                        {
                            "meta": {
                                "proces": "Transmutatio Gnosis",
                                "kategorija": category,
                                "cas_transformacije": timestamp,
                                "stevilo_elementov": len(items),
                            },
                            "arhetipi": items,
                        },
                        f,
                        ensure_ascii=False,
                        indent=2,
                    )

        print(f"🎭 USPEŠNO: Ustvarjenih {categories_written} kategorij arhetipov")
        return categories_written

    def execute_transmutatio(self):
        """Izvedi celoten proces transformacije."""
        print("\n--- 🜂 ZAGON TRANSFORMATIO PROCESS ---")
        print("Gnoza → Arhetipi")

        if not self.input_path.exists():
            print("⚠️ OPOZORILO: Ni destilirane gnoze za transformacijo.")
            return False

        gnosis_entries = self.load_destilled_gnosis()
        if not gnosis_entries:
            print("⚠️ OPOZORILO: Destilirane gnoze ni bilo mogoče naložiti.")
            return False

        print(f"📥 Naloženih {len(gnosis_entries)} destiliranih vnosov")

        archetypes = self.transmute_to_archetypes(gnosis_entries)
        saved_categories = self.save_archetypes(archetypes)

        if saved_categories:
            print("--- TRANSFORMATIO USPEŠEN. Gnoza je sedaj praktični arhetip. ---")
            return True

        print("⚠️ TRANSFORMATIO izveden, vendar ni bilo mogoče ustvariti arhetipov.")
        return False


if __name__ == "__main__":
    transmutator = GnosisTransmutator()
    if transmutator.execute_transmutatio():
        print("\n🎯 FAZA II ZAKLJUČENA - pripravljen za Fazo III (Conjunctio)")
    else:
        print("\n❌ TRANSFORMATIO NEUSPEŠEN - preveri vhodne podatke")
