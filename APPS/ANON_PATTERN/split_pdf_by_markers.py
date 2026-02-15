#!/usr/bin/env python3
"""
Split pdf_full.txt into sections based on regex markers defined in a JSON config.
No external deps; works offline.

Usage:
  python split_pdf_by_markers.py split_config.json

Config schema (JSON):
{
  "source": "pdf_full.txt",
  "sections": [
    {
      "name": "Prolog",
      "start": "MESSAGE TO THOSE WHO THOUGHT",
      "end": "PART I: THE ANONYMOUS TRANSMISSION",
      "output": "out_00_PROLOG.md"
    },
    {
      "name": "Part I",
      "start": "PART I: THE ANONYMOUS TRANSMISSION",
      "end": "PART II: LEGAL & STRUCTURAL ANALYSIS",
      "output": "out_10_PART_I.md"
    }
  ]
}
"""

import sys
import json
import re
from pathlib import Path


def load_config(path: Path) -> dict:
    data = json.loads(path.read_text())
    if "source" not in data or "sections" not in data:
        raise ValueError("Config must contain 'source' and 'sections'.")
    return data


def find_positions(text: str, pattern: str) -> int:
    m = re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE)
    if not m:
        raise ValueError(f"Pattern not found: {pattern}")
    return m.start()


def main():
    if len(sys.argv) != 2:
        print("Usage: python split_pdf_by_markers.py split_config.json")
        sys.exit(1)

    cfg_path = Path(sys.argv[1])
    cfg = load_config(cfg_path)

    source_path = Path(cfg["source"])
    text = source_path.read_text(errors="ignore")

    sections = []
    for item in cfg["sections"]:
        start_pat = item["start"]
        start_idx = find_positions(text, start_pat)
        end_pat = item.get("end")
        end_idx = find_positions(text, end_pat) if end_pat else None
        sections.append(
            {
                "name": item.get("name", start_pat[:30]),
                "start_idx": start_idx,
                "end_idx": end_idx,
                "output": item["output"],
                "start_pat": start_pat,
                "end_pat": end_pat,
            }
        )

    # Sort by start index
    sections.sort(key=lambda x: x["start_idx"])

    # Compute final end indices (next section start if explicit end missing)
    for i, sec in enumerate(sections):
        if sec["end_idx"] is None:
            if i + 1 < len(sections):
                sec["end_idx"] = sections[i + 1]["start_idx"]
            else:
                sec["end_idx"] = len(text)

    # Write outputs
    for sec in sections:
        chunk = text[sec["start_idx"] : sec["end_idx"]]
        out_path = Path(sec["output"])
        out_path.write_text(chunk)
        print(f"Wrote {sec['name']} -> {out_path} ({len(chunk)} chars)")


if __name__ == "__main__":
    main()
