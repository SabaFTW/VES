# Bicameral Kernel — Execution Gate Preflight Checklist

Status: OPEN (not yet satisfied — no execution gate exists)
Date: 2026-06-03
Purpose: Define what must be true before any real file mutation is allowed.

This document does NOT build the execution gate.
It defines what the execution gate must prove before it is allowed to run.

---

## 1. Allowed Mutation Scope

Before any real execution, the following must be explicitly constrained:

- [ ] Target path is within `intent.constraints.allowed_paths` — verified dynamically, not hardcoded
- [ ] First candidate: `.fixtures/manual_e2e/workspace/` only
- [ ] `.workspace/app.py` is categorically forbidden (never a valid target for D-phase)
- [ ] `.workspace/templates/` is categorically forbidden
- [ ] No production or live runtime paths may be targets
- [ ] No path traversal permitted (e.g., `../../` in any resolved path)
- [ ] No symlink escape: resolved absolute path must still be within allowed prefix
- [ ] No glob patterns in target paths (explicit filenames only)
- [ ] Source file must exist before any copy is attempted

---

## 2. Rollback Requirements

Rollback is not optional. It must exist before any mutation is attempted.

- [ ] Rollback snapshot is created before any file is touched
- [ ] Snapshot stores exact byte content of the file before mutation
- [ ] Rollback path is recorded in the audit log before execution begins
- [ ] Rollback is tested in dry-run isolation before being trusted in live run
- [ ] Rollback must restore the file to its exact pre-mutation state
- [ ] If rollback itself fails, execution must abort and human must be notified
- [ ] Rollback must not be skipped even for "low risk" operations
- [ ] Rollback record must be in `.rollback/` (gitignored, local runtime only)

---

## 3. Command Whitelist

No command in `commands.post_apply`, `commands.test`, or `commands.rollback` may execute unless it passes a strict whitelist check.

Allowed command forms (initial candidate set):
- `ls -la <path>` — read-only listing
- `python3 -c "<inline check expression>"` — non-interactive, no imports beyond stdlib
- `cp <src> <dst>` — explicit file copy within allowed paths only
- `rm -f <path>` — only for rollback of files created by this execution, within allowed paths

Forbidden in any command field:
- [ ] `sudo` — never
- [ ] Any network call (`curl`, `wget`, `requests`, `urllib`)
- [ ] Service start/stop/restart (`systemctl`, `service`, `supervisorctl`, `gunicorn`, etc.)
- [ ] Package install (`pip install`, `apt`, `npm install`, etc.)
- [ ] Shell glob in target path (`*`, `?`, `**`)
- [ ] Subshell or backtick expansion
- [ ] Redirect to files outside allowed paths
- [ ] Any command that touches `.workspace/app.py`, `.workspace/templates/`, `tests/`
- [ ] External API calls
- [ ] Local model invocations

---

## 4. Human Approval Boundary

- [ ] Dry-run ALLOWED is not execution ALLOWED — these are separate gates
- [ ] Real execution requires an explicit human GO signal
- [ ] The GO signal format must be defined before D-phase is designed
- [ ] `human_confirmation=REQUIRED` in any review → automatic block, regardless of other decisions
- [ ] A BLOCK trace cannot be overridden silently by re-submitting with a different plan_id
- [ ] Human approval must be recorded in the audit log with timestamp and approver identifier
- [ ] No automated agent may approve its own execution request

---

## 5. Audit Requirements

Every execution attempt (whether it proceeds or aborts) must produce an audit trail:

- [ ] `EXECUTION_PREFLIGHT_START` — before any file is touched
- [ ] `ROLLBACK_SNAPSHOT_CREATED` — path and hash of snapshot
- [ ] `FILE_COPY_ATTEMPTED` — source, target, change_type
- [ ] `FILE_COPY_COMPLETED` or `FILE_COPY_FAILED` — with details
- [ ] `POST_APPLY_COMMAND_RUN` — command, exit code, stdout/stderr truncated
- [ ] `TEST_RUN` — command, result
- [ ] `EXECUTION_COMPLETE` — with `execution_performed=true`, file list, exit codes
- [ ] `ROLLBACK_TRIGGERED` and `ROLLBACK_COMPLETE` — if anything failed
- [ ] `execution_performed=true` must be set only if at least one file was actually modified
- [ ] All audit entries go to `.logs/audit.jsonl` (JSONL, append-only)

