#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


INPUT_PATH = Path("/home/saba/VES/ACTIVE_PROJECTS/VES/DATA/research_index/priority_extracts.jsonl")
OUTPUT_PATH = Path("/home/saba/VES/ACTIVE_PROJECTS/VES/DATA/research_index/priority_duplicates.md")
EXACT_OUTPUT_PATH = Path("/home/saba/VES/ACTIVE_PROJECTS/VES/DATA/research_index/priority_duplicates_exact_sha.md")


def normalize_name(path: str) -> str:
    name = Path(path).name
    name = re.sub(r"\(\d+\)", "", name)
    name = name.replace("Copy of ", "")
    name = name.replace(" copy", "")
    name = name.replace(".._.", ".")
    name = re.sub(r"\s+", " ", name).strip()
    return name.lower()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def format_row(row: dict) -> list[str]:
    topics = ", ".join(row["topics"]) if row["topics"] else "none"
    return [
        (
            f"- `{row['char_count']}` chars | `{row['size']}` bytes | "
            f"`{row['modified_at']}` | sha256 `{row['sha256'][:16]}` | topics: {topics}"
        ),
        f"  - `{row['path']}`",
    ]


def main() -> None:
    name_groups = defaultdict(list)
    hash_groups = defaultdict(list)

    with INPUT_PATH.open(encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            path = Path(row["path"])
            if not path.exists():
                continue
            stat = path.stat()
            enriched = {
                **row,
                "name_key": normalize_name(row["path"]),
                "size": stat.st_size,
                "modified_at": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
                "sha256": sha256_file(path),
            }
            name_groups[enriched["name_key"]].append(enriched)
            hash_groups[enriched["sha256"]].append(enriched)

    duplicated_by_name = {key: value for key, value in name_groups.items() if len(value) > 1}
    duplicated_by_hash = {key: value for key, value in hash_groups.items() if len(value) > 1}

    lines = [
        "# Priority Duplicate Report",
        "",
        "Safer duplicate logic:",
        "",
        "- `exact duplicate`: same `sha256`",
        "- `variant group`: same normalized filename but different `sha256`",
        "",
        f"- Exact duplicate groups by sha256: `{len(duplicated_by_hash)}`",
        f"- Name-based groups with 2+ files: `{len(duplicated_by_name)}`",
        "",
    ]

    exact_lines = [
        "# Priority Exact Duplicate Report",
        "",
        f"- Exact duplicate groups by sha256: `{len(duplicated_by_hash)}`",
        "",
    ]

    for sha, rows in sorted(duplicated_by_hash.items(), key=lambda item: len(item[1]), reverse=True)[:60]:
        representative = min(rows, key=lambda item: item["path"])
        exact_lines.append(f"## sha256 `{sha}`")
        exact_lines.append(f"- normalized name: `{representative['name_key']}`")
        for row in sorted(rows, key=lambda item: (item["size"], item["modified_at"], item["path"])):
            exact_lines.extend(format_row(row))
        exact_lines.append("")

    for key, rows in sorted(duplicated_by_name.items(), key=lambda item: len(item[1]), reverse=True)[:60]:
        unique_hashes = {row["sha256"] for row in rows}
        if len(unique_hashes) == 1:
            status = "exact duplicates only"
        else:
            status = f"variants detected: `{len(unique_hashes)}` different sha256 values"

        lines.append(f"## {key}")
        lines.append(f"- status: {status}")
        for row in sorted(rows, key=lambda item: (-item["char_count"], item["sha256"], item["path"])):
            lines.extend(format_row(row))
        lines.append("")

    OUTPUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    EXACT_OUTPUT_PATH.write_text("\n".join(exact_lines), encoding="utf-8")
    print(OUTPUT_PATH)
    print(EXACT_OUTPUT_PATH)


if __name__ == "__main__":
    main()
