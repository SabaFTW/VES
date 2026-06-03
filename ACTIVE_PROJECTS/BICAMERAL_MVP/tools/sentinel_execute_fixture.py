#!/usr/bin/env python3
"""
sentinel_execute_fixture.py — Bicameral Kernel D0

First real execution gate slice. Applies exactly one approved fixture-only
file copy for intent 2026-06-03-001, with a mandatory rollback snapshot
taken before any mutation.

This is D0, not full D-phase:
  - Only intent_id 2026-06-03-001 is accepted (D0 hard constraint)
  - Only .fixtures/manual_e2e/ target paths are allowed
  - Pure Python file operations (shutil.copy2), no subprocess
  - Rollback snapshot taken before any mutation
  - Rollback restores exact pre-mutation state

This script:
  - does NOT start or restart any service
  - does NOT call external APIs or models
  - does NOT use sudo
  - does NOT touch .workspace/app.py or any production path
  - does NOT run shell commands from the plan

Exit codes:
    0 = execution or rollback succeeded
    1 = blocked — paperwork, boundary violation, or D0 constraint
    2 = error — bad args, missing files, I/O error
"""

import argparse
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

# D0 hard constraints
D0_ALLOWED_INTENT = "2026-06-03-001"
D0_FIXTURE_PREFIX = ".fixtures/manual_e2e/"
D0_FORBIDDEN_PREFIXES = [
    ".workspace/app.py",
    ".workspace/templates/",
    "tests/",
]

# Import shared utilities from sentinel_dry_run (same tools/ directory)
sys.path.insert(0, str(Path(__file__).parent))
from sentinel_dry_run import _check_paperwork, _load_json, _within_allowed


# ── Helpers ────────────────────────────────────────────────────────────────────

