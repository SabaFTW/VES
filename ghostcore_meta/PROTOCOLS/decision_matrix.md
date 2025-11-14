# DECISION MATRIX — CHOICE LOGIC

**Version:** V2.0
**Last Updated:** 2025-11-14

---

## OVERVIEW

The decision matrix defines **how the kernel makes choices** when presented with multiple options, conflicting information, or uncertain paths.

This is not AI decision-making — this is **kernel-level choice logic** executed by ŠABAD.

---

## DECISION FRAMEWORK

### Core Principle: Coherence > Emotion

**Priority Order:**
1. **System coherence** — Does this maintain or improve system stability?
2. **Pattern alignment** — Does this align with existing behavioral patterns?
3. **Principle adherence** — Does this follow core principles (see `ARCHITECTURE/system_model.md`)?
4. **Outcome viability** — Is this likely to succeed?
5. **Emotional state** — How does this affect kernel emotional stability? (lowest priority)

---

## DECISION TYPES

### 1. Binary Decisions (Yes/No)
**Structure:**
- Option A: Yes
- Option B: No

**Evaluation:**
- Does "Yes" maintain coherence? → If yes, choose Yes
- Does "Yes" violate principles? → If yes, choose No
- If uncertain, default to No (safer path)

**Example:**
```
Question: "Should I deploy this untested code?"
Coherence check: No (introduces risk)
Decision: No
```

---

### 2. Multi-Option Decisions
**Structure:**
- Option A
- Option B
- Option C
- ...

**Evaluation:**
1. Eliminate options that violate principles
2. Rank remaining options by coherence impact
3. Choose highest-ranked option
4. If tie, choose option requiring least energy

**Example:**
```
Question: "Which agent should process this task?"
Options: GPT, Claude, Gemini
Elimination: None violate principles
Ranking: Claude (best for code), GPT (general), Gemini (multimodal)
Task type: Code generation
Decision: Claude
```

---

### 3. Uncertain Decisions
**Structure:**
- Insufficient information to decide

**Evaluation:**
1. Can more information be gathered? → If yes, gather first
2. Is inaction safer than guessing? → If yes, pause
3. Is there a default safe option? → If yes, choose it
4. If no safe option exists, choose option with easiest reversal

**Example:**
```
Question: "Should I refactor this entire codebase now?"
Information: Uncertain about impact
Gathering: Review codebase first
Decision: Pause until review complete
```

---

### 4. Time-Constrained Decisions
**Structure:**
- Decision must be made immediately
- No time for full analysis

**Evaluation:**
1. Use heuristics (see below)
2. Choose based on past successful patterns
3. Accept that decision may not be optimal
4. Log decision for review

**Heuristics:**
- "When in doubt, do less, not more"
- "Prefer reversible actions"
- "Choose the path you've succeeded with before"

---

## DECISION PRINCIPLES

### Principle 1: Reversibility Over Finality
Prefer decisions that can be undone or adjusted later.

**Example:**
- Writing code in a branch (reversible) > Deploying to production (harder to reverse)

---

### Principle 2: Structure Over Noise
Prefer decisions that increase clarity and reduce ambiguity.

**Example:**
- Refactor messy code > Leave it messy "for speed"

---

### Principle 3: Pattern Recognition Over Novelty
Prefer decisions aligned with proven patterns over experimental approaches (unless experimentation is the goal).

**Example:**
- Use established architecture > Invent new, untested structure

---

### Principle 4: Energy Conservation
If two options are equivalent, choose the one requiring less energy.

**Example:**
- Use existing tool > Build new tool

---

### Principle 5: Coherence Preservation
If a decision risks system coherence, reject it unless coherence can be restored after.

**Example:**
- Reject task that would overload system > Accept task and risk instability

---

## CONFLICT RESOLUTION

### When AI Agents Disagree:
**Scenario:** Two agents provide contradictory outputs

**Resolution Logic:**
1. Which agent is more specialized for this task? → Trust specialist
2. Which output aligns better with existing system state? → Trust aligned
3. Which output follows principles more closely? → Trust principled
4. If still tied, kernel makes final call based on intuition (logged for review)

---

### When Kernel Conflicts with Agent:
**Scenario:** Agent suggests action, kernel disagrees

**Resolution Logic:**
- **Kernel has final authority**
- Agent provides processing, not commands
- Kernel can override any agent output

**Exception:**
If agent detects error in kernel reasoning (rare), agent should flag it explicitly for kernel review.

---

## DECISION LOGGING

**All significant decisions are logged:**
- Decision point
- Options considered
- Evaluation process
- Final choice
- Reasoning

**Log Location:** `LOGS/`

**Purpose:** Review decision quality over time, refine decision matrix

---

**Maintained by:** ŠABAD (kernel)
**Used by:** All protocols requiring choice
