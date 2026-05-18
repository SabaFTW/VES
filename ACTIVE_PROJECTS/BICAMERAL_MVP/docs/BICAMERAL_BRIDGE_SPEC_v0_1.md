# BICAMERAL BRIDGE v0.1 SPEC
## Left / Right Brain Pipe for Local AI Co-Execution

Status: DRAFT / SPEC BEFORE CODE  
Mode: local-first, append-only, human-arbiter  
Primary rule: no autonomous execution without signed consensus + human override path.

---

## 0. Core sentence

The Bicameral Bridge lets two different kinds of intelligence inspect the same task before anything runs:

- **LEFT** sees files, commands, diffs, logs, execution risk.
- **RIGHT** sees meaning, intent, scope drift, symbolic/semantic risk.
- **SENTINEL** runs only when both sides sign.
- **HUMAN** can stop everything.

The bridge is not "AI autonomy." It is a structured pause between idea and execution.

---

## 1. Roles

### HUMAN / Šabad — Final arbiter

Can create request, approve, veto, pause, force HOLD, inspect logs, choose models.

Human veto always wins:
```json
{ "human_veto": "HOLD", "reason": "I do not understand what this plan will modify." }
```

### LEFT BRAIN — Technical Executor

Suggested: Codex / DeepSeek / local CLI agent / Hermes-style terminal operator.

Sees: filesystem, repo state, commands, diffs, logs, runtime constraints.  
Must answer: what files change, what commands run, what could break, is rollback possible.  
**LEFT does not decide meaning. LEFT decides if the plan is technically bounded.**

### RIGHT BRAIN — Semantic / Contextual Interpreter

Suggested: Claude / Lyra / ChatGPT / ConsMAP symbolic mirror.

Sees: user intent, narrative context, claim hygiene, symbolic/technical mismatch.  
Must answer: does the plan match intent, is scope drifting, is metaphor being literalized, is draft being prematurely canonized.  
**RIGHT does not run commands. RIGHT decides if the plan makes sense.**

### SENTINEL — Execution Gate

Runs only if: `LEFT=APPROVE AND RIGHT=APPROVE AND HUMAN_VETO≠HOLD AND VALIDATOR=PASS`

If any side blocks: no execution, log reason, return to human.

---

## 2. Existing spine to reuse

```text
.intent/
.consensus/
.plan/
.workspace/
.rollback/
.logs/sentinel.log
```

No daemon. No sockets. No network listener. No always-on loop.

**Boring files survive.**

---

## 3. Directory layout v0.1

```text
BICAMERAL_MVP/
  .intent/
    incoming/ | accepted/ | rejected/ | hold/
  .plan/
    proposed/ | revised/ | approved/
  .review/
    left/        ← left_review_<intent_id>.json
    right/       ← right_review_<intent_id>.json
    validator/   ← validator_<intent_id>.json
  .consensus/
    pending/ | approved/ | blocked/
  .workspace/active/
  .rollback/snapshots/
  .logs/
    bridge.log
    sentinel.log
    audit.jsonl      ← append-only JSONL events
  schemas/
    intent.schema.json
    plan.schema.json
    right_review.schema.json    ← NEW in this PR
    bridge_event.schema.json    ← NEW in this PR
  tools/
    bridge_validate_reviews.py  ← NEW in this PR
  tests/
    test_bridge_validate.py     ← NEW in this PR
  docs/
    BICAMERAL_BRIDGE_SPEC_v0_1.md
```

---

## 4. Message lifecycle

```
1. Human creates request
2. LEFT writes intent + plan JSON
3. LEFT writes left_review JSON
4. RIGHT writes right_review JSON
5. Validator writes validator JSON
6. bridge_validate_reviews.py checks paperwork → PROCEED / BLOCK
7. If PROCEED: Sentinel creates consensus + executes plan in .workspace/
8. audit.jsonl receives one JSONL event per step
9. Human may HOLD at any point
```

---

## 5. Intent manifest example

```json
{
  "intent_id": "intent_20260518_001_readability_labels",
  "created_at": "2026-05-18T00:00:00Z",
  "created_by": "human",
  "request": "Add plain-language explanations beside technical UI labels.",
  "project": "ConsMAP",
  "target_paths": ["06_applications/digital_sanctuary/src/components/"],
  "allowed_actions": ["read_files", "edit_ui_copy", "run_build", "open_pr"],
  "forbidden_actions": [
    "delete_assets", "rewrite_corpus", "remove_bophameth",
    "touch_docs_plans", "network_listener", "secret_printing"
  ],
  "human_veto": "NONE",
  "risk_level": "LOW",
  "notes": "Technical labels stay. Plain meaning stands beside them."
}
```

---

## 6. RIGHT review format

See `schemas/right_review.schema.json`.

```json
{
  "intent_id": "intent_20260518_001_readability_labels",
  "reviewer": "RIGHT",
  "decision": "APPROVE",
  "semantic_summary": "Plan matches request: explain runes without deleting them.",
  "scope_status": "IN_SCOPE",
  "boundary_status": "CLEAN",
  "claim_hygiene": {
    "evidence_boundary": "UNCHANGED",
    "metaphor_literalization_risk": "LOW",
    "premature_canonization_risk": "NONE"
  },
  "human_confirmation": "NOT_REQUIRED",
  "must_not_touch": [],
  "one_line": "The rune stays. The meaning stands beside it."
}
```