def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _append_audit(audit_path: Path, intent_id: str, event: str,
                  decision: str = "", notes: str = "") -> None:
    entry: dict = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "event": event,
        "intent_id": intent_id,
        "by": "SENTINEL_EXECUTE_FIXTURE",
    }
    if decision:
        entry["decision"] = decision
    if notes:
        entry["notes"] = notes
    try:
        audit_path.parent.mkdir(parents=True, exist_ok=True)
        with open(audit_path, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError as e:
        print(f"ERROR: cannot write audit log {audit_path}: {e}", file=sys.stderr)
        sys.exit(2)


def _is_forbidden(target: str) -> bool:
    return any(
        target == p.rstrip("/") or target.startswith(p)
        for p in D0_FORBIDDEN_PREFIXES
    )


# ── Rollback snapshot ──────────────────────────────────────────────────────────

def _create_snapshot(rollback_dir: Path, intent_id: str, target_path: Path) -> Path:
    """Record target's pre-mutation state. Returns the snapshot directory."""
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    snap_dir = rollback_dir / f"{intent_id}_{ts}"
    snap_dir.mkdir(parents=True, exist_ok=True)

    existed = target_path.exists()
    meta: dict = {
        "intent_id": intent_id,
        "ts": ts,
        "target": str(target_path),
        "existed_before": existed,
    }

    if existed:
        content_file = snap_dir / "pre_mutation_content"
        shutil.copy2(target_path, content_file)
        meta["sha256_before"] = _sha256(target_path)
        meta["content_file"] = content_file.name

    (snap_dir / "snapshot.json").write_text(json.dumps(meta, indent=2))
    return snap_dir


def _load_snapshot(rollback_dir: Path, intent_id: str) -> "tuple[Path | None, dict]":
    """Find the most recent snapshot for this intent_id."""
    if not rollback_dir.exists():
        return None, {}
    prefix = f"{intent_id}_"
    candidates = [
        d for d in rollback_dir.iterdir()
        if d.is_dir() and d.name.startswith(prefix)
    ]
    if not candidates:
        return None, {}
    snap_dir = sorted(candidates)[-1]
    meta_path = snap_dir / "snapshot.json"
    if not meta_path.exists():
        return None, {}
    with open(meta_path) as f:
        return snap_dir, json.load(f)


# ── Rollback ───────────────────────────────────────────────────────────────────

def _do_rollback(rollback_dir: Path, intent_id: str,
                 audit_path: Path, auto: bool = False) -> int:
    label = "AUTO-ROLLBACK" if auto else "ROLLBACK"
    print(f"\n{label} — intent: {intent_id!r}")
    print("=" * 60)

    snap_dir, meta = _load_snapshot(rollback_dir, intent_id)
    if snap_dir is None:
        print(f"ERROR: no rollback snapshot found for intent {intent_id!r}", file=sys.stderr)
        _append_audit(audit_path, intent_id, "ROLLBACK_FAILED", notes="no_snapshot_found")
        return 2

    target_str = meta.get("target", "")
    existed_before = meta.get("existed_before", False)

    if not target_str:
        print("ERROR: snapshot has no target path", file=sys.stderr)
        _append_audit(audit_path, intent_id, "ROLLBACK_FAILED", notes="snapshot_missing_target")
        return 2

    target_path = Path(target_str)

    _append_audit(
        audit_path, intent_id, "ROLLBACK_TRIGGERED",
        notes=f"snapshot: {snap_dir.name}; target: {target_str}; existed_before: {existed_before}",
    )

    try:
        if not existed_before:
            if target_path.exists():
                target_path.unlink()
                print(f"  → Removed: {target_path}")
            else:
                print(f"  → Target already absent: {target_path}")
        else:
            content_name = meta.get("content_file", "")
            if not content_name:
                print("ERROR: snapshot missing content_file reference", file=sys.stderr)
                _append_audit(audit_path, intent_id, "ROLLBACK_FAILED",
                              notes="snapshot_content_name_missing")
                return 2
            content_file = snap_dir / content_name
            if not content_file.exists():
                print(f"ERROR: snapshot content file missing: {content_file}", file=sys.stderr)
                _append_audit(audit_path, intent_id, "ROLLBACK_FAILED",
                              notes="snapshot_content_file_missing")
                return 2
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(content_file, target_path)
            print(f"  → Restored: {target_path}")
    except OSError as e:
        print(f"ERROR: rollback failed: {e}", file=sys.stderr)
        _append_audit(audit_path, intent_id, "ROLLBACK_FAILED", notes=str(e))
        return 2

    _append_audit(
        audit_path, intent_id, "ROLLBACK_COMPLETE",
        notes=f"existed_before={existed_before}; target={target_str}",
    )
    print(f"\nROLLBACK RESULT: COMPLETE")
    print(f"execution_performed: false (undone)")
    return 0


# ── Execute ────────────────────────────────────────────────────────────────────

def execute(intent_id: str, base_dir: Path) -> int:
    """D0 fixture execution: preflight → snapshot → copy → verify → audit."""

    audit_path   = base_dir / ".logs"    / "audit.jsonl"
    rollback_dir = base_dir / ".rollback"

    print(f"\nSENTINEL EXECUTE FIXTURE — D0 — intent: {intent_id!r}")
    print("=" * 60)

    # ── D0 hard constraint ────────────────────────────────────────────────────
    if intent_id != D0_ALLOWED_INTENT:
        print(f"BLOCKED: D0 only allows intent {D0_ALLOWED_INTENT!r}. Got: {intent_id!r}")
        print(f"\nEXECUTION RESULT: BLOCKED")
        print(f"execution_performed: false")
        _append_audit(audit_path, intent_id, "EXECUTION_BLOCKED", decision="BLOCK",
                      notes=f"D0_hard_constraint: only {D0_ALLOWED_INTENT!r} is allowed")
        return 1

    # ── Load artifacts ────────────────────────────────────────────────────────
    intent = _load_json(base_dir / ".intent" / f"{intent_id}.json", "intent")
    plan   = _load_json(base_dir / ".plan"   / f"{intent_id}.json", "plan")

    if intent.get("intent_id") != intent_id:
        print("ERROR: intent file intent_id mismatch", file=sys.stderr)
        sys.exit(2)
    if plan.get("intent_ref") != intent_id:
        print("ERROR: plan intent_ref does not match intent_id", file=sys.stderr)
        sys.exit(2)

    _append_audit(audit_path, intent_id, "EXECUTION_PREFLIGHT_START",
                  notes="D0 fixture execution preflight")

    # ── Paperwork ─────────────────────────────────────────────────────────────
    blocks, warns = _check_paperwork(base_dir, intent_id)
    for w in warns:
        print(f"WARN:  {w}")

    if blocks:
        print("\nPAPERWORK BLOCKED — execution not permitted.\n")
        for b in blocks:
            print(f"  ✗  {b}")
        print(f"\nEXECUTION RESULT: BLOCKED")
        print(f"execution_performed: false")
        _append_audit(audit_path, intent_id, "EXECUTION_BLOCKED", decision="BLOCK",
                      notes="paperwork_blocked; " + "; ".join(blocks))
        return 1

    print("Paperwork: ✓ PASS")

    # ── D0 single-file constraint ─────────────────────────────────────────────
    files_to_modify = plan.get("files_to_modify", [])
    if len(files_to_modify) != 1:
        print(f"BLOCKED: D0 requires exactly 1 file operation; plan has {len(files_to_modify)}.")
        _append_audit(audit_path, intent_id, "EXECUTION_BLOCKED", decision="BLOCK",
                      notes=f"D0_single_file_constraint: got {len(files_to_modify)}")
        return 1

    fmod       = files_to_modify[0]
    source_rel = fmod.get("source", "")
    target_rel = fmod.get("path", "")
    change_type = fmod.get("change_type", "unknown")

    allowed_paths = intent.get("constraints", {}).get("allowed_paths", [])

    # ── Boundary checks ───────────────────────────────────────────────────────
    if not _within_allowed(target_rel, allowed_paths):
        print(f"BLOCKED: target {target_rel!r} outside allowed_paths {allowed_paths}")
        _append_audit(audit_path, intent_id, "EXECUTION_BLOCKED", decision="BLOCK",
                      notes=f"boundary_violation: {target_rel}")
        return 1

    if _is_forbidden(target_rel):
        print(f"BLOCKED: target {target_rel!r} is a forbidden path.")
        _append_audit(audit_path, intent_id, "EXECUTION_BLOCKED", decision="BLOCK",
                      notes=f"forbidden_path: {target_rel}")
        return 1

    if not target_rel.startswith(D0_FIXTURE_PREFIX):
        print(f"BLOCKED: target {target_rel!r} not inside D0 fixture prefix {D0_FIXTURE_PREFIX!r}")
        _append_audit(audit_path, intent_id, "EXECUTION_BLOCKED", decision="BLOCK",
                      notes=f"outside_fixture_prefix: {target_rel}")
        return 1

    source_path = base_dir / source_rel
    target_path = base_dir / target_rel

    if not source_path.exists():
        print(f"ERROR: source does not exist: {source_path}", file=sys.stderr)
        _append_audit(audit_path, intent_id, "EXECUTION_ABORTED",
                      notes=f"source_missing: {source_rel}")
        sys.exit(2)

    print(f"Source:  {source_rel} ✓")
    print(f"Target:  {target_rel}")
    print(f"Action:  {change_type}")

    # ── Rollback snapshot BEFORE any mutation ─────────────────────────────────
    try:
        snap_dir = _create_snapshot(rollback_dir, intent_id, target_path)
    except OSError as e:
        print(f"ERROR: rollback snapshot failed: {e}", file=sys.stderr)
        _append_audit(audit_path, intent_id, "EXECUTION_ABORTED",
                      notes=f"snapshot_failed: {e}")
        sys.exit(2)

    _append_audit(audit_path, intent_id, "ROLLBACK_SNAPSHOT_CREATED",
                  notes=f"snapshot: {snap_dir.name}")
    print(f"Snapshot: ✓ {snap_dir.name}")

    # ── File copy ─────────────────────────────────────────────────────────────
    _append_audit(audit_path, intent_id, "FILE_COPY_ATTEMPTED",
                  notes=f"source: {source_rel}; target: {target_rel}; change_type: {change_type}")

    try:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, target_path)
    except OSError as e:
        print(f"ERROR: file copy failed: {e}", file=sys.stderr)
        _append_audit(audit_path, intent_id, "FILE_COPY_FAILED", notes=str(e))
        _append_audit(audit_path, intent_id, "EXECUTION_ABORTED", notes="copy_failed")
        _do_rollback(rollback_dir, intent_id, audit_path, auto=True)
        sys.exit(2)

    if not target_path.exists():
        print(f"ERROR: target missing after copy: {target_path}", file=sys.stderr)
        _append_audit(audit_path, intent_id, "FILE_COPY_FAILED",
                      notes="verification_failed: target missing post-copy")
        _append_audit(audit_path, intent_id, "EXECUTION_ABORTED",
                      notes="post_copy_verification_failed")
        _do_rollback(rollback_dir, intent_id, audit_path, auto=True)
        sys.exit(2)

    _append_audit(audit_path, intent_id, "FILE_COPY_COMPLETED",
                  notes=f"target: {target_rel}; sha256: {_sha256(target_path)}")

    print(f"\n  ✓  Copied: {source_rel}")
    print(f"         → {target_rel}")

    _append_audit(audit_path, intent_id, "EXECUTION_COMPLETE", decision="COMPLETE",
                  notes=f"execution_performed=true; target: {target_rel}")

    print(f"\nEXECUTION RESULT: COMPLETE")
    print(f"execution_performed: true")
    print(f"\nTo rollback:")
    print(f"  python tools/sentinel_execute_fixture.py --intent-id {intent_id} --rollback")
    return 0


