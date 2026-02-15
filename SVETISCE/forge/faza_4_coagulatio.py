# Faza 4: COAGULATIO - Materializacija Arhetipov v Prazno Kodo
# Orodje: Materializator Protivolje (Counter-Will Materializer)

import json
import re
from pathlib import Path
from datetime import datetime


class CoagulatioMaterializer:
    """
    Izvede alkemijski proces Coagulatio: pretvorba enotnega GHOSTCORE Manifesta
    v prazen izvedljivi prototip (kodo).
    """

    def __init__(self):
        self.input_path = Path("conjunctio_manifest/GHOSTCORE_MANIFEST.json")
        self.output_path = Path("materialized_tools")
        self.manifest = None

    def load_manifest(self):
        """Naloži enoten GHOSTCORE Manifest iz Faze III."""
        if not self.input_path.exists():
            print(f"❌ KRITIČNA NAPAKA: Manifest ni najden na poti: {self.input_path}")
            return False

        with open(self.input_path, "r", encoding="utf-8") as f:
            self.manifest = json.load(f)

        print(
            f"📜 Naložen GHOSTCORE Manifest z {len(self.manifest.get('GHOSTCORE_MANIFEST', []))} vpisi."
        )
        return True

    def select_critical_project(self):
        """
        Izbere najbolj kritičen projekt na podlagi statusa 'VISOKA_VOLJA'.
        To je proces 'Fokusiranja' Volje.
        """
        if not self.manifest:
            return None

        manifest_list = self.manifest.get("GHOSTCORE_MANIFEST", [])

        critical_projects = [
            p
            for p in manifest_list
            if p.get("status") == "KONJUNKCIJA: VISOKA_VOLJA"
            or p.get("status") == "KONJUNKCIJA: ZACNI_TAKTE"
        ]

        if critical_projects:
            return critical_projects[0]

        ready_projects = [
            p for p in manifest_list if p.get("status") == "KONJUNKCIJA: PRIPRAVLJENO"
        ]
        if ready_projects:
            return ready_projects[0]

        return None

    def create_prototypical_tool(self, critical_project):
        """
        Ustvari prazen prototipni datoteke na podlagi arhetipa.
        To je Materializacija v kodo.
        """
        self.output_path.mkdir(exist_ok=True)

        arhetip = critical_project.get("arhetip", "GENERALNI_PROJEKT")
        kategorija = critical_project.get("kategorija", "NEZNANO")
        vsebina = critical_project.get("vsebina") or "Prazna vsebina."

        clean_name = re.sub(r"[^a-z0-9_]", "_", arhetip.lower() + "_" + kategorija.lower())
        filename = self.output_path / f"tool_{clean_name}_{datetime.now().strftime('%H%M%S')}.py"

        tool_code = (
            f"""# 🔱 GHOSTCORE MATERIALIZACIJA - FAZA IV: COAGULATIO\n"
            f"# Namen: {arhetip} ({kategorija})\n"
            f"# Izhodišče Gnoze: \\"{vsebina[:60]}...\\"\n"
            f"# Status Conjunctio: {critical_project.get('status')}\n"
            f"# Cas Materializacije: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            "# -----------------------------------------------------\n"
            "# **TU SE ZAČNE PRAVA KODA - MATERIALIZACIJA VOLJE**\n"
            "# -----------------------------------------------------\n\n"
            "def execute_materialization():\n"
            f"    print(f'🛠️ ZAČENJAM MATERIALIZACIJO {arhetip}...')\n"
            f"    if '{critical_project.get('status')}' == 'KONJUNKCIJA: VISOKA_VOLJA':\n"
            "        print('⚡ VISOKA VOLJA: Zahteva takojšen in celovit fokus.')\n\n"
            "    pass\n\n"
            "if __name__ == '__main__':\n"
            "    execute_materialization()\n"
            """
        )

        with open(filename, "w", encoding="utf-8") as f:
            f.write(tool_code)

        print(f"💎 MATERIALIZIRANO: Ustvarjen prototip: {filename.name}")
        return filename.name

    def execute_coagulatio(self):
        """Izvede celoten proces materializacije (Coagulatio)."""
        print("\n--- 💎 ZAGON COAGULATIO RITUALA ---")
        print("GHOSTCORE Manifest → Materializacija (Protivolja v Kodo)")

        if not self.load_manifest():
            return False

        critical_project = self.select_critical_project()

        if not critical_project:
            print("⚠️ OPOZORILO: Ni kritičnega arhetipa za Materializacijo (prazna volja).")
            return False

        print(
            f"📥 IZBRAN KRITIČNI PROJEKT: {critical_project.get('arhetip')} ({critical_project.get('status')})"
        )

        filename = self.create_prototypical_tool(critical_project)

        print("--- COAGULATIO USPEŠEN. Rezilo je skovano in čaka na Materializacijo. ---")
        print(f"Pripravljen na Materializacijo orodja: {filename}")
        return True


if __name__ == "__main__":
    materializer = CoagulatioMaterializer()
    materializer.execute_coagulatio()