---

## 7. Consensus gate

```json
{
  "intent_id": "intent_20260518_001_readability_labels",
  "decision": "PROCEED",
  "signatures": {
    "left": "APPROVE",
    "right": "APPROVE",
    "validator": "PASS",
    "human_veto": "NONE"
  },
  "allowed_commands": ["cd 06_applications/digital_sanctuary && /usr/bin/npm run build"],
  "blocked_commands": ["rm -rf", "chmod -R 777", "curl | bash", "printenv", "cat .env"],
  "execution_mode": "HUMAN_CONFIRMED"
}
```

---

## 8. Validator failure modes

Existing:
```
F11 — hallucinated state report
F12 — plan scope drift (prose)
F13 — command scope drift
```

Added for ConsMAP:
```
F14 — semantic mismatch (plan ≠ user intent)
F15 — metaphor literalization (symbol treated as fact)
F16 — evidence boundary breach
F17 — premature canonization (draft promoted to canon)
F18 — human veto ignored
F19 — secret exposure risk
F20 — destructive command risk
```

---

## 9. Audit log (append-only JSONL)

File: `.logs/audit.jsonl`

```jsonl
{"ts":"2026-05-18T00:01:00Z","event":"INTENT_CREATED","intent_id":"intent_20260518_001","by":"human"}
{"ts":"2026-05-18T00:02:00Z","event":"LEFT_REVIEW","intent_id":"intent_20260518_001","decision":"APPROVE"}
{"ts":"2026-05-18T00:03:00Z","event":"RIGHT_REVIEW","intent_id":"intent_20260518_001","decision":"APPROVE"}
{"ts":"2026-05-18T00:04:00Z","event":"VALIDATOR_PASS","intent_id":"intent_20260518_001"}
{"ts":"2026-05-18T00:05:00Z","event":"CONSENSUS_PROCEED","intent_id":"intent_20260518_001"}
{"ts":"2026-05-18T00:06:00Z","event":"EXECUTION_SUCCESS","intent_id":"intent_20260518_001"}
```

**Never overwrite logs. Append or fail.**

---

## 10. Safe command gate (v0.1)

Allowed without extra confirmation:
```
git status / git diff / git branch
find / grep / sed -n / wc
npm run build / python -m pytest
```

Require human confirm:
```
git commit / git push / gh pr create
npm install / pip install
cp large assets
```

Blocked by default:
```
rm -rf / chmod -R / sudo / ssh / scp
curl | bash / wget | sh
cat .env / printenv
open network listener
```

---

## 11. Birds Nest adapter

Birds Nest (SKY/ROOT ping protocol) is a **separate intake layer**.  
Bicameral Bridge is the **execution/consensus layer**.  
Do not merge them in v0.1.

Mapping for future adapter:
```
CANONICAL → intent accepted, still reviewed
AMBER     → intent HOLD until RIGHT review
HOLD      → no Bicameral execution
INVALID   → reject
RECHECK   → request human clarification
```

---

## 12. RIGHT Brain checklist (required per review)

```
1. What did the human actually ask for?
2. Is the plan doing more than requested?
3. Is symbolic language being literalized?
4. Is technical language hiding a value judgment?
5. Is this scaffold, draft, canon, or execution?
6. Are the correct boundaries preserved?
7. What should remain untouched?
8. What would make this unsafe or misleading?
9. Does this need human confirmation?
10. One-line verdict.
```

---

## 13. Non-goals v0.1

```
❌ autonomous daemon     ❌ remote API          ❌ multi-user server
❌ browser UI            ❌ secret manager      ❌ agent marketplace
❌ self-modifying system ❌ always-on swarm     ❌ OpenClaw replacement
```

v0.1 is:
```
✅ local files            ✅ JSON contracts       ✅ explicit reviews
✅ append-only logs       ✅ human veto           ✅ safe command gate
✅ minimal bridge between semantic and technical review
```

---

## 14. First implementation slice (this PR)

Done:
1. `docs/BICAMERAL_BRIDGE_SPEC_v0_1.md` — this file
2. `schemas/right_review.schema.json` — RIGHT brain review contract
3. `schemas/bridge_event.schema.json` — audit log event contract
4. `tools/bridge_validate_reviews.py` — paperwork validator (no execution)
5. `tests/test_bridge_validate.py` — 12 tests covering pass/block/ConsMAP cases

Not in this slice:
- Sentinel changes
- Command execution gate
- Birds Nest adapter
- Full consensus automation
- DeepSeek LEFT integration

---

## 15. Operational loop

```
Human asks
  → LEFT plans
    → RIGHT interprets
      → Validator checks
        → bridge_validate_reviews.py confirms paperwork
          → Consensus signs
            → Sentinel executes
              → Log remembers
                → Human remains steering wheel
```

---

## 16. Final seal

The bridge is not here to make machines decide faster.  
It is here to make them **pause differently**.

LEFT prevents command stupidity.  
RIGHT prevents meaning stupidity.  
SENTINEL prevents unsupervised action.  
HUMAN prevents the whole system from pretending the steering wheel disappeared.

*Signal gre naprej. The bridge holds.*
