#!/usr/bin/env python3
"""
sentinel_dry_run.py — Bicameral Kernel C-phase

Shows what Sentinel WOULD do for a given intent_id, without applying
any changes. Reads paperwork, validates allowed_paths boundaries, reports
planned actions. Appends dry-run event to .logs/audit.jsonl (local runtime).

This script:
  - does NOT copy, edit, or delete any file
  - does NOT run any command from the plan
  - does NOT start or restart any service
  - does NOT call external APIs or models

Exit codes:
    0 = DRY-RUN ALLOWED  — paperwork valid, plan within boundary
    1 = DRY-RUN BLOCKED  — paperwork blocked or boundary violation
    2 = ERROR            — bad args, missing required files, JSON error
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

BLOCKING_DECISIONS = {"BLOCK", "HOLD"}
REQUIRED_RIGHT_FIELDS = [
    "intent_id", "reviewer", "decision",
    "semantic_summary", "scope_status",
    "boundary_status", "human_confirmation", "one_line",
]


# ── Helpers ────────────────────────────────────────────────────────────────────

def _load_json(path: Path, label: str) -> dict:
    if not path.exists():
        print(f"ERROR: {label} not found: {path}", file=sys.stderr)
        sys.exit(2)
    try:
        with open(path) as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: {label} is not valid JSON: {e}", file=sys.stderr)
        sys.exit(2)


def _load_optional_json(path: Path) -> dict | None:
    if not path.exists():
        return None
    try:
        with open(path) as f:
            return json.load(f)
    except json.JSONDecodeError:
        return None


def _append_audit(audit_path: Path, intent_id: str, event: str,
                  decision: str = "", notes: str = "") -> None:
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "event": event,
        "intent_id": intent_id,
        "by": "SENTINEL_DRY_RUN",
    }
    if decision:
        entry["decision"] = decision
    if notes:
        entry["notes"] = notes
    audit_path.parent.mkdir(parents=True, exist_ok=True)
    with open(audit_path, "a") as f:
        f.write(json.dumps(entry) + "\n")


def _within_allowed(target: str, allowed_paths: list[str]) -> bool:
    return any(target.startswith(p) for p in allowed_paths)


# ── Paperwork validation (mirrors bridge_validate_reviews logic) ───────────────

def _check_paperwork(base_dir: Path, intent_id: str) -> tuple[list[str], list[str]]:
    review_dir = base_dir / ".review"
    blocks: list[str] = []
    warns: list[str] = []

    # RIGHT review (required)
    right_path = review_dir / "right" / f"right_review_{intent_id}.json"
    right = _load_optional_json(right_path)
    if right is None:
        blocks.append(f"Missing RIGHT review: {right_path}")
    else:
        missing = [f for f in REQUIRED_RIGHT_FIELDS if f not in right]
        if missing:
            blocks.append(f"RIGHT review missing fields: {missing}")
        else:
            if right.get("reviewer") != "RIGHT":
                blocks.append("RIGHT review 'reviewer' field must be 'RIGHT'")
            dec = right.get("decision", "")
            if dec in BLOCKING_DECISIONS:
                blocks.append(f"RIGHT review BLOCKED: {dec} — {right.get('one_line', '')}")
            elif dec not in {"APPROVE"}:
                blocks.append(f"RIGHT review unexpected decision: {dec!r}")
            if right.get("human_confirmation") == "REQUIRED":
                blocks.append("RIGHT review: human_confirmation=REQUIRED — human must approve first")

    # LEFT review (optional — warns only if missing)
    left_path = review_dir / "left" / f"left_review_{intent_id}.json"
    left = _load_optional_json(left_path)
    if left is None:
        warns.append(f"LEFT review not found at {left_path} — proceeding with warning")
    else:
        dec = left.get("decision", "")
        if dec in BLOCKING_DECISIONS:
            blocks.append(f"LEFT review BLOCKED: {dec} — {left.get('one_line', '')}")

    # Validator (optional — warns only if missing)
    val_path = review_dir / "validator" / f"validator_{intent_id}.json"
    val = _load_optional_json(val_path)
    if val is None:
        warns.append(f"Validator result not found at {val_path} — proceeding with warning")
    else:
        dec = val.get("decision", "")
        if dec == "BLOCK":
            blocks.append(f"Validator BLOCKED — check {val_path.name}")
        elif dec != "PASS":
            blocks.append(f"Validator unexpected decision: {dec!r}")

    return blocks, warns


# ── Main dry-run logic ─────────────────────────────────────────────────────────

def dry_run(intent_id: str, base_dir: Path) -> int:
    intent_path = base_dir / ".intent" / f"{intent_id}.json"
    plan_path   = base_dir / ".plan"   / f"{intent_id}.json"
    audit_path  = base_dir / ".logs"   / "audit.jsonl"

    print(f"\nSENTINEL DRY-RUN — intent: {intent_id!r}")
    print("=" * 60)

    intent = _load_json(intent_path, "intent")
    plan   = _load_json(plan_path,   "plan")

    # Verify intent_id consistency
    if intent.get("intent_id") != intent_id:
        print(f"ERROR: intent file intent_id mismatch", file=sys.stderr)
        sys.exit(2)
    if plan.get("intent_ref") != intent_id:
        print(f"ERROR: plan intent_ref does not match intent_id", file=sys.stderr)
        sys.exit(2)

    # Step 1: paperwork
    blocks, warns = _check_paperwork(base_dir, intent_id)

    for w in warns:
        print(f"WARN:  {w}")

    if blocks:
        print("\nPAPERWORK BLOCKED — dry-run not permitted.\n")
        for b in blocks:
            print(f"  ✗  {b}")
        print(f"\nDRY-RUN RESULT: BLOCKED")
        print(f"execution_performed: false")
        _append_audit(audit_path, intent_id, "DRY_RUN_BLOCKED",
                      decision="BLOCK", notes="paperwork_blocked; " + "; ".join(blocks))
        return 1

    print("Paperwork: ✓ PASS")

    # Step 2: boundary check
    allowed_paths = intent.get("constraints", {}).get("allowed_paths", [])
    print(f"Allowed paths:  {allowed_paths}")

    boundary_blocks: list[str] = []
    planned_actions: list[dict] = []

    for fmod in plan.get("files_to_modify", []):
        target = fmod.get("path", "")
        source = fmod.get("source", "")
        change_type = fmod.get("change_type", "")

        if not _within_allowed(target, allowed_paths):
            boundary_blocks.append(
                f"target '{target}' is outside allowed_paths {allowed_paths}"
            )
        else:
            source_path = base_dir / source
            planned_actions.append({
                "source": source,
                "target": target,
                "change_type": change_type,
                "source_exists": source_path.exists(),
            })

    if boundary_blocks:
        print("\nBOUNDARY VIOLATION — dry-run not permitted.\n")
        for v in boundary_blocks:
            print(f"  ✗  {v}")
        print(f"\nDRY-RUN RESULT: BLOCKED — scope drift")
        print(f"execution_performed: false")
        _append_audit(audit_path, intent_id, "DRY_RUN_BLOCKED",
                      decision="BLOCK",
                      notes="boundary_violation; " + "; ".join(boundary_blocks))
        return 1

    # Step 3: all clear — report planned actions only
    print("\nWHAT SENTINEL WOULD DO (not applied):")
    print()
    print("  → would create rollback snapshot of fixture workspace")
    for act in planned_actions:
        src_ok = "EXISTS ✓" if act["source_exists"] else "MISSING ✗"
        print(f"  → would copy '{act['source']}' [{src_ok}]")
        print(f"           to '{act['target']}' [{act['change_type']}]")

    cmds = plan.get("commands", {})
    print(f"  → would run post_apply: {cmds.get('post_apply', [])}")
    print(f"  → would run tests:      {cmds.get('test', [])}")
    print(f"  → rollback command:     {cmds.get('rollback', [])}")

    print()
    print("WHAT SENTINEL REFUSED TO DO:")
    print("  ✗  did not copy any file")
    print("  ✗  did not run any command")
    print("  ✗  did not create consensus record")
    print("  ✗  did not touch runtime workspace or services")

    print()
    print(f"DRY-RUN RESULT: ALLOWED")
    print(f"execution_performed: false")

    _append_audit(audit_path, intent_id, "DRY_RUN_ALLOWED",
                  decision="ALLOWED",
                  notes="paperwork_pass; boundary_clean; no_execution_performed")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sentinel dry-run: show what Sentinel would do, without applying anything."
    )
    parser.add_argument("--intent-id", required=True,
                        help="Intent ID to dry-run (e.g. 2026-06-03-001)")
    parser.add_argument("--base-dir", default=".",
                        help="Base directory of BICAMERAL_MVP (default: current dir)")
    args = parser.parse_args()

    base_dir = Path(args.base_dir).resolve()
    if not base_dir.exists():
        print(f"ERROR: base-dir not found: {base_dir}", file=sys.stderr)
        sys.exit(2)

    sys.exit(dry_run(args.intent_id, base_dir))


if __name__ == "__main__":
    main()
