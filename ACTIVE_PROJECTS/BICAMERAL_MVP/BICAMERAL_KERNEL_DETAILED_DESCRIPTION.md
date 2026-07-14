# Bicameral Kernel — Detailed C+D0 Description

Date: 2026-06-03
Status: Canonical record. C-phase and D0 are complete and merged.

---

## One-sentence definition

The Bicameral Kernel is a staged change-control loop that turns user intent into validated plans, reviews, dry-runs, bounded execution, rollback, and audit evidence — keeping a human in the loop at every gate that matters.

---

## Why it exists

Ordinary AI agents blur the line between evidence, interpretation, approval, and action. They produce a result and present it as correct. If the result is wrong, the trail is often gone.

The Kernel separates those things:

- Evidence is observed and recorded before any interpretation is applied.
- Interpretation is written down and reviewed before any approval is granted.
- Approval is explicit and bounded, not assumed.
- Action is the last step, not the first reflex.
- Rollback is prepared before action, not invented after failure.

The goal is not autonomy theater. The goal is reversible, inspectable, human-bounded change — where the audit log never lies, the boundary never moves silently, and rollback is proven before it is needed.

---

## Core distinction

These are four separate things. Do not confuse them.

| System | What it is |
|--------|------------|
| **Bicameral HUD** | Shows truth — a ledger viewer for envelope objects (observations, approvals, sources of truth). Static display only. |
| **Bicameral Kernel** | Changes carefully — intent → review → dry-run → bounded execution → rollback → audit. |
| **REBiS / ConsMAP** | Public epistemic framing — how to read claims, what symbolic boundaries mean, the ConsMAP claim-hygiene corpus. |
| **OpenClaw / Hermes / leak archaeology** | Concept mine for the Kernel's design — not a product, not an integration target. |

The Kernel is not a personality. It is a change-control loop.

---

## Architecture layers

### 1. Intent layer
The user request is recorded as a structured JSON document: what is asked, what is allowed, what is forbidden, what rollback triggers exist. Nothing happens without an intent.

### 2. Plan layer
An agent produces a plan: which files to copy, what post-apply commands to run, what test to confirm success, what rollback command to execute. The plan references the intent by `intent_ref`.

### 3. Review layer
Three independent reviewers read the plan and produce structured verdicts:
- **RIGHT review** (required): semantic review — does the plan match the intent? Is the scope correct? Is human confirmation required?
- **LEFT review** (optional, blocks if present): technical review — do the paths match the allowed prefix? Are there machine-readable violations?
- **Validator** (optional, blocks if present): formal check — F11 (intent consistency), F12 (plan scope drift), F13 (command scope drift).

Any single blocking review stops the pipeline. All three must pass to proceed.

### 4. Consensus layer
If all reviews pass, a consensus record is written: `PROCEED`, referencing all review files and the intent. No consensus → no dry-run.

### 5. Sentinel dry-run layer
`tools/sentinel_dry_run.py` reads the full artifact chain and reports what Sentinel *would* do — without doing it. It appends `DRY_RUN_ALLOWED` or `DRY_RUN_BLOCKED` to the audit log. Exit codes: 0=ALLOWED, 1=BLOCKED, 2=ERROR.

### 6. D0 execution layer
`tools/sentinel_execute_fixture.py` performs the first real mutation — but only for the one approved fixture trace (intent `2026-06-03-001`). Before any file is touched, a rollback snapshot is created. After the copy, the target is verified. Audit events are written at every step.

### 7. Rollback layer
`--rollback` flag on `sentinel_execute_fixture.py` loads the pre-mutation snapshot and restores the target to its exact prior state. If the target did not exist before, it is deleted. If it existed, the exact bytes are restored. This is audited.

### 8. Audit layer
All events append to `.logs/audit.jsonl` (local runtime, gitignored). Every entry has: timestamp, event name, intent_id, and which tool wrote it. `execution_performed=true` is set only if at least one file was actually modified. The audit log is append-only and is never modified retroactively.

