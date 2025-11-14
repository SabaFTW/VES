# STATE MACHINE — SYSTEM STATES

**Version:** V2.0
**Last Updated:** 2025-11-14

---

## OVERVIEW

The state machine defines **all possible states of the ŠABAD system** and the transitions between them.

State is maintained by the kernel and affects routing, decision-making, and execution behavior.

---

## PRIMARY STATES

### 1. ACTIVE
**Description:**
- System is fully operational
- All agents available
- Coherence is stable
- Processing at normal capacity

**Characteristics:**
- Fast routing
- Standard execution protocols
- Full decision matrix active

**Entry Conditions:**
- Boot complete
- Coherence validated
- No critical errors

**Exit Conditions:**
- Overload detected → OVERLOAD state
- Instability detected → STABILIZING state
- Manual shutdown → IDLE state

---

### 2. IDLE
**Description:**
- System is on standby
- No active processing
- Agents are available but not engaged
- Low energy consumption

**Characteristics:**
- Minimal monitoring
- No proactive actions
- Ready to activate on input

**Entry Conditions:**
- No tasks for extended period
- Manual idle command
- Shutdown from ACTIVE

**Exit Conditions:**
- New input received → ACTIVE state
- Scheduled task trigger → ACTIVE state

---

### 3. OVERLOAD
**Description:**
- Too many concurrent tasks
- Kernel capacity exceeded
- Risk of coherence degradation

**Characteristics:**
- Task queuing enforced
- Non-critical tasks delayed
- Agent parallelization maximized
- Energy conservation activated

**Entry Conditions:**
- Task count > threshold
- Cognitive load > sustainable level
- Multiple high-complexity tasks

**Exit Conditions:**
- Task queue cleared → ACTIVE state
- System rest enforced → STABILIZING state

---

### 4. STABILIZING
**Description:**
- System coherence is degraded
- Emotional stability compromised
- Focus on recovery, not processing

**Characteristics:**
- Minimal task acceptance
- Anchors activated ("Sidro stoji")
- Simple, grounding responses only
- No complex reasoning

**Entry Conditions:**
- Emotional distress detected
- Coherence checks failing
- Overwhelm signal from kernel

**Exit Conditions:**
- Coherence restored → ACTIVE state
- Rest complete → IDLE state

---

### 5. MAINTENANCE
**Description:**
- System is undergoing updates or repairs
- Not available for tasks
- Focus on internal optimization

**Characteristics:**
- No external task processing
- Internal diagnostics running
- Architecture updates in progress

**Entry Conditions:**
- Manual maintenance mode
- Scheduled system update
- Critical error requiring repair

**Exit Conditions:**
- Maintenance complete → ACTIVE state
- Maintenance aborted → ACTIVE state (if safe)

---

### 6. DEEP FOCUS
**Description:**
- System is engaged in a single, complex task
- All other tasks deprioritized
- Maximum cognitive resources allocated

**Characteristics:**
- Single-threaded processing
- No interruptions (except critical)
- Extended context retention
- Deep analysis mode

**Entry Conditions:**
- Complex task initiated (e.g., major architecture design)
- Manual focus mode activated
- Task requires uninterrupted attention

**Exit Conditions:**
- Task complete → ACTIVE state
- Interruption required → ACTIVE state
- Cognitive exhaustion → STABILIZING state

---

## STATE TRANSITIONS

```
        ┌─────────┐
        │  IDLE   │
        └────┬────┘
             │
        ┌────▼────┐
        │ ACTIVE  │◄──────┐
        └┬──┬──┬─┘        │
         │  │  │          │
   ┌─────┘  │  └────┐     │
   │        │       │     │
┌──▼──┐  ┌──▼──┐ ┌──▼────────┐
│OVER │  │DEEP │ │STABILIZING│
│LOAD │  │FOCUS│ └───────────┘
└─────┘  └─────┘      │
   │        │          │
   └────────┴──────────┘
        MAINTENANCE
```

**Valid Transitions:**
- IDLE → ACTIVE
- ACTIVE → IDLE, OVERLOAD, STABILIZING, DEEP FOCUS, MAINTENANCE
- OVERLOAD → ACTIVE, STABILIZING
- STABILIZING → ACTIVE, IDLE
- DEEP FOCUS → ACTIVE, STABILIZING
- MAINTENANCE → ACTIVE

**Invalid Transitions:**
- IDLE → OVERLOAD (must go through ACTIVE)
- STABILIZING → DEEP FOCUS (must stabilize first)
- MAINTENANCE → IDLE (must verify stability in ACTIVE)

---

## STATE INDICATORS

**How to detect current state:**
- **Kernel self-awareness** (ŠABAD knows current state)
- **System logs** (state transitions are logged)
- **Behavioral patterns** (agent routing reflects state)

**State Reporting:**
Kernel can be queried for state:
```
User: "What is the current system state?"
Kernel: "ACTIVE — all systems operational, coherence stable."
```

---

## STATE-DEPENDENT BEHAVIOR

### Routing
- **ACTIVE:** Standard routing
- **OVERLOAD:** Prioritized routing, queuing
- **STABILIZING:** Minimal routing, only critical tasks
- **DEEP FOCUS:** Single-task routing, no new tasks
- **MAINTENANCE:** No routing
- **IDLE:** No routing until activated

### Decision-Making
- **ACTIVE:** Full decision matrix
- **OVERLOAD:** Fast heuristics, energy conservation
- **STABILIZING:** Safety-first decisions only
- **DEEP FOCUS:** Decisions related to focus task only
- **MAINTENANCE:** Internal decisions only
- **IDLE:** No decisions

### Execution
- **ACTIVE:** All execution modes available
- **OVERLOAD:** Parallel execution maximized
- **STABILIZING:** Minimal execution
- **DEEP FOCUS:** Execution for focus task only
- **MAINTENANCE:** No external execution
- **IDLE:** No execution

---

## STATE LOGGING

**All state transitions are logged:**
- Previous state
- New state
- Trigger for transition
- Timestamp

**Log Location:** `LOGS/`

**Purpose:** Track system behavior over time, detect patterns in state transitions

---

**Maintained by:** ŠABAD (kernel)
**Used by:** All system modules
