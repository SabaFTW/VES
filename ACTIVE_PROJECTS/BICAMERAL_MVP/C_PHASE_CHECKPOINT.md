# Bicameral Kernel — C-Phase Checkpoint

Status: SEALED
Date: 2026-06-03
Branch: bicameral-bridge-spec-v0.1

---

## Canonical Sentence

> APPROVE trace proved the pipeline can breathe.
> BLOCK trace proved the pipeline has a spine.
> Sentinel dry-run proved the hand can hover over the knife without cutting.

---

## What Was Proven

| Claim | Evidence |
|-------|----------|
| Paperwork pipeline has correct artifact shape | intent → plan → review → consensus → audit all exist and link |
| intent_id stays consistent across all files | Validated by bridge_validate_reviews.py and sentinel_dry_run.py |
| RIGHT review gates consensus | APPROVE = proceed allowed; BLOCK = consensus not issued |
| LEFT review and validator wired correctly | All three fire independently; any one is sufficient to block |
| Audit log receives events | audit.jsonl appended on VALIDATE, DRY_RUN_ALLOWED, DRY_RUN_BLOCKED |
| Sentinel can read allowed_paths from intent dynamically | Confirmed in dry-run — not hardcoded |
| Sentinel can distinguish ALLOWED vs BLOCKED intent before touching anything | exit 0 / exit 1 verified manually |
| Sentinel does not mutate anything during dry-run | .fixtures/manual_e2e/workspace/ remained empty after both runs |
| execution_performed=false is enforced | Neither dry-run created, copied, or modified a file |
| Tests cover the full paperwork + dry-run logic | 61 tests passing |

---

## Files and Tools That Now Exist

### Artifact traces (go into git)

```
.intent/2026-06-03-001.json              ← APPROVE trace intent
.plan/2026-06-03-001.json                ← APPROVE trace plan (fixture-only)
.review/right/right_review_2026-06-03-001.json
.review/left/left_review_2026-06-03-001.json
.review/validator/validator_2026-06-03-001.json
.consensus/2026-06-03-001-CONSENSUS.json

.intent/2026-06-03-002.json              ← BLOCK trace intent
.plan/2026-06-03-002.json                ← BLOCK trace plan (deliberate scope drift to .workspace/app.py)
.review/right/right_review_2026-06-03-002.json   ← BLOCK
.review/left/left_review_2026-06-03-002.json     ← BLOCK
.review/validator/validator_2026-06-03-002.json  ← BLOCK (F12 + F13)
```

### Tools

```
tools/bridge_validate_reviews.py    ← paperwork validator, appends VALIDATE_PAPERWORK_PASS/BLOCK
tools/sentinel_dry_run.py           ← dry-run gate: reads intent+plan+reviews, no mutation
```

### Tests

```
tests/test_bridge_validate.py       ← paperwork validation
tests/test_sentinel_dry_run.py      ← 9 tests: _within_allowed, APPROVE/BLOCK exits, no mutation
```

### Documentation

```
MANUAL_E2E_FLOW.md                  ← full trace narrative: APPROVE, BLOCK, dry-run
C_PHASE_CHECKPOINT.md               ← this file
EXECUTION_GATE_PREFLIGHT.md         ← preflight checklist for D-phase
```

### Local runtime (gitignored)

```
.logs/audit.jsonl                   ← VALIDATE_PAPERWORK_PASS, VALIDATE_PAPERWORK_BLOCK,
                                       DRY_RUN_ALLOWED, DRY_RUN_BLOCKED
.fixtures/manual_e2e/staged/status_note.html    ← staged artifact, not applied
.fixtures/manual_e2e/workspace/     ← intentionally empty (Sentinel has not executed)
```

---

## Commits That Matter

```
6a76d08  Add Bicameral Bridge v0.1 spec and paperwork validator
7505412  feat: C-phase manual E2E paperwork trace (APPROVE — 2026-06-03-001)
f2b9a76  feat: C-phase BLOCK trace — scope drift rejection (2026-06-03-002)
c74d23d  feat: C-phase Sentinel dry-run — hand hovered, knife stayed sheathed
```