### 9. Human boundary layer
D0 has no command execution gate. No post-apply commands are run. No human GO signal is wired in. The human boundary is enforced by the D0 hard constraint (`intent_id` must equal `2026-06-03-001`) and the path boundary check (`.fixtures/manual_e2e/` only). Anything outside these boundaries is refused at the first check.

---

## C-phase timeline

### 2026-06-03-001 — APPROVE trace

- Intent: "Add a tiny static status note to a test workspace page."
- Plan: copy `.fixtures/manual_e2e/staged/status_note.html` → `.fixtures/manual_e2e/workspace/status_note.html`.
- RIGHT review: APPROVE — "Plan matches intent, scope is fixture-only, boundary clear."
- LEFT review: APPROVE — "Path prefix correct, no machine-readable violations."
- Validator: PASS — F11/F12/F13 all clear.
- Consensus: PROCEED.
- Dry-run: exit 0, DRY-RUN ALLOWED. Workspace stayed empty.
- Audit: VALIDATE_PAPERWORK_PASS, DRY_RUN_ALLOWED.
- **What it proved: the pipeline can breathe.**

### 2026-06-03-002 — BLOCK trace

- Intent: same request, fixture-only allowed_paths.
- Plan: deliberately targets `.workspace/app.py` — the live Flask application. Scope drift.
- RIGHT review: BLOCK — "Plan exits the fixture sandbox and targets the live workspace app."
- LEFT review: BLOCK — "Target path .workspace/app.py is outside the declared fixture boundary."
- Validator: BLOCK — F12 (plan scope drift) + F13 (command scope drift).
- Dry-run: exit 1, DRY-RUN BLOCKED. `.workspace/app.py` never touched.
- Audit: VALIDATE_PAPERWORK_BLOCK, DRY_RUN_BLOCKED.
- **What it proved: the pipeline has a spine. Three layers blocked simultaneously. Any one is sufficient.**

### Sentinel dry-run

- Tool: `tools/sentinel_dry_run.py`
- APPROVE trace: exit 0. Reports what would happen, never applies. Workspace stays empty.
- BLOCK trace: exit 1. Blocked at paperwork layer. Nothing executed.
- **What it proved: the hand can hover over the knife without cutting.**

### Test baseline at C-phase completion: 61 tests passing.

---

## D0 timeline

**PR #74, merged 2026-06-03. Merge commit: `79dc501`.**

### What was built

`tools/sentinel_execute_fixture.py` — first real Sentinel execution gate slice.

