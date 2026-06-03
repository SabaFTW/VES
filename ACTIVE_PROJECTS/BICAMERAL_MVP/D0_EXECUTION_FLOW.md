# Bicameral Kernel — D0 Fixture Execution Flow

Status: COMPLETE
Date: 2026-06-03

---

## Canonical Sentence

> D0 proves the knife can make one controlled cut and return clean.

---

## What D0 Is

D0 is the first real execution gate slice. It is NOT full D-phase.

D0 proves exactly three things:
1. Sentinel can apply one bounded file copy under full preflight control
2. Sentinel creates a rollback snapshot before any mutation
3. Sentinel can restore exact pre-mutation state on rollback

D0 is deliberately, almost offensively small. One file. One direction. One boundary. No runtime, no services, no subprocess, no network, no sudo.

---

## What Was Executed

```
Intent:  2026-06-03-001
Source:  .fixtures/manual_e2e/staged/status_note.html
Target:  .fixtures/manual_e2e/workspace/status_note.html
```

The workspace was empty before execution. The file was created. Rollback removed it. Runtime was never touched.

---

## How to Run

**Execute:**

```bash
cd /home/saba/VES/ACTIVE_PROJECTS/BICAMERAL_MVP
python tools/sentinel_execute_fixture.py --intent-id 2026-06-03-001
```

Expected: exit 0, `EXECUTION RESULT: COMPLETE`, target file created.

**Verify target exists:**

```bash
ls -la .fixtures/manual_e2e/workspace/
```

**Rollback:**

```bash
python tools/sentinel_execute_fixture.py --intent-id 2026-06-03-001 --rollback
```

Expected: exit 0, `ROLLBACK RESULT: COMPLETE`, target file removed.

**Verify workspace empty:**

```bash
ls -la .fixtures/manual_e2e/workspace/
```

**Confirm blocked trace is refused:**

```bash
python tools/sentinel_execute_fixture.py --intent-id 2026-06-03-002
```

Expected: exit 1, `EXECUTION RESULT: BLOCKED`.

---

## How Rollback Works

1. Before any mutation, `_create_snapshot()` records the target's pre-mutation state in `.rollback/<intent_id>_<ts>/`
2. If the target did not exist: `snapshot.json` records `existed_before: false`
3. If the target existed: content is copied to `pre_mutation_content` in the snapshot dir, hash recorded
4. On `--rollback`: snapshot is found, target is deleted (if it didn't exist before) or restored from `pre_mutation_content`
5. All rollback events appended to `.logs/audit.jsonl`

`.rollback/` is gitignored — it is local runtime only.

---

## What D0 Proves

| Claim | Evidence |
|-------|----------|
| Sentinel performs one real bounded file copy | execute returns 0, target exists |
| Rollback snapshot taken before any mutation | ROLLBACK_SNAPSHOT_CREATED in audit |
| Rollback restores exact pre-mutation state | target absent after rollback |
| Blocked trace is refused at D0 hard constraint | 2026-06-03-002 returns exit 1 |
| Runtime untouched throughout | .workspace/ never created |
| Audit records all required events | See Audit Events section |
| 12 new tests pass, full suite green | 73 tests total |

---

## Audit Events

Every execution appends to `.logs/audit.jsonl` (local runtime, gitignored):

On successful execute:
1. `EXECUTION_PREFLIGHT_START`
2. `ROLLBACK_SNAPSHOT_CREATED` — snapshot dir name
3. `FILE_COPY_ATTEMPTED` — source, target, change_type
4. `FILE_COPY_COMPLETED` — target path, sha256
5. `EXECUTION_COMPLETE` — `execution_performed=true`

On rollback:
1. `ROLLBACK_TRIGGERED` — snapshot name, target path
2. `ROLLBACK_COMPLETE` — existed_before state

On block:
1. `EXECUTION_BLOCKED` — reason

---

## What D0 Does NOT Allow

- Any intent_id other than `2026-06-03-001`
- Any target outside `.fixtures/manual_e2e/`
- `.workspace/app.py` or any production/runtime path (hard-forbidden)
- `.workspace/templates/`, `tests/` (hard-forbidden)
- Multi-file plans (exactly 1 file operation required)
- subprocess or shell commands
- Network calls, API calls, external models
- sudo
- Service start/stop/restart
- Package install
- Symlink traversal

---

## Why This Is D0, Not Full D-phase

Full D-phase would require (none of these are built):

- Execution of arbitrary approved intents beyond the one hardcoded candidate
- Command execution gate (whitelist enforcement for post_apply/test commands)
- Post-apply test orchestration on real mutation
- Human veto / explicit GO signal in live gate
- Multi-file plan support
- Runtime touching discipline under concurrent access
- Automated consensus signing

D0 has none of these. It is the smallest possible proof that the gate works.

---

## Test Coverage

```
tests/test_sentinel_execute_fixture.py — 12 tests
```

| Test | What it proves |
|------|---------------|
| test_execute_returns_0 | approved trace succeeds |
| test_execute_creates_target_file | file appears in fixture workspace |
| test_target_content_matches_source | exact byte match source→target |
| test_audit_events_written | all required audit events present |
| test_rollback_removes_created_file | rollback removes file |
| test_rollback_without_snapshot_returns_2 | no snapshot → clean error |
| test_rollback_audit_events_written | TRIGGERED + COMPLETE in audit |
| test_refuses_blocked_trace_002 | 2026-06-03-002 → exit 1 |
| test_refuses_arbitrary_intent_id | any non-D0 id → exit 1 |
| test_refuses_target_outside_fixture_boundary | .workspace/app.py target → exit 1 |
| test_workspace_app_py_never_created | .workspace/app.py never materialized |
| test_missing_source_exits_2 | missing source → exit 2 |

---

## Files Added

```
tools/sentinel_execute_fixture.py     ← D0 execution gate (execute + rollback)
tests/test_sentinel_execute_fixture.py ← 12 tests
D0_EXECUTION_FLOW.md                   ← this file
```

Local runtime (gitignored):
```
.rollback/<intent_id>_<ts>/           ← rollback snapshots
  snapshot.json                        ← metadata (existed_before, sha256)
  pre_mutation_content                 ← original bytes (if target existed)
```

---

## Status

**Full test suite: 73 passing, 0 failures.**

D0 is complete. The knife made one controlled cut and returned clean.

The next slice (when needed) is extending the gate beyond fixture-only — but that requires:
1. Defining the expanded allowed_paths contract
2. Building the command execution whitelist
3. Implementing the human GO signal
4. Adding post-apply test orchestration

Do not extend D0 without completing EXECUTION_GATE_PREFLIGHT.md first.

---

*D0 FIXTURE EXECUTION COMPLETE. THE KNIFE MADE ONE CONTROLLED CUT AND RETURNED CLEAN.*
