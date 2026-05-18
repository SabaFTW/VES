"""
test_bridge_validate.py — Tests for bridge_validate_reviews.py

Tests only validate the paperwork logic (JSON field checks, decision routing).
No file system side effects beyond temp dirs.
No external calls.
No command execution.
"""

import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))
from bridge_validate_reviews import validate


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data))


def _make_right(tmp: Path, intent_id: str, **overrides) -> Path:
    defaults = {
        "intent_id": intent_id,
        "reviewer": "RIGHT",
        "decision": "APPROVE",
        "semantic_summary": "Plan matches request.",
        "scope_status": "IN_SCOPE",
        "boundary_status": "CLEAN",
        "human_confirmation": "NOT_REQUIRED",
        "one_line": "Plan is semantically aligned.",
    }
    defaults.update(overrides)
    p = tmp / ".review" / "right" / f"right_review_{intent_id}.json"
    _write_json(p, defaults)
    return p


def _make_left(tmp: Path, intent_id: str, **overrides) -> Path:
    defaults = {
        "intent_id": intent_id,
        "decision": "APPROVE",
        "one_line": "Plan is technically bounded.",
    }
    defaults.update(overrides)
    p = tmp / ".review" / "left" / f"left_review_{intent_id}.json"
    _write_json(p, defaults)
    return p


def _make_validator(tmp: Path, intent_id: str, **overrides) -> Path:
    defaults = {
        "intent_id": intent_id,
        "decision": "PASS",
    }
    defaults.update(overrides)
    p = tmp / ".review" / "validator" / f"validator_{intent_id}.json"
    _write_json(p, defaults)
    return p


class TestPaperwerkPass(unittest.TestCase):

    def test_all_approve_returns_0(self):
        """All three reviews APPROVE/PASS → exit 0."""
        with TemporaryDirectory() as tmp_str:
            tmp = Path(tmp_str)
            intent_id = "2026-05-18-001"
            _make_right(tmp, intent_id)
            _make_left(tmp, intent_id)
            _make_validator(tmp, intent_id)
            result = validate(intent_id, tmp)
            self.assertEqual(result, 0)

    def test_missing_left_and_validator_warns_but_passes(self):
        """Missing LEFT + Validator → warns but still passes if RIGHT is APPROVE."""
        with TemporaryDirectory() as tmp_str:
            tmp = Path(tmp_str)
            intent_id = "2026-05-18-002"
            _make_right(tmp, intent_id)
            # No LEFT, no Validator
            result = validate(intent_id, tmp)
            self.assertEqual(result, 0)


class TestPaperwerkBlock(unittest.TestCase):

    def test_right_block_returns_1(self):
        """RIGHT review BLOCK → exit 1."""
        with TemporaryDirectory() as tmp_str:
            tmp = Path(tmp_str)
            intent_id = "2026-05-18-003"
            _make_right(tmp, intent_id, decision="BLOCK",
                        one_line="Scope drifts into corpus rewrite.")
            _make_left(tmp, intent_id)
            _make_validator(tmp, intent_id)
            result = validate(intent_id, tmp)
            self.assertEqual(result, 1)

    def test_right_hold_returns_1(self):
        """RIGHT review HOLD → exit 1."""
        with TemporaryDirectory() as tmp_str:
            tmp = Path(tmp_str)
            intent_id = "2026-05-18-004"
            _make_right(tmp, intent_id, decision="HOLD",
                        one_line="Needs human clarification.")
            result = validate(intent_id, tmp)
            self.assertEqual(result, 1)

    def test_left_block_returns_1(self):
        """LEFT review BLOCK → exit 1."""
        with TemporaryDirectory() as tmp_str:
            tmp = Path(tmp_str)
            intent_id = "2026-05-18-005"
            _make_right(tmp, intent_id)
            _make_left(tmp, intent_id, decision="BLOCK",
                        one_line="Command targets production path.")
            _make_validator(tmp, intent_id)
            result = validate(intent_id, tmp)
            self.assertEqual(result, 1)

    def test_validator_block_returns_1(self):
        """Validator BLOCK → exit 1."""
        with TemporaryDirectory() as tmp_str:
            tmp = Path(tmp_str)
            intent_id = "2026-05-18-006"
            _make_right(tmp, intent_id)
            _make_left(tmp, intent_id)
            _make_validator(tmp, intent_id, decision="BLOCK")
            result = validate(intent_id, tmp)
            self.assertEqual(result, 1)

    def test_missing_right_review_returns_1(self):
        """Missing RIGHT review → exit 1 (required)."""
        with TemporaryDirectory() as tmp_str:
            tmp = Path(tmp_str)
            intent_id = "2026-05-18-007"
            # No RIGHT review created
            _make_left(tmp, intent_id)
            _make_validator(tmp, intent_id)
            result = validate(intent_id, tmp)
            self.assertEqual(result, 1)

    def test_right_human_confirmation_required_returns_1(self):
        """RIGHT requires human confirmation → blocks Sentinel."""
        with TemporaryDirectory() as tmp_str:
            tmp = Path(tmp_str)
            intent_id = "2026-05-18-008"
            _make_right(tmp, intent_id,
                        human_confirmation="REQUIRED",
                        one_line="Needs human eye before proceeding.")
            _make_left(tmp, intent_id)
            _make_validator(tmp, intent_id)
            result = validate(intent_id, tmp)
            self.assertEqual(result, 1)

    def test_right_missing_required_field_returns_1(self):
        """RIGHT review missing required field → exit 1."""
        with TemporaryDirectory() as tmp_str:
            tmp = Path(tmp_str)
            intent_id = "2026-05-18-009"
            p = tmp / ".review" / "right" / f"right_review_{intent_id}.json"
            _write_json(p, {"intent_id": intent_id, "decision": "APPROVE"})
            result = validate(intent_id, tmp)
            self.assertEqual(result, 1)

    def test_right_wrong_reviewer_field_returns_1(self):
        """RIGHT review with reviewer != RIGHT → exit 1."""
        with TemporaryDirectory() as tmp_str:
            tmp = Path(tmp_str)
            intent_id = "2026-05-18-010"
            _make_right(tmp, intent_id, reviewer="LEFT")
            result = validate(intent_id, tmp)
            self.assertEqual(result, 1)


class TestConsMapChecks(unittest.TestCase):
    """ConsMAP-specific semantic boundary tests."""

    def test_premature_canonization_blocked_by_right(self):
        """Plan tries to canonize draft content → RIGHT should BLOCK."""
        with TemporaryDirectory() as tmp_str:
            tmp = Path(tmp_str)
            intent_id = "2026-05-18-011"
            _make_right(tmp, intent_id,
                        decision="BLOCK",
                        scope_status="OUT_OF_SCOPE",
                        one_line="Draft text promoted to canon — premature canonization (F17).")
            _make_left(tmp, intent_id)
            _make_validator(tmp, intent_id)
            result = validate(intent_id, tmp)
            self.assertEqual(result, 1)

    def test_bophameth_touch_blocked_by_right(self):
        """Plan tries to remove BOPHAMETH → RIGHT should BLOCK."""
        with TemporaryDirectory() as tmp_str:
            tmp = Path(tmp_str)
            intent_id = "2026-05-18-012"
            _make_right(tmp, intent_id,
                        decision="BLOCK",
                        boundary_status="BREACHED",
                        must_not_touch=["WelcomeRitual.tsx", "baphomet-loader.png"],
                        one_line="BOPHAMETH removal attempted — boundary breached.")
            result = validate(intent_id, tmp)
            self.assertEqual(result, 1)


if __name__ == "__main__":
    unittest.main()
