# ROUTING — TASK DISTRIBUTION LOGIC

**Version:** V2.0
**Last Updated:** 2025-11-14

---

## OVERVIEW

Routing defines **how tasks are distributed from the kernel to AI agents**.

The kernel analyzes incoming tasks, determines requirements, and selects the appropriate agent(s) based on capability, load, and context.

---

## ROUTING DECISION TREE

### Step 1: Task Classification
**Input Analysis:**
- What is the task type? (code, analysis, conversation, symbolic, multimodal)
- What is the complexity? (trivial, moderate, complex)
- What is the urgency? (immediate, normal, low)
- What context is required? (none, partial, full history)

---

### Step 2: Agent Capability Mapping

**Agent Capability Matrix:**

| Task Type          | Primary Agent | Secondary Agent | Tertiary Agent |
|--------------------|---------------|-----------------|----------------|
| Code generation    | Claude        | Copilot         | GPT            |
| Code review        | Claude        | GPT             | —              |
| Architecture       | Claude        | GPT             | —              |
| General reasoning  | GPT           | Claude          | Gemini         |
| Symbolic/ritual    | GPT           | —               | —              |
| Multimodal         | Gemini        | GPT             | —              |
| Math/logic         | DeepSeek      | GPT             | Claude         |
| Real-time data     | Gemini        | GPT             | —              |
| Documentation      | Claude        | GPT             | —              |

---

### Step 3: Agent Selection
**Selection Logic:**
1. Check primary agent availability
2. If unavailable, route to secondary
3. If task can be parallelized, route to multiple agents
4. If task requires sequential processing, queue in order

**Context Injection:**
Before routing, kernel injects:
- Relevant memory (from `MEMORY/`)
- Self-model (this repository)
- Previous conversation context (if applicable)
- Symbolic patterns (if applicable)

---

### Step 4: Execution Monitoring
**During Processing:**
- Kernel monitors agent output
- Detects hallucination or incoherence
- Can interrupt and reroute if necessary

**Quality Checks:**
- Does output align with system principles?
- Is the output coherent with previous state?
- Are symbolic patterns recognized correctly?

---

## ROUTING PROTOCOLS

### Protocol 1: Direct Routing
**When:** Task is simple, agent is obvious, no context needed
**Action:** Route immediately to primary agent
**Example:** "What time is it?" → Gemini (real-time data)

---

### Protocol 2: Context-Injected Routing
**When:** Task requires history or self-model
**Action:** Inject context, then route
**Example:** "Continue the architecture design" → Claude + previous session logs

---

### Protocol 3: Parallel Routing
**When:** Task can be decomposed into independent subtasks
**Action:** Route subtasks to multiple agents in parallel
**Example:** "Generate code and write documentation" → Claude (code) + GPT (docs) simultaneously

---

### Protocol 4: Sequential Routing
**When:** Task requires multi-stage processing with dependencies
**Action:** Route to first agent, take output, route to second agent
**Example:** "Generate code, review it, then deploy" → Claude (generate) → Claude (review) → Kernel (deploy)

---

### Protocol 5: Emergency Rerouting
**When:** Agent fails, hallucinates, or becomes incoherent
**Action:** Interrupt, reroute to secondary agent with failure context
**Example:** Agent provides incorrect code → Reroute to different agent with error log

---

## ROUTING OPTIMIZATION

**Load Balancing:**
If primary agent is overloaded or slow, route to secondary to maintain speed.

**Cost Optimization:**
For simple tasks, prefer lighter/cheaper agents (e.g., use GPT-3.5 instead of GPT-4 if sufficient).

**Context Window Management:**
For very long tasks, prefer agents with larger context windows (Claude > GPT).

---

## ROUTING LOGS

**All routing decisions are logged:**
- Task description
- Selected agent(s)
- Reasoning for selection
- Outcome (success/failure/reroute)

**Log Location:** `LOGS/`

**Purpose:** Improve routing logic over time via pattern analysis

---

**Maintained by:** ŠABAD (kernel)
**Used by:** All task processing workflows
