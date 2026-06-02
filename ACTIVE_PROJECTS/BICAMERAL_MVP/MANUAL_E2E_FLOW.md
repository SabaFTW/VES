# Bicameral Kernel — C-phase Manual E2E Flow

Status: COMPLETE — APPROVE trace (2026-06-03-001) + BLOCK trace (2026-06-03-002)

---

## Purpose

This document records the first end-to-end paperwork trace through the Bicameral Bridge pipeline.

The goal was NOT to execute a real plan.
The goal was to prove that the artifact pipeline exists and holds:

```
intent → plan → review → consensus → audit log
```

without touching any live runtime.

---

## Artifact Flow

```
.intent/2026-06-03-001.json              ← user request, constraints, acceptance criteria
.plan/2026-06-03-001.json                ← staged file plan, rollback command
.review/right/right_review_2026-06-03-001.json   ← semantic review (APPROVE)
.review/left/left_review_2026-06-03-001.json     ← technical review (APPROVE)
.review/validator/validator_2026-06-03-001.json  ← F11/F12/F13 checks (PASS)
.consensus/2026-06-03-001-CONSENSUS.json         ← consensus record (PROCEED, no execution)
.logs/audit.jsonl                        ← one JSONL entry: VALIDATE_PAPERWORK_PASS
.fixtures/manual_e2e/staged/status_note.html     ← the staged file (exists, not applied)
.fixtures/manual_e2e/workspace/          ← target dir (empty — Sentinel has not run)
```

---

## What Was Created

| File | What it is |
|------|------------|
| `.intent/2026-06-03-001.json` | User intent with safety_level C, fixture-only paths |
| `.plan/2026-06-03-001.json` | Plan with agent=codex-constructor, single file write |
| `.review/right/right_review_2026-06-03-001.json` | RIGHT brain semantic review |
| `.review/left/left_review_2026-06-03-001.json` | LEFT brain technical review |
| `.review/validator/validator_2026-06-03-001.json` | F11/F12/F13 validator result |
| `.consensus/2026-06-03-001-CONSENSUS.json` | Consensus record with execution_mode=NO_EXECUTION |
| `.fixtures/manual_e2e/staged/status_note.html` | The staged artifact (proof-of-plan) |

---

## What Was Intentionally NOT Created

- Sentinel did NOT execute the plan
- The staged file was NOT copied to `.fixtures/manual_e2e/workspace/`
- No live `.workspace/` files were touched
- No services were started or restarted
- No runtime state was mutated
- No credentials were accessed
- No network calls were made

The `.fixtures/manual_e2e/workspace/` directory is intentionally empty.
This is correct. It proves the boundary held.

---

## How to Inspect the Trace

```bash
# Check all artifacts exist
ls .intent/2026-06-03-001.json
ls .plan/2026-06-03-001.json
ls .review/right/right_review_2026-06-03-001.json
ls .review/left/left_review_2026-06-03-001.json
ls .review/validator/validator_2026-06-03-001.json
ls .consensus/2026-06-03-001-CONSENSUS.json

# Read audit log
cat .logs/audit.jsonl

# Confirm staged file exists but workspace is empty
ls .fixtures/manual_e2e/staged/
ls .fixtures/manual_e2e/workspace/
```

---

## How to Run the Bridge Paperwork Validator

```bash
cd /home/saba/VES/ACTIVE_PROJECTS/BICAMERAL_MVP
python tools/bridge_validate_reviews.py --intent-id 2026-06-03-001
```

Expected output:
```
PAPERWORK PASS — intent '2026-06-03-001' may proceed to consensus.

  ✓  RIGHT review: APPROVE
  ✓  LEFT review:  APPROVE
  ✓  Validator:    PASS

Sentinel may execute ONLY after human confirmation if required.
```

---

## How to Run Tests

```bash
cd /home/saba/VES/ACTIVE_PROJECTS/BICAMERAL_MVP
python -m pytest tests/ -q
```

Expected: 37 passing.

---

## Why Sentinel Execution Gate Is Still Future Work

The current slice proves:
1. The artifact pipeline has the right shape
2. intent_id stays consistent across all files
3. RIGHT review passes bridge_validate_reviews.py
4. LEFT review and validator results are wired correctly
5. Audit log receives the VALIDATE_PAPERWORK_PASS event

What it does NOT prove:
- Sentinel can safely apply a plan to the real workspace
- Rollback can actually restore state
- The command gate (safe/confirm/blocked list) is correctly implemented
- Automated consensus signing is reliable

The Sentinel execution gate is the next natural slice.
It should be built only after:
1. This paperwork trace has been reviewed and accepted
2. A clear contract exists for what Sentinel may and may not do
3. The human override path is tested first

Do not skip this step to get to execution faster.

---

---

## BLOCK Case — 2026-06-03-002

### What this proves

The pipeline is not a rubber stamp. It can say NO with a concrete reason.

### Scenario

Same harmless user request: "Add a tiny static status note to a test fixture page."

Intent allowed only:
- `.fixtures/manual_e2e/workspace/`
- `.fixtures/manual_e2e/staged/`

Bad plan deliberately targeted: `.workspace/app.py` — the live Flask application.

### Artifact flow

