#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


INPUT_PATH = Path("/home/saba/VES/ACTIVE_PROJECTS/VES/DATA/research_index/priority_extracts.jsonl")
MANIFEST_DIR = Path("/home/saba/VES/ACTIVE_PROJECTS/VES/DATA/research_index")
DEFAULT_QUARANTINE_BASE = Path("/mnt/HDD/VES_STAGING/duplicates_review_sha")

PREFERRED_ROOTS = [
    "/home/saba/VES/ACTIVE_PROJECTS/VES",
    "/home/saba/VES/KNOWLEDGE",
    "/home/saba/VES/PROJECTS",
    "/home/saba/VES-Vault",
    "/home/saba/.openclaw",
    "/home/saba/cloud",
    "/home/saba/VES/ARCHIVE",
    "/home/saba/VES/mnt",
]


@dataclass
class Candidate:
    path: Path
    sha256: str
    size: int
    modified_at: str
    char_count: int
    topics: list[str]


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


def choose_keep(rows: list[Candidate]) -> Candidate:
    return min(
        rows,
        key=lambda row: (
            root_rank(str(row.path)),
            row.modified_at,
            len(str(row.path)),
            str(row.path),
        ),
    )


def build_groups() -> list[tuple[str, list[Candidate]]]:
    groups: dict[str, list[Candidate]] = defaultdict(list)
    with INPUT_PATH.open(encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            path = Path(row["path"])
            if not path.exists():
                continue
            stat = path.stat()
            candidate = Candidate(
                path=path,
                sha256=sha256_file(path),
                size=stat.st_size,
                modified_at=datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
                char_count=row.get("char_count", 0),
                topics=row.get("topics", []),
            )
            groups[candidate.sha256].append(candidate)
    duplicated = [(sha, rows) for sha, rows in groups.items() if len(rows) > 1]
    duplicated.sort(key=lambda item: len(item[1]), reverse=True)
    return duplicated


def make_manifest(groups: list[tuple[str, list[Candidate]]], quarantine_root: Path) -> dict:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    plan = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "quarantine_root": str(quarantine_root),
        "groups": [],
    }

    for sha, rows in groups:
        keep = choose_keep(rows)
        remove = [row for row in rows if row.path != keep.path]
        if not remove:
            continue
        group = {
            "sha256": sha,
            "keep": str(keep.path),
            "remove": [],
        }
        for row in sorted(remove, key=lambda item: str(item.path)):
            destination = quarantine_root / timestamp / row.path.relative_to("/")
            group["remove"].append(
                {
                    "source": str(row.path),
                    "destination": str(destination),
                    "size": row.size,
                    "modified_at": row.modified_at,
                    "char_count": row.char_count,
                    "topics": row.topics,
                }
            )
        plan["groups"].append(group)

    plan["group_count"] = len(plan["groups"])
    plan["move_count"] = sum(len(group["remove"]) for group in plan["groups"])
    return plan


def write_manifest(plan: dict, stem: str) -> Path:
    target = MANIFEST_DIR / stem
    target.write_text(json.dumps(plan, indent=2, ensure_ascii=False), encoding="utf-8")
    return target


