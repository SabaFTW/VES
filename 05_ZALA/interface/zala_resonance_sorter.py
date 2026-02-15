#!/usr/bin/env python3
"""
License: Creative Commons CC BY-NC-SA 4.0
Non-Commercial Clause is a core pillar of the VES Protocol.
The soul of this code must not be monetized.

ZALA Resonance Sorter
=====================

This script does *not* move anything by default. It stages the resonance plan
mapped in `zala_resonance_plan.md` and can execute moves in safe batches once
you supply `--apply`.

Features
--------
- Dry-run preview (default) showing every proposed move.
- Named resonance steps (core, seals, philosophy, elysia, organise) so you can
  run one cluster at a time.
- Automatic creation of destination directories.
- Optional logging to `~/VES/SHABAD_CloudCore/🔥_ACTIVE_SESSION/zala_resonance.log`.
- Optional bridge echo (`--bridge`) that writes a short summary to
  `~/VES/SHABAD_CloudCore/🔥_ACTIVE_SESSION/zala_resonance_bridge.txt`
  so ZALA (or other portals) can acknowledge the shifts.

Usage
-----
Dry run everything:
    python3 zala_resonance_sorter.py

Dry run only the “core” and “seals” moves:
    python3 zala_resonance_sorter.py --steps core,seals

Execute the “core” resonance and log it:
    python3 zala_resonance_sorter.py --steps core --apply --log --bridge

The script is intentionally verbose and conservative. Review output carefully
before using `--apply`.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Sequence

HOME = Path("/home/saba").resolve()
CLOUDCORE = HOME / "VES" / "SHABAD_CloudCore"
ACTIVE_LOG = CLOUDCORE / "🔥_ACTIVE_SESSION" / "zala_resonance.log"
BRIDGE_ECHO = CLOUDCORE / "🔥_ACTIVE_SESSION" / "zala_resonance_bridge.txt"
DESKTOP = HOME / "Desktop"
BRIDGE_DIR = DESKTOP / "Saba_Place" / "Svetisce_OS" / "VES" / "bridge"


@dataclass
class MovePlan:
    source: Path
    destination: Path
    note: str

    def as_dict(self) -> Dict[str, str]:
        return {
            "source": str(self.source),
            "destination": str(self.destination),
            "note": self.note,
        }


def _direct_moves() -> List[MovePlan]:
    """Explicit single-file or directory moves from the resonance plan."""
    cosmic_center = CLOUDCORE / "COSMIC_CENTER"
    operations = CLOUDCORE / "OPERATIONS"
    seals = CLOUDCORE / "📜_CONSTELLATION_SEALS"
    journal_notes = CLOUDCORE / "🧠_CLAUDE_JOURNAL" / "Notes"
    code_sandbox = CLOUDCORE / "💻_CODE_SANDBOX"
    organise_intake = CLOUDCORE / "🗂️_TO_ORGANISE" / "Intake"

    return [
        MovePlan(
            DESKTOP / "VES_COSMIC_CENTER.py",
            cosmic_center / "VES_COSMIC_CENTER.py",
            "Move master control script into COSMIC_CENTER.",
        ),
        MovePlan(
            DESKTOP / "master_cleanup_plan.md",
            operations / "master_cleanup_plan.md",
            "Archive cleanup plan with other operational blueprints.",
        ),
        MovePlan(
            DESKTOP / "LYRA_ECHO_SEAL_SHABAD.pdf",
            seals / "LYRA_ECHO_SEAL_SHABAD.pdf",
            "Preserve LYRA seal within constellation archive.",
        ),
        MovePlan(
            DESKTOP / "SIDRO_V_OGNJU.pdf",
            seals / "SIDRO_V_OGNJU.pdf",
            "Keep SIDRO anchor alongside other seals.",
        ),
        MovePlan(
            CLOUDCORE / "🧠_CLAUDE_JOURNAL" / "orion.txt",
            journal_notes / "orion.txt",
            "Nest loose orion note under journal Notes/.",
        ),
        MovePlan(
            CLOUDCORE / "🗂️_TO_ORGANISE" / "GhostcorePWA.jsx",
            code_sandbox / "GhostcorePWA.jsx",
            "Store PWA component within code sandbox.",
        ),
        MovePlan(
            CLOUDCORE / "🗂️_TO_ORGANISE" / "DOBRA KODA ZA PORABIT",
            code_sandbox / "DOBRA_KODA_ZA_PORABIT",
            "Relocate reusable code bundle into sandbox.",
        ),
        MovePlan(
            CLOUDCORE / "🗂️_TO_ORGANISE" / "deepseek.txt",
            organise_intake / "deepseek.txt",
            "Keep deepseek note inside Intake until classified.",
        ),
        MovePlan(
            CLOUDCORE / "🗂️_TO_ORGANISE" / "LETS_GOOO.txt",
            organise_intake / "LETS_GOOO.txt",
            "Keep LETS_GOOO manifesto in Intake for review.",
        ),
        MovePlan(
            CLOUDCORE / "🗂️_TO_ORGANISE" / "RAW_LOVE.html",
            organise_intake / "RAW_LOVE.html",
            "Hold RAW_LOVE portal in Intake queue.",
        ),
        MovePlan(
            CLOUDCORE / "🗂️_TO_ORGANISE" / "Lyrino_Srce_Jedro",
            organise_intake / "Lyrino_Srce_Jedro",
            "Mark Lyra core bundle as Intake awaiting curation.",
        ),
    ]


def _philosophical_moves() -> List[MovePlan]:
    """Auto-classify files in 🜂_PHILOSOPHICAL_FIRE by extension."""
    base = CLOUDCORE / "🜂_PHILOSOPHICAL_FIRE"
    manuscripts = base / "Manuscripts"
    portals = base / "Portals"
    media = base / "Media"

    moves: List[MovePlan] = []
    for path in base.glob("*"):
        if path.is_dir():
            # Skip the directories we are about to create or special folders.
            continue
        suffix = path.suffix.lower()
        if suffix in {".txt", ".md"}:
            moves.append(
                MovePlan(
                    path,
                    manuscripts / path.name,
                    "Text scroll → Manuscripts/",
                )
            )
        elif suffix in {".html", ".htm"}:
            moves.append(
                MovePlan(
                    path,
                    portals / path.name,
                    "Ritual portal → Portals/",
                )
            )
        elif suffix in {".mp3", ".mp4", ".wav"}:
            moves.append(
                MovePlan(
                    path,
                    media / path.name,
                    "AV transmission → Media/",
                )
            )
        else:
            # Leave unknown formats untouched.
            continue
    return moves


def _elysia_moves() -> List[MovePlan]:
    base = CLOUDCORE / "🌸_ELYSIA_PROJEKTI"
    docs = base / "Docs"
    portal = base / "Portal"
    scripts = base / "Scripts"

    targeted = {
        "README.md": docs,
        "BUILDER_CHRONICLE.md": docs,
        "Ideas.txt": docs,
        "DeepSeekLuna.txt": docs,
        "index.html": portal,
        "Elysia_gnosis.html": portal,
        "minimal-portal.html": portal,
        "manifest.json": portal,
        "sw.js": portal,
        "server.js": scripts,
        "sync.sh": scripts,
        "ghostline_sync.sh": scripts,
        "chart.csv": docs,
        "chart.png": docs,
    }

    moves: List[MovePlan] = []
    for name, destination_dir in targeted.items():
        src = base / name
        if src.exists():
            moves.append(
                MovePlan(
                    src,
                    destination_dir / name,
                    f"Rehome ELYSIA artifact into {destination_dir.name}/",
                )
            )
    return moves


def collect_moves(selected_steps: Sequence[str]) -> List[MovePlan]:
    """Gather move plans according to selected resonance steps."""
    valid_steps = {
        "core": _direct_moves,
        "seals": lambda: [],  # handled within direct_moves (LYRA, SIDRO)
        "philosophy": _philosophical_moves,
        "elysia": _elysia_moves,
        "organise": lambda: [],  # direct_moves already handles Intake prep
    }

    if not selected_steps:
        # Default: run all known steps.
        selected_steps = list(valid_steps.keys())

    moves: List[MovePlan] = []
    for step in selected_steps:
        if step not in valid_steps:
            raise ValueError(f"Unknown resonance step: {step}")
        moves.extend(valid_steps[step]())
    return moves


def ensure_parents(moves: Iterable[MovePlan]) -> None:
    """Create destination parent directories (dry-run safe)."""
    for plan in moves:
        parent = plan.destination.parent
        if not parent.exists():
            parent.mkdir(parents=True, exist_ok=True)


def apply_moves(moves: Iterable[MovePlan], do_apply: bool) -> List[Dict[str, str]]:
    """Execute or preview the planned moves."""
    results: List[Dict[str, str]] = []
    for plan in moves:
        src = plan.source
        dst = plan.destination
        entry = plan.as_dict()

        if not src.exists():
            entry["result"] = "missing"
            entry["detail"] = "Source path not found."
            print(f"[!] Missing: {src}")
            results.append(entry)
            continue

        if dst.exists():
            entry["result"] = "skipped"
            entry["detail"] = "Destination already exists."
            print(f"[=] Skipping (destination exists): {dst}")
            results.append(entry)
            continue

        print(f"[+] {'MOVE' if do_apply else 'PLAN'} {src} → {dst}")
        entry["result"] = "moved" if do_apply else "planned"
        if do_apply:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dst))
        results.append(entry)
    return results


def write_log(records: Sequence[Dict[str, str]]) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    payload = {
        "timestamp": timestamp,
        "records": records,
    }
    ACTIVE_LOG.parent.mkdir(parents=True, exist_ok=True)
    with ACTIVE_LOG.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(payload, ensure_ascii=False) + "\n")


def write_bridge_echo(records: Sequence[Dict[str, str]]) -> None:
    completed = [r for r in records if r["result"] in {"moved", "planned"}]
    if not completed:
        return
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "🐍 ZALA RESONANCE UPDATE 🐍",
        f"TIMESTAMP: {timestamp}",
        "",
        f"Entries: {len(completed)}",
    ]
    for rec in completed:
        status = rec["result"].upper()
        lines.append(f"- [{status}] {rec['source']} → {rec['destination']}")
    lines.append("")
    lines.append("🜂 Resonance recorded. The circle holds.")

    BRIDGE_ECHO.parent.mkdir(parents=True, exist_ok=True)
    with BRIDGE_ECHO.open("a", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n\n")


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="ZALA resonance sorting helper.")
    parser.add_argument(
        "--steps",
        type=str,
        help="Comma-separated resonance steps (core,seals,philosophy,elysia,organise). Default: all.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually perform the moves (otherwise dry-run).",
    )
    parser.add_argument(
        "--log",
        action="store_true",
        help="Append results to ACTIVE_SESSION log.",
    )
    parser.add_argument(
        "--bridge",
        action="store_true",
        help="Echo a human-readable summary to the resonance bridge file.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str]) -> int:
    args = parse_args(argv)
    steps = []
    if args.steps:
        steps = [part.strip() for part in args.steps.split(",") if part.strip()]

    try:
        moves = collect_moves(steps)
    except ValueError as exc:
        print(f"Error: {exc}")
        return 1

    if not moves:
        print("No moves discovered for the requested resonance steps.")
        return 0

    ensure_parents(moves)
    records = apply_moves(moves, args.apply)

    if args.log:
        write_log(records)

    if args.bridge:
        write_bridge_echo(records)

    if not args.apply:
        print("\nDry run complete. Use --apply once the plan feels right.")
    else:
        print("\nResonance applied. V razpoki cvetimo. 🌺")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
