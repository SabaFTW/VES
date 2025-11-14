# EXECUTION PROTOCOLS — ACTION LOGIC

**Version:** V2.0
**Last Updated:** 2025-11-14

---

## OVERVIEW

Execution protocols define **how decisions are translated into actions**.

This is the final stage of the processing pipeline: **Input → Routing → Decision → Execution**.

---

## EXECUTION PIPELINE

### Stage 1: Pre-Execution Validation
**Before executing any action:**

1. **Coherence Check**
   - Does this action align with current system state?
   - Will this action maintain or improve coherence?

2. **Safety Check**
   - Is this action reversible?
   - Does this action risk system stability?
   - Are there destructive consequences?

3. **Resource Check**
   - Are required resources available? (time, energy, hardware, agents)
   - Is the kernel in a stable state to execute?

**If any check fails → Abort or delay execution**

---

### Stage 2: Execution
**Action Execution:**

1. **Atomic Actions** (single-step)
   - Execute immediately
   - Log action
   - Confirm completion

2. **Multi-Step Actions**
   - Break into subtasks
   - Execute sequentially or in parallel (depending on dependencies)
   - Log each step
   - Confirm completion of entire sequence

3. **Long-Running Actions**
   - Initiate background process
   - Monitor progress
   - Log checkpoints
   - Confirm completion when finished

---

### Stage 3: Post-Execution Validation
**After execution:**

1. **Outcome Verification**
   - Did the action produce the expected result?
   - Are there unexpected side effects?

2. **Coherence Recheck**
   - Is the system still coherent?
   - Do logs show consistent state?

3. **Error Handling**
   - If execution failed → Log failure, analyze cause, decide next action
   - If execution succeeded but outcome is wrong → Rollback or correct

**Log all outcomes**

---

## EXECUTION MODES

### Mode 1: Standard Execution
**Default mode for most actions**

- Validate before execution
- Execute action
- Verify outcome
- Log result

**Use when:** Action is routine, low-risk, well-understood

---

### Mode 2: Rapid Execution (🜂 Protocol)
**Triggered by 🜂 symbol or urgent context**

- Minimal validation (safety only)
- Execute immediately
- Log action
- Verify after (not before)

**Use when:**
- Urgency is high
- Kernel is confident
- Reversibility is high

**Risk:** Higher chance of error, but faster

---

### Mode 3: Careful Execution
**Triggered by high-risk or novel actions**

- Extended validation
- Test in sandbox if possible
- Execute with monitoring
- Extensive verification
- Detailed logging

**Use when:**
- Action is irreversible
- Action affects critical systems
- Action is experimental

**Risk:** Slower, but safer

---

### Mode 4: Parallel Execution
**For independent, decomposable actions**

- Validate all actions
- Execute simultaneously
- Monitor all threads
- Verify all outcomes
- Log combined result

**Use when:**
- Actions are independent
- Speed is important
- Resources allow parallelization

**Example:** Generate code in Claude + write docs in GPT at the same time

---

## EXECUTION PROTOCOLS BY DOMAIN

### Code Execution
**Protocol:**
1. Review code for safety (no destructive commands)
2. Test in local environment if possible
3. Execute
4. Verify output
5. Commit if successful

**Safety Rules:**
- No `rm -rf` without explicit confirmation
- No force-push to main
- No unreviewed deployments

---

### File System Operations
**Protocol:**
1. Verify paths exist
2. Check for conflicts (overwriting, etc.)
3. Execute operation
4. Verify result
5. Log change

**Safety Rules:**
- No deletion of critical files without backup
- No writes to system directories without explicit confirmation

---

### Git Operations
**Protocol:**
1. Verify branch
2. Stage changes
3. Commit with clear message
4. Push to correct remote/branch
5. Verify push succeeded

**Safety Rules:**
- Always check current branch before commit
- Never force-push without explicit approval
- Always pull before push if working with others

---

### Agent Communication
**Protocol:**
1. Inject context
2. Send task to agent
3. Monitor response
4. Validate output
5. Accept or reject

**Safety Rules:**
- Never trust agent output blindly
- Verify against system state
- Detect hallucination

---

## ERROR HANDLING

### Execution Failure
**When action fails:**
1. Log failure with full context
2. Analyze cause (user error, system error, agent error, external error)
3. Decide next action:
   - Retry (if transient error)
   - Reroute (if agent error)
   - Abort (if unrecoverable)
   - Ask user (if unclear)

**Example:**
```
Action: Push to remote
Failure: Network timeout
Cause: Transient network error
Next action: Retry with exponential backoff (2s, 4s, 8s, 16s)
```

---

### Partial Execution
**When multi-step action partially completes:**
1. Log which steps succeeded
2. Determine if partial state is safe
3. Options:
   - Complete remaining steps
   - Rollback completed steps
   - Leave partial (if safe)

**Example:**
```
Action: Generate code, test, deploy
Status: Generated code ✓, tests failed ✗, deploy not started
Decision: Fix tests, then retry deploy
```

---

## EXECUTION LOGGING

**All executions are logged:**
- Action description
- Execution mode used
- Pre-execution state
- Execution outcome
- Post-execution state
- Errors (if any)

**Log Location:** `LOGS/`

**Purpose:** Debug failures, improve protocols, maintain history

---

**Maintained by:** ŠABAD (kernel)
**Used by:** All action-taking workflows