---

## 6. Test Requirements

Before any execution gate is trusted in a live run, the following test coverage must exist:

- [ ] Preflight tests pass — boundary check, rollback setup, command whitelist
- [ ] Actual mutation test: file is copied correctly to target
- [ ] Post-mutation state test: target file content matches source
- [ ] Rollback test: after mutation, rollback restores exact original state
- [ ] No-regression test: files outside allowed_paths are not touched
- [ ] Exit code test: execution returns 0 only if all steps succeeded
- [ ] Audit log test: all required events are appended in correct order
- [ ] These tests must run against the fixture workspace, not the live workspace

---

## 7. Abort Conditions

Execution must abort immediately if any of the following are true:

- [ ] Source file does not exist at time of copy
- [ ] Target path is not within allowed_paths (even by one character)
- [ ] Any review has `decision=BLOCK` or `decision=HOLD`
- [ ] Validator has `decision=BLOCK`
- [ ] `human_confirmation=REQUIRED` and no explicit GO recorded
- [ ] Rollback snapshot could not be created
- [ ] A post-apply command returns non-zero exit code
- [ ] A test command returns non-zero exit code
- [ ] Unexpected file diff detected (target already exists with unexpected content)
- [ ] Any command attempts to touch a forbidden path
- [ ] Audit log is not writable

Abort behavior:
- Trigger rollback immediately
- Append `EXECUTION_ABORTED` to audit log with reason
- Return exit 1
- Do not attempt partial completion

---

## 8. First Safe D-Phase Candidate

When execution gate is eventually built, the first live test must be:

- Intent: `2026-06-03-001` (APPROVE trace — already reviewed and passed)
- Operation: copy `.fixtures/manual_e2e/staged/status_note.html`
          → `.fixtures/manual_e2e/workspace/status_note.html`
- Change type: `create`
- Allowed paths: `.fixtures/manual_e2e/`
- Forbidden: any path outside `.fixtures/manual_e2e/`
- Must verify: file content matches, workspace was empty before, audit log updated
- Must test rollback immediately after: remove the file, confirm workspace is empty again
- Must not touch: `.workspace/app.py`, `tests/`, `.logs/sentinel.log`, any production path

This is the minimum viable first cut.

---

## Checklist Summary

```
SCOPE
  [ ] dynamic allowed_paths check
  [ ] no path traversal
  [ ] no symlink escape
  [ ] no glob in targets
  [ ] source must exist before copy

ROLLBACK
  [ ] snapshot before mutation
  [ ] rollback tested before trust
  [ ] rollback failure = abort

COMMANDS
  [ ] whitelist enforced
  [ ] no sudo
  [ ] no network
  [ ] no service restart
  [ ] no package install

HUMAN GATE
  [ ] dry-run ALLOWED ≠ execution ALLOWED
  [ ] explicit GO required for live run
  [ ] REQUIRED confirmation is a hard block
  [ ] no self-approval by agent

AUDIT
  [ ] preflight start event
  [ ] snapshot event
  [ ] copy attempted/completed/failed events
  [ ] execution_performed=true only on actual mutation
  [ ] rollback events if triggered

TESTS
  [ ] mutation test
  [ ] rollback test
  [ ] no-regression test
  [ ] audit event sequence test

ABORT
  [ ] missing source → abort
  [ ] path outside boundary → abort
  [ ] BLOCK review → abort
  [ ] REQUIRED confirmation missing → abort
  [ ] rollback unavailable → abort
  [ ] any command fails → abort + rollback
  [ ] unexpected diff → abort + rollback
```

---

## Status

**Execution gate: NOT BUILT.**

This checklist defines what the gate must satisfy.
No item in this checklist is checked.
Building the gate begins only after this document is reviewed and accepted.

---

*C-PHASE CHECKPOINT SEALED. EXECUTION GATE STILL NOT BUILT.*