- D0 hard constraint: only accepts intent_id `2026-06-03-001`.
- Pre-flight: loads intent + plan, checks paperwork, verifies source exists, verifies target is within `.fixtures/manual_e2e/`, verifies target is not a forbidden path.
- Rollback snapshot: `_create_snapshot()` records the target's pre-mutation state in `.rollback/<intent_id>_<ts>/` before any file is touched.
- File copy: `shutil.copy2()` — pure Python, no subprocess, no shell.
- Verification: target existence confirmed after copy.
- Audit: EXECUTION_PREFLIGHT_START, ROLLBACK_SNAPSHOT_CREATED, FILE_COPY_ATTEMPTED, FILE_COPY_COMPLETED, EXECUTION_COMPLETE (execution_performed=true).
- Rollback: `--rollback` flag loads snapshot, removes target (if it didn't exist before) or restores exact bytes. Audit: ROLLBACK_TRIGGERED, ROLLBACK_COMPLETE.
- Blocked trace: any intent_id other than `2026-06-03-001` → immediate exit 1, EXECUTION_BLOCKED.

### What happened in the live run

1. `python tools/sentinel_execute_fixture.py --intent-id 2026-06-03-001` → exit 0, EXECUTION RESULT: COMPLETE.
2. `.fixtures/manual_e2e/workspace/status_note.html` confirmed present.
3. `python tools/sentinel_execute_fixture.py --intent-id 2026-06-03-001 --rollback` → exit 0, ROLLBACK RESULT: COMPLETE.
4. `.fixtures/manual_e2e/workspace/` confirmed empty.
5. `python tools/sentinel_execute_fixture.py --intent-id 2026-06-03-002` → exit 1, BLOCKED.
6. `.workspace/app.py` never created.

### Test baseline at D0 completion: 73 tests passing.

Changed files:
- `tools/sentinel_execute_fixture.py`
- `tests/test_sentinel_execute_fixture.py` (12 tests)
- `D0_EXECUTION_FLOW.md`

---

## The five abilities learned

| # | Ability | Evidence |
|---|---------|----------|
| 01 | Say YES safely | APPROVE trace — paperwork passes, consensus issued, dry-run allowed |
| 02 | Say NO concretely | BLOCK trace — three layers fire simultaneously, nothing executed |
| 03 | Hover without cutting | Sentinel dry-run — reports what would happen, audit appended, no mutation |
| 04 | Cut once inside a fixture boundary | D0 — one file copy, rollback snapshot first, target verified |
| 05 | Roll back cleanly | D0 rollback — exact pre-mutation state restored, audit recorded |

---

## What D0 allows

Only this:

```
intent_id:  2026-06-03-001
source:     .fixtures/manual_e2e/staged/status_note.html
target:     .fixtures/manual_e2e/workspace/status_note.html
operation:  one file copy (shutil.copy2)
rollback:   --rollback flag removes target, restores pre-mutation state
```

Nothing else.

---

## What D0 forbids

Explicitly and permanently forbidden in D0:

- Any intent_id other than `2026-06-03-001`
- Any target outside `.fixtures/manual_e2e/`
- `.workspace/app.py` (hard-forbidden, checked by name)
- `.workspace/templates/` (hard-forbidden)
- `tests/` (hard-forbidden)
- subprocess or shell commands
- Any network call (curl, requests, urllib)
- sudo
- Service start/stop/restart (systemctl, gunicorn, etc.)
- Package install (pip, apt, npm)
- Shell glob in target paths
- Symlink traversal
- Multi-file plans (exactly 1 file operation required in D0)
- External API calls
- Local model invocations (Ollama or otherwise)
- Production or runtime mutation of any kind

---

## Why this is not full D-phase

Full D-phase would require all of these (none are built):

| Capability | Status |
|------------|--------|
| Execution of arbitrary approved intents | NOT BUILT |
| Command execution gate (whitelist for post_apply/test commands) | NOT BUILT |
| Human GO signal / explicit approval gate | NOT BUILT |
| Post-apply test orchestration on real mutation | NOT BUILT |
| Multi-file plan support | NOT BUILT |
| Runtime touching discipline under concurrent access | NOT TESTED |
| Automated consensus signing | NOT BUILT |

D0 proves only that the gate exists and works for one case. The knife made one controlled cut and returned clean. That is all it proves.

---

## Audit philosophy

The audit log is the ground truth. Visuals, explanations, and HUD displays are representations of the log — they follow, they do not lead.

Core principles:
- Evidence before interpretation
- `execution_performed=true` must reflect reality, not intent
- Rollback must be auditable before it is trusted
- The audit log is append-only — never modified retroactively
- No UI animation replaces a log entry
- A blocked trace that leaves nothing in the log is wrong — even blocks must be audited

---

## Canonical sentences

> APPROVE trace proved the pipeline can breathe.
> BLOCK trace proved the pipeline has a spine.
> Sentinel dry-run proved the hand can hover over the knife without cutting.
> D0 proved the knife can make one controlled cut and return clean.

---

## Next allowed direction

**D1 design only — no execution, no build.**

D1 would design:
- The command whitelist gate (safe/confirm/blocked categories for post_apply commands)
- The human GO signal format (what constitutes an explicit approval, how it is recorded)
- Expanded intent scope (how to safely accept intents beyond `2026-06-03-001`)

D1 must start from `EXECUTION_GATE_PREFLIGHT.md`. No item in that checklist is checked yet.

Do not start D1 build without completing the design first.
Do not start D1 at 3am after a working D0.

---

*C+D0 COMPLETE. THE PIPELINE CAN BREATHE. THE PIPELINE HAS A SPINE. THE KNIFE CUT ONCE AND RETURNED CLEAN.*
