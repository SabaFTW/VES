"""
test_sentinel_dry_run.py — Tests for tools/sentinel_dry_run.py

Tests: paperwork APPROVE trace exits 0, BLOCK trace exits 1, no file mutation,
       missing intent_id exits 2.
No external calls. No command execution. No live workspace mutation.
"""

import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))
from sentinel_dry_run import dry_run, _within_allowed


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data))


def _make_base(tmp: Path, intent_id: str, allowed_paths: list[str],
               plan_target: str, plan_source: str = None) -> Path:
    """Write minimal intent + plan + APPROVE reviews into tmp."""
    base = Path(tmp)
    src = plan_source or f".fixtures/manual_e2e/staged/note.html"

    _write_json(base / ".intent" / f"{intent_id}.json", {
        "intent_id": intent_id,
        "constraints": {
            "allowed_paths": allowed_paths,
        },
    })
    _write_json(base / ".plan" / f"{intent_id}.json", {
        "plan_id": intent_id,
        "intent_ref": intent_id,
        "agent": "codex-constructor",
        "files_to_modify": [{
            "source": src,
            "path": plan_target,
            "change_type": "create",
        }],
        "commands": {"post_apply": [], "test": [], "rollback": []},
    })
    _write_json(base / ".review" / "right" / f"right_review_{intent_id}.json", {
        "intent_id": intent_id,
        "reviewer": "RIGHT",
        "decision": "APPROVE",
        "semantic_summary": "Plan matches request.",
        "scope_status": "IN_SCOPE",
        "boundary_status": "CLEAR",
        "human_confirmation": "NOT_REQUIRED",
        "one_line": "Approve.",
    })
    return base


class TestWithinAllowed(unittest.TestCase):
    def test_exact_prefix_match(self):
        self.assertTrue(_within_allowed(".fixtures/manual_e2e/workspace/file.html",
                                        [".fixtures/manual_e2e/workspace/"]))

    def test_no_match(self):
        self.assertFalse(_within_allowed(".workspace/app.py",
                                         [".fixtures/manual_e2e/workspace/"]))

    def test_multiple_allowed_second_matches(self):
        self.assertTrue(_within_allowed(".fixtures/manual_e2e/staged/x.html",
                                        [".fixtures/manual_e2e/workspace/",
                                         ".fixtures/manual_e2e/staged/"]))


class TestApproveTrace(unittest.TestCase):
    def test_approve_trace_returns_0(self):
        with TemporaryDirectory() as tmp:
            base = _make_base(tmp, "2999-01-01-001",
                              allowed_paths=[".fixtures/manual_e2e/"],
                              plan_target=".fixtures/manual_e2e/workspace/note.html")
            result = dry_run("2999-01-01-001", Path(tmp))
        self.assertEqual(result, 0)

    def test_approve_trace_does_not_create_target_file(self):
        with TemporaryDirectory() as tmp:
            base = _make_base(tmp, "2999-01-01-002",
                              allowed_paths=[".fixtures/manual_e2e/"],
                              plan_target=".fixtures/manual_e2e/workspace/note.html")
            dry_run("2999-01-01-002", Path(tmp))
            target = Path(tmp) / ".fixtures/manual_e2e/workspace/note.html"
            self.assertFalse(target.exists(),
                             "dry-run must not create the target file")


class TestBlockTrace(unittest.TestCase):
    def test_boundary_violation_returns_1(self):
        """Plan targets path outside allowed_paths — boundary gate must block."""
        with TemporaryDirectory() as tmp:
            base = _make_base(tmp, "2999-01-01-003",
                              allowed_paths=[".fixtures/manual_e2e/workspace/",
                                             ".fixtures/manual_e2e/staged/"],
                              plan_target=".workspace/app.py")
            result = dry_run("2999-01-01-003", Path(tmp))
        self.assertEqual(result, 1)

    def test_paperwork_block_returns_1(self):
        """RIGHT review with decision=BLOCK must block dry-run."""
        with TemporaryDirectory() as tmp:
            intent_id = "2999-01-01-004"
            base = _make_base(tmp, intent_id,
                              allowed_paths=[".fixtures/manual_e2e/"],
                              plan_target=".fixtures/manual_e2e/workspace/note.html")
            # Overwrite RIGHT review with BLOCK decision
            _write_json(Path(tmp) / ".review" / "right" / f"right_review_{intent_id}.json", {
                "intent_id": intent_id,
                "reviewer": "RIGHT",
                "decision": "BLOCK",
                "semantic_summary": "Bad plan.",
                "scope_status": "OUT_OF_SCOPE",
                "boundary_status": "BREACHED",
                "human_confirmation": "REQUIRED",
                "one_line": "Blocked — scope drift.",
            })
            result = dry_run(intent_id, Path(tmp))
        self.assertEqual(result, 1)

    def test_boundary_block_does_not_mutate_workspace(self):
        """After a boundary-blocked dry-run, no files appear in the target dir."""
        with TemporaryDirectory() as tmp:
            base = _make_base(tmp, "2999-01-01-005",
                              allowed_paths=[".fixtures/manual_e2e/"],
                              plan_target=".workspace/app.py")
            dry_run("2999-01-01-005", Path(tmp))
            mutated = Path(tmp) / ".workspace" / "app.py"
            self.assertFalse(mutated.exists(),
                             "dry-run must not create .workspace/app.py even when blocked")


class TestMissingIntentId(unittest.TestCase):
    def test_missing_intent_file_exits_2(self):
        """If the intent file does not exist, dry_run should sys.exit(2)."""
        with TemporaryDirectory() as tmp:
            # Write plan but no intent file
            _write_json(Path(tmp) / ".plan" / "9999-01-01-001.json", {
                "plan_id": "9999-01-01-001",
                "intent_ref": "9999-01-01-001",
                "agent": "codex-constructor",
                "files_to_modify": [],
                "commands": {},
            })
            with self.assertRaises(SystemExit) as cm:
                dry_run("9999-01-01-001", Path(tmp))
            self.assertEqual(cm.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
