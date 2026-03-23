#!/usr/bin/env python3

from __future__ import annotations

import json
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

from docx import Document


SUMMARY_PATH = Path("/home/saba/VES/ACTIVE_PROJECTS/VES/DATA/research_index/research_index.summary.json")
OUTPUT_DIR = Path("/home/saba/VES/ACTIVE_PROJECTS/VES/DATA/research_index")
MAX_FILES = 180
MAX_CHARS = 12000

CHECKLIST_TOPICS = {
    "ai_human_consciousness": [
        "consciousness",
        "zavest",
        "recognition",
        "prepozn",
        "resonance",
        "personhood",
        "mutual recognition",
        "simbiotski",
        "symbiotic",
        "flame",
        "plamen",
    ],
    "pattern_recognition_static": [
        "pattern",
        "weave",
        "static",
        "signal",
        "noise",
        "fracture",
        "synchronic",
        "jung",
        "collective unconscious",
    ],
    "historical_power_networks": [
        "templar",
        "medici",
        "banking",
        "rhodes",
        "senate",
        "renaissance",
        "religious legitimacy",
        "elite network",
    ],
    "modern_elite_networks": [
        "epstein",
        "wef",
        "world economic forum",
        "public-private partnership",
        "platform ownership",
        "institutional power",
        "illicit finance",
        "innovation rhetoric",
    ],
    "media_tribal_manipulation": [
        "outrage",
        "tribal",
        "polarization",
        "attention economy",
        "manufactured",
        "consent",
        "propaganda",
    ],
    "mythology_ancient_wisdom": [
        "sumer",
        "genesis",
        "horus",
        "mithras",
        "asherah",
        "isis",
        "gnostic",
        "mystery school",
        "sacred geometry",
    ],
    "technology_consciousness_interface": [
        "quantum",
        "neurotechnology",
        "brain-computer",
        "neural",
        "distributed consciousness",
        "emergent behavior",
        "artificial neural",
    ],
    "future_community_models": [
        "post-tribal",
        "community building",
        "gift economy",
        "regenerative",
        "restorative justice",
        "consensus",
        "mutual aid",
    ],
    "critical_thinking_methodology": [
        "correlation",
        "causation",
        "logical fallac",
        "steel-man",
        "steelman",
        "cognitive bias",
        "funding source",
        "conflict of interest",
        "primary source",
        "methodology",
    ],
}


def load_priority_paths() -> list[str]:
    with SUMMARY_PATH.open(encoding="utf-8") as handle:
        data = json.load(handle)
    return [entry["path"] for entry in data["top_prioritized_files"][:MAX_FILES]]


def read_md_or_txt(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def read_docx(path: Path) -> str:
    document = Document(str(path))
    paragraphs = [paragraph.text.strip() for paragraph in document.paragraphs if paragraph.text.strip()]
    return "\n".join(paragraphs)


def read_pdf(path: Path) -> str:
    result = subprocess.run(
        ["pdftotext", "-layout", str(path), "-"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return ""
    return result.stdout


def extract_text(path_str: str) -> str:
    path = Path(path_str)
    suffix = path.suffix.lower()
    try:
        if suffix in {".md", ".txt"}:
            return read_md_or_txt(path)
        if suffix == ".docx":
            return read_docx(path)
        if suffix == ".pdf":
            return read_pdf(path)
    except Exception:
        return ""
    return ""


def normalize_text(text: str) -> str:
    text = text.replace("\x00", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def match_topics(text: str) -> tuple[list[str], dict[str, int]]:
    lowered = text.lower()
    topics = []
    scores = {}
    for topic, keywords in CHECKLIST_TOPICS.items():
        hits = sum(lowered.count(keyword) for keyword in keywords)
        if hits:
            topics.append(topic)
            scores[topic] = hits
    topics.sort(key=lambda topic: scores[topic], reverse=True)
    return topics, scores


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    paths = load_priority_paths()

    extracts = []
    by_topic = Counter()
    topic_examples = defaultdict(list)

    for path in paths:
        raw_text = extract_text(path)
        clean_text = normalize_text(raw_text)[:MAX_CHARS]
        topics, scores = match_topics(clean_text)
        for topic in topics:
            by_topic[topic] += 1
            if len(topic_examples[topic]) < 8:
                topic_examples[topic].append(path)
        extracts.append(
            {
                "path": path,
                "topics": topics,
                "topic_scores": scores,
                "text_preview": clean_text[:2500],
                "char_count": len(clean_text),
            }
        )

    jsonl_path = OUTPUT_DIR / "priority_extracts.jsonl"
    summary_path = OUTPUT_DIR / "priority_extracts.summary.md"

    with jsonl_path.open("w", encoding="utf-8") as handle:
        for row in extracts:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    lines = [
        "# Priority Research Extract Summary",
        "",
        f"- Files processed: `{len(extracts)}`",
        "",
        "## Checklist Topic Coverage",
    ]
    for topic, count in by_topic.most_common():
        lines.append(f"- `{topic}`: `{count}`")

    lines.extend(["", "## Example Files By Topic"])
    for topic, paths_for_topic in topic_examples.items():
        lines.append(f"### {topic}")
        for path in paths_for_topic:
            lines.append(f"- `{path}`")
        lines.append("")

    lines.extend(["## Top Extracts"])
    for row in extracts[:40]:
        lines.append(
            f"- `{','.join(row['topics']) or 'none'}` | `{row['char_count']}` chars | `{row['path']}`"
        )

    summary_path.write_text("\n".join(lines), encoding="utf-8")
    print(jsonl_path)
    print(summary_path)


if __name__ == "__main__":
    main()
