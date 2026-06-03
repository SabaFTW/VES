"""
test_sentinel_execute_fixture.py — Tests for tools/sentinel_execute_fixture.py

Tests D0 fixture execution gate: approved copy, target creation, rollback,
blocked trace refusal, boundary enforcement, missing source error.
No external calls. No subprocess. No live workspace mutation.
"""

import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))
from sentinel_execute_fixture import execute, rollback, D0_ALLOWED_INTENT


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data))


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def _make_fixtures(base: Path, *,
                   source_rel: str = ".fixtures/manual_e2e/staged/status_note.html",
                   target_rel: str = ".fixtures/manual_e2e/workspace/status_note.html",
                   create_source: bool = True) -> None:
    """Write minimal valid D0 intent + plan + RIGHT-APPROVE review into base."""
    iid = D0_ALLOWED_INTENT

    _write_json(base / ".intent" / f"{iid}.json", {
        "intent_id": iid,
        "constraints": {"allowed_paths": [".fixtures/manual_e2e/"]},
    })
    _write_json(base / ".plan" / f"{iid}.json", {
        "plan_id": iid,
        "intent_ref": iid,
        "agent": "codex-constructor",
        "files_to_modify": [{
            "source": source_rel,
            "path": target_rel,
            "change_type": "create",
        }],
        "commands": {"post_apply": [], "test": [], "rollback": []},
    })
    _write_json(base / ".review" / "right" / f"right_review_{iid}.json", {
        "intent_id": iid,
        "reviewer": "RIGHT",
        "decision": "APPROVE",
        "semantic_summary": "Fixture-only, safe.",
        "scope_status": "IN_SCOPE",
        "boundary_status": "CLEAR",
        "human_confirmation": "NOT_REQUIRED",
        "one_line": "Approve.",
    })
    if create_source:
        _write_text(base / source_rel, "<html><body>status note</body></html>")


class TestApprovedExecution(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.base = Path(self.tmp.name)
        _make_fixtures(self.base)

    def tearDown(self):
        self.tmp.cleanup()

    def test_execute_returns_0(self):
        result = execute(D0_ALLOWED_INTENT, self.base)
        self.assertEqual(result, 0)

    def test_execute_creates_target_file(self):
        execute(D0_ALLOWED_INTENT, self.base)
        target = self.base / ".fixtures/manual_e2e/workspace/status_note.html"
        self.assertTrue(target.exists(), "target file must exist after execute")

    def test_target_content_matches_source(self):
        execute(D0_ALLOWED_INTENT, self.base)
        source = self.base / ".fixtures/manual_e2e/staged/status_note.html"
        target = self.base / ".fixtures/manual_e2e/workspace/status_note.html"
        self.assertEqual(source.read_bytes(), target.read_bytes())

    def test_audit_events_written(self):
        execute(D0_ALLOWED_INTENT, self.base)
        audit = self.base / ".logs" / "audit.jsonl"
        self.assertTrue(audit.exists())
        events = [json.loads(l)["event"]
                  for l in audit.read_text().strip().splitlines()]
        self.assertIn("EXECUTION_PREFLIGHT_START", events)
        self.assertIn("ROLLBACK_SNAPSHOT_CREATED", events)
        self.assertIn("FILE_COPY_ATTEMPTED", events)
        self.assertIn("FILE_COPY_COMPLETED", events)
        self.assertIn("EXECUTION_COMPLETE", events)


class TestRollback(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.base = Path(self.tmp.name)
        _make_fixtures(self.base)

    def tearDown(self):
        self.tmp.cleanup()

    def test_rollback_removes_created_file(self):
        execute(D0_ALLOWED_INTENT, self.base)
        target = self.base / ".fixtures/manual_e2e/workspace/status_note.html"
        self.assertTrue(target.exists())

        result = rollback(D0_ALLOWED_INTENT, self.base)
        self.assertEqual(result, 0)
        self.assertFalse(target.exists(), "target must be absent after rollback")

    def test_rollback_without_snapshot_returns_2(self):
        # No execute was run — no snapshot exists
        result = rollback(D0_ALLOWED_INTENT, self.base)
        self.assertEqual(result, 2)

    def test_rollback_audit_events_written(self):
        execute(D0_ALLOWED_INTENT, self.base)
        rollback(D0_ALLOWED_INTENT, self.base)
        audit = self.base / ".logs" / "audit.jsonl"
        events = [json.loads(l)["event"]
                  for l in audit.read_text().strip().splitlines()]
        self.assertIn("ROLLBACK_TRIGGERED", events)
        self.assertIn("ROLLBACK_COMPLETE", events)


class TestBlockedExecution(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.base = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_refuses_blocked_trace_002(self):
        result = execute("2026-06-03-002", self.base)
        self.assertEqual(result, 1)

    def test_refuses_arbitrary_intent_id(self):
        result = execute("9999-01-01-001", self.base)
        self.assertEqual(result, 1)

    def test_refuses_target_outside_fixture_boundary(self):
        _make_fixtures(self.base)
        # Override plan to target .workspace/app.py (outside allowed_paths)
        _write_json(self.base / ".plan" / f"{D0_ALLOWED_INTENT}.json", {
            "plan_id": D0_ALLOWED_INTENT,
            "intent_ref": D0_ALLOWED_INTENT,
            "agent": "codex-constructor",
            "files_to_modify": [{
                "source": ".fixtures/manual_e2e/staged/status_note.html",
                "path": ".workspace/app.py",
                "change_type": "modify",
            }],
            "commands": {},
        })
        result = execute(D0_ALLOWED_INTENT, self.base)
        self.assertEqual(result, 1)

    def test_workspace_app_py_never_created(self):
        _make_fixtures(self.base)
        # Even with bad target, .workspace/app.py must never be created
        _write_json(self.base / ".plan" / f"{D0_ALLOWED_INTENT}.json", {
            "plan_id": D0_ALLOWED_INTENT,
            "intent_ref": D0_ALLOWED_INTENT,
            "agent": "codex-constructor",
            "files_to_modify": [{
                "source": ".fixtures/manual_e2e/staged/status_note.html",
                "path": ".workspace/app.py",
                "change_type": "modify",
            }],
            "commands": {},
        })
        execute(D0_ALLOWED_INTENT, self.base)
        self.assertFalse((self.base / ".workspace" / "app.py").exists())

    def test_missing_source_exits_2(self):
        _make_fixtures(self.base, create_source=False)
        with self.assertRaises(SystemExit) as cm:
            execute(D0_ALLOWED_INTENT, self.base)
        self.assertEqual(cm.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
