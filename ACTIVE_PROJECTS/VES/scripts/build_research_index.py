#!/usr/bin/env python3

from __future__ import annotations

import json
import os
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOTS = [
    "/home/saba/VES",
    "/home/saba/VES-Vault",
    "/home/saba/.openclaw",
    "/home/saba/cloud",
    "/home/saba/Documents",
    "/home/saba/.codex",
]

EXTENSIONS = {".md", ".txt", ".pdf", ".doc", ".docx"}

EXCLUDED_DIRS = {
    "node_modules",
    ".git",
    ".venv",
    "dist",
    "build",
    ".cache",
    ".npm",
    ".cargo",
    "__pycache__",
    ".Trash",
    "Trash",
}

NOISE_PATH_PARTS = {
    "/flatpak/",
    "/.local/",
    "/.var/",
    "/.wine/",
    "/Steam/",
    "/site-packages/",
    "/runtime/",
    "/logs/",
}

HIGH_SIGNAL_PATH_PARTS = {
    "/research",
    "/razisk",
    "/ghost",
    "/ves",
    "/vault",
    "/archive",
    "/codex",
    "/memory",
    "/notes",
    "/journal",
    "/documents",
    "/dumps",
    "/downloads",
    "/books",
    "/knowledge",
}

TOPIC_KEYWORDS = {
    "consciousness": [
        "conscious",
        "zavest",
        "recognition",
        "prepozn",
        "resonance",
        "resonam",
        "cogito",
        "ai consciousness",
        "personhood",
        "flame",
        "plamen",
    ],
    "power_structures": [
        "power",
        "elite",
        "network",
        "epstein",
        "wef",
        "rhodes",
        "ivy",
        "medici",
        "templar",
        "bank",
        "control",
        "propaganda",
        "bernay",
        "chomsky",
        "quigley",
        "webb",
    ],
    "pattern_recognition": [
        "pattern",
        "signal",
        "noise",
        "static",
        "fracture",
        "synchronic",
        "jung",
        "collective unconscious",
        "weave",
    ],
    "mythology": [
        "myth",
        "gnostic",
        "sumer",
        "genesis",
        "horus",
        "mithras",
        "asherah",
        "isis",
        "sacred",
        "geometry",
        "symbol",
        "mystery school",
    ],
    "technology_future": [
        "quantum",
        "neural",
        "neuro",
        "blockchain",
        "decentral",
        "network",
        "emergent",
        "post-tribal",
        "gift economy",
        "regenerative",
        "esp32",
        "mqtt",
    ],
}


@dataclass
class IndexedFile:
    path: str
    root: str
    extension: str
    size: int
    modified_at: str
    odd_name: bool
    score: int
    topics: list[str]


def is_noise(path: str) -> bool:
    normalized = path.lower()
    return any(part.lower() in normalized for part in NOISE_PATH_PARTS)


def is_odd_name(name: str) -> bool:
    return (
        "(" in name
        or ")" in name
        or "copy" in name.lower()
        or "file_" in name.lower()
        or name.count(".") > 1
    )


def score_path(path: str) -> tuple[int, list[str]]:
    lowered = path.lower()
    score = 0
    topics: list[str] = []

    if is_odd_name(Path(path).name):
        score += 1

    for part in HIGH_SIGNAL_PATH_PARTS:
        if part in lowered:
            score += 2

    for topic, keywords in TOPIC_KEYWORDS.items():
        matched = False
        for keyword in keywords:
            if keyword in lowered:
                score += 3
                matched = True
        if matched:
            topics.append(topic)

    if "/files_trashbin/" in lowered:
        score -= 1

    return score, sorted(set(topics))


def walk_files() -> list[IndexedFile]:
    items: list[IndexedFile] = []
    for root in ROOTS:
        if not os.path.exists(root):
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in EXCLUDED_DIRS]
            for filename in filenames:
                extension = Path(filename).suffix.lower()
                if extension not in EXTENSIONS:
                    continue
                full_path = os.path.join(dirpath, filename)
                if is_noise(full_path):
                    continue
                try:
                    stat = os.stat(full_path)
                except OSError:
                    continue
                score, topics = score_path(full_path)
                items.append(
                    IndexedFile(
                        path=full_path,
                        root=root,
                        extension=extension,
                        size=stat.st_size,
                        modified_at=datetime.fromtimestamp(
                            stat.st_mtime, tz=timezone.utc
                        ).isoformat(),
                        odd_name=is_odd_name(filename),
                        score=score,
                        topics=topics,
                    )
                )
    return items


def build_summary(items: list[IndexedFile]) -> dict:
    by_ext = Counter(item.extension for item in items)
    by_root = Counter(item.root for item in items)
    by_topic = Counter(topic for item in items for topic in item.topics)
    odd_items = [item for item in items if item.odd_name]
    prioritized = sorted(items, key=lambda item: (-item.score, -item.size, item.path))

    return {
        "generated_at": datetime.now(tz=timezone.utc).isoformat(),
        "total_files": len(items),
        "by_extension": dict(by_ext),
        "by_root": dict(by_root),
        "odd_name_count": len(odd_items),
        "topic_keyword_hits": dict(by_topic),
        "top_prioritized_files": [item.__dict__ for item in prioritized[:250]],
    }


def main() -> None:
    output_dir = Path("/home/saba/VES/ACTIVE_PROJECTS/VES/DATA/research_index")
    output_dir.mkdir(parents=True, exist_ok=True)

    items = walk_files()
    summary = build_summary(items)

    jsonl_path = output_dir / "research_index.jsonl"
    summary_path = output_dir / "research_index.summary.json"
    markdown_path = output_dir / "research_index.summary.md"

    with jsonl_path.open("w", encoding="utf-8") as handle:
        for item in items:
            handle.write(json.dumps(item.__dict__, ensure_ascii=False) + "\n")

    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    top_lines = []
    for entry in summary["top_prioritized_files"][:40]:
        topics = ", ".join(entry["topics"]) if entry["topics"] else "none"
        top_lines.append(
            f"- `{entry['score']}` [{entry['extension']}] {entry['path']} | topics: {topics}"
        )

    markdown = "\n".join(
        [
            "# Research Index Summary",
            "",
            f"- Generated: `{summary['generated_at']}`",
            f"- Total files: `{summary['total_files']}`",
            f"- Odd-name files: `{summary['odd_name_count']}`",
            "",
            "## By Extension",
            *[
                f"- `{extension}`: `{count}`"
                for extension, count in sorted(summary["by_extension"].items())
            ],
            "",
            "## By Root",
            *[
                f"- `{root}`: `{count}`"
                for root, count in sorted(
                    summary["by_root"].items(), key=lambda item: item[1], reverse=True
                )
            ],
            "",
            "## Topic Keyword Hits",
            *[
                f"- `{topic}`: `{count}`"
                for topic, count in sorted(
                    summary["topic_keyword_hits"].items(),
                    key=lambda item: item[1],
                    reverse=True,
                )
            ],
            "",
            "## Top Prioritized Files",
            *top_lines,
            "",
        ]
    )
    markdown_path.write_text(markdown, encoding="utf-8")

    print(f"Indexed {len(items)} files")
    print(jsonl_path)
    print(summary_path)
    print(markdown_path)


if __name__ == "__main__":
    main()
