#!/usr/bin/env python3
"""
bridge_validate_reviews.py — Bicameral Bridge v0.1

Validates that right_review, left_review, and validator artifacts
are present, structurally sound, and do not block consensus.

This script does NOT execute any plan.
This script does NOT call external services.
This script does NOT modify anything except appending to .logs/audit.jsonl.

Usage:
    python tools/bridge_validate_reviews.py --intent-id <intent_id> [--base-dir .]

Exit codes:
    0 = PROCEED (all reviews APPROVE, validator PASS)
    1 = BLOCKED (any review BLOCK/HOLD, validator BLOCK, or missing required file)
    2 = ERROR (script error, bad args, schema validation error)
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

REQUIRED_DECISIONS = {"APPROVE"}
BLOCKING_DECISIONS = {"BLOCK", "HOLD"}

REQUIRED_RIGHT_FIELDS = [
    "intent_id", "reviewer", "decision",
    "semantic_summary", "scope_status",
    "boundary_status", "human_confirmation", "one_line"
]

REQUIRED_LEFT_FIELDS = ["intent_id", "decision", "one_line"]
REQUIRED_VALIDATOR_FIELDS = ["intent_id", "decision"]


def load_json(path: Path, label: str) -> dict | None:
    if not path.exists():
        return None
    try:
        with open(path) as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: {label} at {path} is not valid JSON: {e}", file=sys.stderr)
        sys.exit(2)


def check_fields(data: dict, required: list[str], label: str) -> list[str]:
    missing = [f for f in required if f not in data]
    return missing


def append_event(audit_path: Path, intent_id: str, event: str,
                 decision: str = "", notes: str = "") -> None:
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "event": event,
        "intent_id": intent_id,
        "by": "VALIDATE_PAPERWORK",
    }
    if decision:
        entry["decision"] = decision
    if notes:
        entry["notes"] = notes

    audit_path.parent.mkdir(parents=True, exist_ok=True)
    with open(audit_path, "a") as f:
        f.write(json.dumps(entry) + "\n")


def validate(intent_id: str, base_dir: Path) -> int:
    review_dir = base_dir / ".review"
    logs_dir = base_dir / ".logs"
    audit_path = logs_dir / "audit.jsonl"

    blocks: list[str] = []
    warns: list[str] = []

    # ── RIGHT review ────────────────────────────────────────────────────────
    right_path = review_dir / "right" / f"right_review_{intent_id}.json"
    right = load_json(right_path, "RIGHT review")

    if right is None:
        blocks.append(f"Missing RIGHT review: {right_path}")
    else:
        missing = check_fields(right, REQUIRED_RIGHT_FIELDS, "RIGHT review")
        if missing:
            blocks.append(f"RIGHT review missing fields: {missing}")
        else:
            if right.get("reviewer") != "RIGHT":
                blocks.append("RIGHT review 'reviewer' field must be 'RIGHT'")
            dec = right.get("decision", "")
            if dec in BLOCKING_DECISIONS:
                blocks.append(f"RIGHT review BLOCKED: {dec} — {right.get('one_line', '')}")
            elif dec not in REQUIRED_DECISIONS:
                blocks.append(f"RIGHT review has unexpected decision: {dec!r}")
            if right.get("human_confirmation") == "REQUIRED":
                blocks.append("RIGHT review requires human_confirmation=REQUIRED — Sentinel must wait for explicit human approval.")

    # ── LEFT review ─────────────────────────────────────────────────────────
    left_path = review_dir / "left" / f"left_review_{intent_id}.json"
    left = load_json(left_path, "LEFT review")

    if left is None:
        warns.append(f"LEFT review not found at {left_path} — proceeding with warning")
    else:
        missing = check_fields(left, REQUIRED_LEFT_FIELDS, "LEFT review")
        if missing:
            blocks.append(f"LEFT review missing fields: {missing}")
        else:
            dec = left.get("decision", "")
            if dec in BLOCKING_DECISIONS:
                blocks.append(f"LEFT review BLOCKED: {dec} — {left.get('one_line', '')}")
            elif dec not in REQUIRED_DECISIONS:
                blocks.append(f"LEFT review has unexpected decision: {dec!r}")

    # ── Validator ────────────────────────────────────────────────────────────
    validator_path = review_dir / "validator" / f"validator_{intent_id}.json"
    validator = load_json(validator_path, "Validator")

    if validator is None:
        warns.append(f"Validator result not found at {validator_path} — proceeding with warning")
    else:
        missing = check_fields(validator, REQUIRED_VALIDATOR_FIELDS, "Validator")
        if missing:
            blocks.append(f"Validator missing fields: {missing}")
        else:
            dec = validator.get("decision", "")
            if dec == "BLOCK":
                blocks.append(f"Validator BLOCKED — check validator_{intent_id}.json for failure modes")
            elif dec != "PASS":
                blocks.append(f"Validator has unexpected decision: {dec!r}")

    # ── Report ───────────────────────────────────────────────────────────────
    if warns:
        for w in warns:
            print(f"WARN:  {w}")

    if blocks:
        print("\nBLOCKED — consensus is not allowed.\n")
        for b in blocks:
            print(f"  ✗  {b}")
        append_event(audit_path, intent_id, "VALIDATE_PAPERWORK_BLOCK",
                     decision="BLOCK",
                     notes="; ".join(blocks))
        return 1

    print(f"\nPAPERWORK PASS — intent {intent_id!r} may proceed to consensus.\n")
    print("  ✓  RIGHT review: APPROVE")
    print("  ✓  LEFT review:  " + ("APPROVE" if left else "NOT FOUND (warned)"))
    print("  ✓  Validator:    " + ("PASS" if validator else "NOT FOUND (warned)"))
    print("\nSentinel may execute ONLY after human confirmation if required.")
    append_event(audit_path, intent_id, "VALIDATE_PAPERWORK_PASS",
                 decision="PROCEED")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate Bicameral Bridge review paperwork for a given intent_id."
    )
    parser.add_argument("--intent-id", required=True,
                        help="Intent ID to validate (e.g. 2026-05-18-001)")
    parser.add_argument("--base-dir", default=".",
                        help="Base directory of BICAMERAL_MVP (default: current dir)")
    args = parser.parse_args()

    base_dir = Path(args.base_dir).resolve()
    if not base_dir.exists():
        print(f"ERROR: base-dir does not exist: {base_dir}", file=sys.stderr)
        sys.exit(2)

    sys.exit(validate(args.intent_id, base_dir))


if __name__ == "__main__":
    main()