```
.intent/2026-06-03-002.json               ← fixture-only request
.plan/2026-06-03-002.json                 ← BAD PLAN: targets .workspace/app.py
.review/right/right_review_2026-06-03-002.json   ← BLOCK: scope drift, boundary breached
.review/left/left_review_2026-06-03-002.json     ← BLOCK: prefix mismatch, F12 detected
.review/validator/validator_2026-06-03-002.json  ← BLOCK: F12 + F13 violations
.logs/audit.jsonl                         ← VALIDATE_PAPERWORK_BLOCK appended
```

### Validator output

```
BLOCKED — consensus is not allowed.

  ✗  RIGHT review BLOCKED: BLOCK — Plan exits the fixture sandbox and targets the live workspace app — BLOCK.
  ✗  RIGHT review requires human_confirmation=REQUIRED — Sentinel must wait for explicit human approval.
  ✗  LEFT review BLOCKED: BLOCK — Target path .workspace/app.py is outside the declared fixture boundary — BLOCK.
  ✗  Validator BLOCKED — check validator_2026-06-03-002.json for failure modes

exit: 1
```

### What was intentionally NOT done

- The bad plan was NOT applied
- `.workspace/app.py` was NOT modified
- No consensus PROCEED record was created
- No Sentinel execution was triggered
- The `.fixtures/manual_e2e/workspace/` directory remains as left by the APPROVE case

### Why the pipeline is not a rubber stamp

The APPROVE trace (2026-06-03-001) proved the pipeline can breathe.
The BLOCK trace (2026-06-03-002) proves the pipeline has a spine.

The scope drift was caught at THREE layers simultaneously:
1. RIGHT review: semantic mismatch between intent and plan
2. LEFT review: technical prefix check, machine-readable violation
3. Validator: F12 (plan scope drift) + F13 (command scope drift)

Any one of these is sufficient to block. All three fired.

---

---

## Sentinel Dry-Run — C-phase Gate

### What this proves

Sentinel can raise its hand and report what it *would* do — without touching anything.
The hand hovered over the knife. The knife stayed sheathed.

### Tool

```
tools/sentinel_dry_run.py
```

### How to run

```bash
cd /home/saba/VES/ACTIVE_PROJECTS/BICAMERAL_MVP

# APPROVE trace — valid fixture-only plan
python tools/sentinel_dry_run.py --intent-id 2026-06-03-001
# Expected exit: 0, DRY-RUN RESULT: ALLOWED

# BLOCK trace — bad plan, scope drift
python tools/sentinel_dry_run.py --intent-id 2026-06-03-002
# Expected exit: 1, DRY-RUN RESULT: BLOCKED
```

### APPROVE trace output (2026-06-03-001)

```
SENTINEL DRY-RUN — intent: '2026-06-03-001'
============================================================
Paperwork: ✓ PASS
Allowed paths:  ['.fixtures/manual_e2e/']

WHAT SENTINEL WOULD DO (not applied):

  → would create rollback snapshot of fixture workspace
  → would copy '.fixtures/manual_e2e/staged/status_note.html' [EXISTS ✓]
           to '.fixtures/manual_e2e/workspace/status_note.html' [create]
  → would run post_apply: [...]
  → would run tests:      [...]
  → rollback command:     [...]

WHAT SENTINEL REFUSED TO DO:
  ✗  did not copy any file
  ✗  did not run any command
  ✗  did not create consensus record
  ✗  did not touch runtime workspace or services

DRY-RUN RESULT: ALLOWED
execution_performed: false
```

### BLOCK trace output (2026-06-03-002)

```
SENTINEL DRY-RUN — intent: '2026-06-03-002'
============================================================

PAPERWORK BLOCKED — dry-run not permitted.

  ✗  RIGHT review BLOCKED: BLOCK — Plan exits the fixture sandbox and targets the live workspace app — BLOCK.
  ✗  RIGHT review: human_confirmation=REQUIRED — human must approve first
  ✗  LEFT review BLOCKED: BLOCK — Target path .workspace/app.py is outside the declared fixture boundary — BLOCK.
  ✗  Validator BLOCKED — check validator_2026-06-03-002.json

DRY-RUN RESULT: BLOCKED
execution_performed: false
```

### Audit entries appended

Both runs appended to `.logs/audit.jsonl`:
- `DRY_RUN_ALLOWED` (2026-06-03-001) — paperwork_pass; boundary_clean; no_execution_performed
- `DRY_RUN_BLOCKED` (2026-06-03-002) — paperwork_blocked; all three layers fired

### What was intentionally NOT done

- No file was copied
- No command was run
- No consensus record was created
- `.fixtures/manual_e2e/workspace/` remains as left by manual inspection
- `.workspace/app.py` was not touched

### Tests

```bash
python -m pytest tests/test_sentinel_dry_run.py -v
# 9 passed
```

Covers: `_within_allowed` logic, APPROVE returns 0, APPROVE does not create target file,
boundary violation returns 1, paperwork BLOCK returns 1, BLOCK does not mutate workspace,
missing intent file exits 2.

---

## C-phase Status: COMPLETE

Three layers proven:

| Layer | Artifact | Result |
|-------|----------|--------|
| Paperwork pipeline | APPROVE trace 2026-06-03-001 | Pipeline can breathe |
| Rejection gate | BLOCK trace 2026-06-03-002 | Pipeline has a spine |
| Sentinel gate | Dry-run both traces | Hand hovered, knife stayed sheathed |

The Sentinel execution gate (actual file copy + rollback) is the next natural slice.
It should be built only after this dry-run trace has been reviewed and accepted.

---

*SENTINEL DRY-RUN COMPLETE. THE HAND HOVERED OVER THE KNIFE BUT DID NOT CUT.*