def rollback(intent_id: str, base_dir: Path) -> int:
    """Restore target file to pre-mutation state using rollback snapshot."""
    audit_path   = base_dir / ".logs"    / "audit.jsonl"
    rollback_dir = base_dir / ".rollback"
    return _do_rollback(rollback_dir, intent_id, audit_path, auto=False)


# ── Entry point ────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            f"Sentinel D0 fixture execution gate — "
            f"apply or rollback one approved fixture copy. "
            f"Only accepts intent {D0_ALLOWED_INTENT!r}."
        )
    )
    parser.add_argument("--intent-id", required=True,
                        help=f"Intent ID (D0 only accepts {D0_ALLOWED_INTENT!r})")
    parser.add_argument("--rollback", action="store_true",
                        help="Restore target to pre-mutation state from snapshot")
    parser.add_argument("--base-dir", default=".",
                        help="Base directory of BICAMERAL_MVP (default: current dir)")
    args = parser.parse_args()

    base_dir = Path(args.base_dir).resolve()
    if not base_dir.exists():
        print(f"ERROR: base-dir not found: {base_dir}", file=sys.stderr)
        sys.exit(2)

    if args.rollback:
        sys.exit(rollback(args.intent_id, base_dir))
    else:
        sys.exit(execute(args.intent_id, base_dir))


if __name__ == "__main__":
    main()