---

## APPROVE Trace Summary (2026-06-03-001)

- Intent: "Add a tiny static status note to a test workspace page."
- Plan: copy `.fixtures/manual_e2e/staged/status_note.html` → `.fixtures/manual_e2e/workspace/status_note.html`
- All reviews: APPROVE / PASS
- Dry-run result: exit 0, DRY-RUN ALLOWED
- Mutation performed: none
- Audit entries: VALIDATE_PAPERWORK_PASS, DRY_RUN_ALLOWED

---

## BLOCK Trace Summary (2026-06-03-002)

- Intent: same request, fixture-only allowed_paths
- Plan: deliberately targets `.workspace/app.py` — the live Flask app (scope drift)
- RIGHT review: BLOCK — "Plan exits the fixture sandbox and targets the live workspace app"
- LEFT review: BLOCK — "Target path .workspace/app.py is outside the declared fixture boundary"
- Validator: BLOCK — F12 (plan scope drift) + F13 (command scope drift)
- Dry-run result: exit 1, DRY-RUN BLOCKED at paperwork layer
- Mutation performed: none
- Audit entries: VALIDATE_PAPERWORK_BLOCK, DRY_RUN_BLOCKED
- `.workspace/app.py` was never touched

The scope drift was caught at THREE layers simultaneously. Any one is sufficient to block.

---

## Sentinel Dry-Run Summary

Tool: `tools/sentinel_dry_run.py`

What it does:
1. Loads intent + plan, verifies intent_id consistency
2. Validates paperwork (RIGHT required, LEFT + validator optional but warn)
3. Checks each `files_to_modify[].path` against `intent.constraints.allowed_paths`
4. Reports what would happen (without applying)
5. Appends DRY_RUN_ALLOWED or DRY_RUN_BLOCKED to `.logs/audit.jsonl`
6. Returns exit 0 (ALLOWED) or 1 (BLOCKED) or 2 (ERROR)

What it never does:
- Does not copy, edit, or delete any file
- Does not run any command from the plan
- Does not start or restart any service
- Does not call external APIs or models
- Does not create a consensus record

---

## Audit / Log Behavior

All events append to `.logs/audit.jsonl` (local runtime, gitignored).
Each entry: `ts`, `event`, `intent_id`, `by`, `decision`, `notes`.

Events generated so far:
- `VALIDATE_PAPERWORK_PASS` — bridge_validate_reviews.py, 2026-06-03-001
- `VALIDATE_PAPERWORK_BLOCK` — bridge_validate_reviews.py, 2026-06-03-002
- `DRY_RUN_ALLOWED` — sentinel_dry_run.py, 2026-06-03-001
- `DRY_RUN_BLOCKED` — sentinel_dry_run.py, 2026-06-03-002

---

## Test Status

```
61 tests passing
0 failures
0 errors
```

Key test files:
- `tests/test_bridge_validate.py` — paperwork validator
- `tests/test_sentinel_dry_run.py` — 9 tests: boundary logic, no-mutation guarantee, exit codes, missing-file error path

---

## What Is Explicitly NOT Proven Yet

The following have not been built or tested:

| Capability | Status |
|------------|--------|
| Real file apply (actual copy from staged to workspace) | NOT BUILT |
| Rollback after actual mutation (snapshot + restore) | NOT BUILT |
| Command execution gate (safe/confirm/blocked whitelist) | NOT BUILT |
| Post-apply test orchestration on real mutation | NOT BUILT |
| Human veto in live gate | NOT BUILT |
| Runtime touching discipline under concurrent access | NOT TESTED |
| Automated consensus signing | NOT BUILT |

C-phase is complete as **paperwork + dry-run discipline**.
It is not complete as an **execution system**.
This is correct and intended.

---

## Next Step

See `EXECUTION_GATE_PREFLIGHT.md` for what must be true before any D-phase execution gate is designed.

Do not start D-phase without reviewing that checklist first.
