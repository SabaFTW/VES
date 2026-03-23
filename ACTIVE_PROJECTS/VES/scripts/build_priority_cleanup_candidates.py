#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


INPUT_PATH = Path("/home/saba/VES/ACTIVE_PROJECTS/VES/DATA/research_index/priority_extracts.jsonl")
OUTPUT_PATH = Path("/home/saba/VES/ACTIVE_PROJECTS/VES/DATA/research_index/priority_duplicate_cleanup_candidates.md")

PREFERRED_ROOTS = [
    "/home/saba/VES/KNOWLEDGE",
    "/home/saba/VES/ACTIVE_PROJECTS",
    "/home/saba/VES/PROJECTS",
    "/home/saba/VES-Vault",
    "/home/saba/.openclaw",
    "/home/saba/cloud",
    "/home/saba/VES/ARCHIVE",
    "/home/saba/VES/mnt",
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def root_rank(path: str) -> int:
    for idx, root in enumerate(PREFERRED_ROOTS):
        if path.startswith(root):
            return idx
    return len(PREFERRED_ROOTS)


def choose_keep(rows: list[dict]) -> dict:
    return min(
        rows,
        key=lambda row: (
            root_rank(row["path"]),
            row["modified_at"],
            len(row["path"]),
            row["path"],
        ),
    )


def main() -> None:
    hash_groups = defaultdict(list)

    with INPUT_PATH.open(encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            path = Path(row["path"])
            if not path.exists():
                continue
            stat = path.stat()
            hash_groups[sha256_file(path)].append(
                {
                    **row,
                    "size": stat.st_size,
                    "modified_at": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
                }
            )

    exact_groups = [rows for rows in hash_groups.values() if len(rows) > 1]
    exact_groups.sort(key=len, reverse=True)

    lines = [
        "# Priority Duplicate Cleanup Candidates",
        "",
        "Only exact binary duplicates are included here.",
        "",
        "Heuristic for `KEEP`:",
        "- prefer `VES/KNOWLEDGE`",
        "- then `VES/ACTIVE_PROJECTS`",
        "- then `VES/PROJECTS`",
        "- then `VES-Vault`",
        "- then `.openclaw`",
        "- then `cloud`",
        "- then `VES/ARCHIVE`",
        "- then `VES/mnt`",
        "",
        f"- Exact duplicate groups considered: `{len(exact_groups)}`",
        "",
    ]

    for rows in exact_groups[:60]:
        keep = choose_keep(rows)
        lines.append(f"## sha256 `{sha256_file(Path(keep['path']))}`")
        lines.append(f"- KEEP: `{keep['path']}`")
        lines.append(f"- modified: `{keep['modified_at']}` | size: `{keep['size']}`")
        lines.append("- REMOVE candidates:")
        for row in sorted(rows, key=lambda item: (item["path"] != keep["path"], item["path"])):
            if row["path"] == keep["path"]:
                continue
            lines.append(f"  - `{row['path']}`")
            lines.append(f"    - modified: `{row['modified_at']}` | size: `{row['size']}`")
        lines.append("")

    OUTPUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(OUTPUT_PATH)


if __name__ == "__main__":
    main()