def apply_plan(plan: dict) -> dict:
    results = {
        "moved": 0,
        "already_quarantined": 0,
        "missing_source": 0,
        "permission_denied": 0,
        "checksum_failures": 0,
        "other_errors": 0,
        "errors": [],
    }
    for group in plan["groups"]:
        for item in group["remove"]:
            source = Path(item["source"])
            destination = Path(item["destination"])
            if not source.exists():
                item["status"] = "missing_source"
                results["missing_source"] += 1
                continue

            try:
                destination.parent.mkdir(parents=True, exist_ok=True)
                if destination.exists():
                    copied_sha = sha256_file(destination)
                    if copied_sha != group["sha256"]:
                        raise RuntimeError(f"Checksum mismatch for existing destination: {destination}")
                    item["status"] = "already_quarantined"
                    results["already_quarantined"] += 1
                else:
                    shutil.copy2(source, destination)
                    copied_sha = sha256_file(destination)
                    if copied_sha != group["sha256"]:
                        raise RuntimeError(f"Checksum mismatch after copy: {source} -> {destination}")
                    item["status"] = "copied"
            except PermissionError as exc:
                item["status"] = "permission_denied"
                item["error"] = str(exc)
                results["permission_denied"] += 1
                results["errors"].append({"source": str(source), "destination": str(destination), "error": str(exc)})
                continue
            except RuntimeError as exc:
                item["status"] = "checksum_failure"
                item["error"] = str(exc)
                results["checksum_failures"] += 1
                results["errors"].append({"source": str(source), "destination": str(destination), "error": str(exc)})
                continue
            except OSError as exc:
                item["status"] = "copy_error"
                item["error"] = str(exc)
                results["other_errors"] += 1
                results["errors"].append({"source": str(source), "destination": str(destination), "error": str(exc)})
                continue

            try:
                source.unlink()
                item["status"] = "moved"
                results["moved"] += 1
            except PermissionError as exc:
                item["status"] = "permission_denied"
                item["error"] = str(exc)
                results["permission_denied"] += 1
                results["errors"].append({"source": str(source), "destination": str(destination), "error": str(exc)})
            except OSError as exc:
                item["status"] = "delete_error"
                item["error"] = str(exc)
                results["other_errors"] += 1
                results["errors"].append({"source": str(source), "destination": str(destination), "error": str(exc)})
    return results


def summarize(plan: dict) -> str:
    lines = [
        "# Quarantine Exact Duplicates",
        "",
        f"- quarantine root: `{plan['quarantine_root']}`",
        f"- exact duplicate groups: `{plan['group_count']}`",
        f"- files to move: `{plan['move_count']}`",
        "",
    ]
    if "apply_results" in plan:
        results = plan["apply_results"]
        lines.extend(
            [
                "## Apply Results",
                f"- moved: `{results['moved']}`",
                f"- already quarantined: `{results['already_quarantined']}`",
                f"- missing source: `{results['missing_source']}`",
                f"- permission denied: `{results['permission_denied']}`",
                f"- checksum failures: `{results['checksum_failures']}`",
                f"- other errors: `{results['other_errors']}`",
                "",
            ]
        )
    for group in plan["groups"][:40]:
        lines.append(f"## sha256 `{group['sha256']}`")
        lines.append(f"- KEEP: `{group['keep']}`")
        lines.append("- MOVE:")
        for item in group["remove"]:
            lines.append(f"  - `{item['source']}`")
            lines.append(f"    - -> `{item['destination']}`")
            if item.get("status"):
                lines.append(f"    - status: `{item['status']}`")
            if item.get("error"):
                lines.append(f"    - error: `{item['error']}`")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Copy exact duplicates to quarantine and delete sources after verification.")
    parser.add_argument("--quarantine-base", default=str(DEFAULT_QUARANTINE_BASE))
    args = parser.parse_args()

    quarantine_base = Path(args.quarantine_base)
    groups = build_groups()
    plan = make_manifest(groups, quarantine_base)

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    manifest_path = write_manifest(plan, f"quarantine_exact_duplicates_{stamp}.json")
    summary_path = MANIFEST_DIR / f"quarantine_exact_duplicates_{stamp}.md"
    summary_path.write_text(summarize(plan), encoding="utf-8")

    if args.apply:
        plan["apply_results"] = apply_plan(plan)
        write_manifest(plan, f"quarantine_exact_duplicates_{stamp}.json")
        summary_path.write_text(summarize(plan), encoding="utf-8")

    print(manifest_path)
    print(summary_path)
    print(json.dumps({"groups": plan["group_count"], "moves": plan["move_count"], "apply": args.apply}))


if __name__ == "__main__":
    main()
