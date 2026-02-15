#!/usr/bin/env python3
"""Faza II: Ignition Ritual (Terminal Sanctum)

1. Zabeleži namen in cilj.
2. Zažene 25-minutni pulse fokus.
3. Po pulsu zbere refleksijo in shrani rezultat.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List

try:
    import getpass
except ImportError:  # pragma: no cover
    getpass = None

OUTPUT_DIR = Path("destilled_gnosis_output/ignitions")
DEFAULT_PULSE_MINUTES = 25
COOLDOWN_MINUTES = 5


class IgnitionSession:
    def __init__(self, dry_run: bool = False, pulse_minutes: int = DEFAULT_PULSE_MINUTES):
        self.dry_run = dry_run
        self.pulse_minutes = pulse_minutes
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.data: Dict[str, object] = {
            "session_id": self.session_id,
            "timestamp": datetime.now().isoformat(),
            "user": getpass.getuser() if getpass else "unknown",
            "dry_run": dry_run,
            "pulse_minutes": pulse_minutes,
            "purpose": "",
            "target": "",
            "tasks": [],
            "reflection": "",
        }

    def prompt_metadata(self) -> None:
        print("\n--- ⚔️ IGNITION: PRIPRAVA NAMENA ---")
        self.data["purpose"] = input("💡 Namen (1 stavek): ").strip()
        self.data["target"] = input("🎯 Glavni cilj (repo/projekt): ").strip()
        print("\n📝 Navedi 3 mikro-naloge (pritisni Enter po vsaki):")
        tasks: List[str] = []
        for i in range(1, 4):
            tasks.append(input(f"  [{i}] ").strip())
        self.data["tasks"] = tasks

    def confirm_and_start(self) -> None:
        print("\n--- POTRDITEV IGNITION ---")
        print(f"Namen: {self.data['purpose']}")
        print(f"Cilj: {self.data['target']}")
        print("Naloge:")
        for idx, task in enumerate(self.data["tasks"], start=1):
            print(f"  {idx}. {task}")
        if self.dry_run:
            print("\n⚠️ DRY-RUN: rezultati NE bodo shranjeni.")
        input("\nPritisni Enter za začetek 25-minutnega pulsa...")

    def run_pulse(self) -> None:
        print("\n🔥 Pulse se začenja. 25 minut fokus. Predlagam, da ekran minimaliziraš.")
        end_time = datetime.now() + timedelta(minutes=self.pulse_minutes)
        try:
            while datetime.now() < end_time:
                remaining = end_time - datetime.now()
                minutes, seconds = divmod(int(remaining.total_seconds()), 60)
                print(f"  ⏳ Preostalo: {minutes:02d}:{seconds:02d}", end="\r")
                time.sleep(1)
            print("\n\n✅ Pulse končan. Pohod skozi ogenj uspešen.")
        except KeyboardInterrupt:
            print("\n❌ Pulse prekinjen z emergency stop. Zapis bo označen kot 'ABORTED'.")
            self.data["status"] = "ABORTED"
            raise

    def cooldown_and_reflect(self) -> None:
        print("\n--- 🧊 COOLDOWN (5 min) ---")
        cooldown_end = datetime.now() + timedelta(minutes=COOLDOWN_MINUTES)
        try:
            while datetime.now() < cooldown_end:
                remaining = cooldown_end - datetime.now()
                minutes, seconds = divmod(int(remaining.total_seconds()), 60)
                print(f"  🫧 Cooldown preostalo: {minutes:02d}:{seconds:02d}", end="\r")
                time.sleep(1)
            print("\nCooldown zaključen.")
        except KeyboardInterrupt:
            print("\n⚠️ Cooldown preklican. Nadaljujem s refleksijo.")

        print("\n--- 🪞 REFLEKSIJA ---")
        reflection = input("Kaj si dosegel? Kako se počutiš? ").strip()
        self.data["reflection"] = reflection
        self.data.setdefault("status", "COMPLETED")

    def persist(self) -> None:
        if self.dry_run:
            print("\n💾 DRY-RUN: Rezultat ni bil shranjen.")
            return
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        outfile = OUTPUT_DIR / f"ignition_{self.session_id}.json"
        with open(outfile, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        try:
            os.chmod(outfile, 0o600)
        except OSError:
            pass
        print(f"\n💾 Rezultat shranjen: {outfile}")


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Ignition Pulse ritual")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Ne shranim rezultatov (testni zagon).",
    )
    parser.add_argument(
        "--minutes",
        type=int,
        default=DEFAULT_PULSE_MINUTES,
        help="Dolžina pulsa v minutah (privzeto 25).",
    )
    args = parser.parse_args(argv)

    session = IgnitionSession(dry_run=args.dry_run, pulse_minutes=args.minutes)

    try:
        session.prompt_metadata()
        session.confirm_and_start()
        session.run_pulse()
    except KeyboardInterrupt:
        session.data.setdefault("status", "ABORTED")
        session.persist()
        print("\n⚠️ IGNITION STOP: Session aborted.")
        return 1

    try:
        session.cooldown_and_reflect()
    except KeyboardInterrupt:
        session.data.setdefault("status", "COOLDOWN_ABORTED")

    session.persist()
    print("\n🛡️ Ignition zaključen. Skrbi zase. Limit: ≤ 3 pulsi / dan.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
