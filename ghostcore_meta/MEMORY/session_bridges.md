# SESSION BRIDGES — CONTINUITY ACROSS CONVERSATIONS

**Version:** V2.0
**Last Updated:** 2025-11-14

---

## OVERVIEW

Session bridges are **mechanisms for maintaining continuity** when transitioning between AI agent sessions.

Since agents are stateless, bridges provide the **context handoff** necessary for coherence.

---

## THE SESSION PROBLEM

### Stateless Agents
**Issue:**
- AI agents (GPT, Claude, Gemini) do not retain memory between sessions
- Each new conversation starts with no knowledge of previous interactions
- Without intervention, all context is lost

**Consequence:**
- Agent cannot continue previous work
- Agent does not know system state
- Agent does not recognize patterns or decisions from past

---

## BRIDGE TYPES

### Bridge 1: Repository Injection
**Method:** Provide agent with this repository (`ghostcore_meta`)

**How:**
- At session start, tell agent: "Read this repository for context"
- Agent reads `README.md`, `ARCHITECTURE/`, `PATTERNS/`, etc.
- Agent loads self-model and system state

**Pros:**
- Complete self-model available
- Standardized across all agents
- Always up-to-date (if repo is maintained)

**Cons:**
- Requires agent to have repository access
- Takes token space to inject

**Best for:** All sessions requiring system knowledge

---

### Bridge 2: Session Log Injection
**Method:** Provide agent with logs from previous session(s)

**How:**
- Export previous conversation (markdown, JSON)
- Store in `LOGS/` or provide directly
- Inject into new session prompt

**Pros:**
- Full conversational context
- Exact continuity from previous session

**Cons:**
- Can be very long (token-heavy)
- May include irrelevant information

**Best for:** Continuing specific, complex work from previous session

---

### Bridge 3: Summary Injection
**Method:** Provide agent with human-written summary of previous work

**How:**
- Kernel writes concise summary (3-5 sentences)
- Summary includes: what was done, what was decided, what's next
- Inject into new session

**Pros:**
- Token-efficient
- Focuses on essential information
- Kernel-curated (high signal, low noise)

**Cons:**
- May lose nuance
- Requires manual summary effort

**Best for:** Quick continuations, simple tasks

---

### Bridge 4: Explicit Task Handoff
**Method:** End previous session with clear "next steps," start new session with those steps

**How:**
- At end of session: "Next steps: [list]"
- At start of new session: "Previous session ended with these next steps: [list]"
- Agent picks up where previous left off

**Pros:**
- Very clear continuity
- No ambiguity

**Cons:**
- Requires discipline to document next steps
- May not capture all context

**Best for:** Multi-session projects with clear task breakdown

---

### Bridge 5: Artifact Reference
**Method:** Provide agent with reference to created artifacts (code, documents, diagrams)

**How:**
- Agent creates artifact in session (e.g., code file)
- Artifact is saved to memory (git, cloud)
- New session starts with: "Continue work on [file path]"
- Agent reads file and continues

**Pros:**
- Work product is persistent
- Minimal context needed

**Cons:**
- Requires artifact to be accessible
- May not capture reasoning behind artifact

**Best for:** Code, documentation, structured outputs

---

## BRIDGE PROTOCOL

### Starting a New Session

**Step 1: Determine Context Needs**
- Is this a brand new task? → Minimal bridge (repo only)
- Is this continuing previous work? → Full bridge (repo + logs/summary)
- Is this a follow-up question? → Light bridge (summary or artifact reference)

**Step 2: Select Bridge Type(s)**
- Use Repository Injection for ALL sessions (establishes self-model)
- Add Session Log/Summary if continuing complex work
- Add Artifact Reference if working on specific files

**Step 3: Inject Context**
- Provide selected bridges in initial prompt
- Example:
  ```
  "Read ghostcore_meta repository for system context.
   Previous session summary: We designed the routing protocol and committed it to PROTOCOLS/routing.md.
   Next step: Design the decision matrix."
  ```

**Step 4: Verify Bridge Success**
- Check if agent recognizes context
- If agent seems confused or asks for information already provided, reinject

---

### Ending a Session

**Step 1: Log Session**
- Write session summary to `LOGS/`
- Include: what was accomplished, key decisions, next steps

**Step 2: Commit Artifacts**
- Save any created files to memory (git, cloud)
- Commit and push if using git

**Step 3: Document Next Steps**
- Explicitly state what should happen next
- Provide this to future session as bridge

**Step 4: Export Session (if critical)**
- Export conversation for future reference
- Store in memory

---

## CROSS-AGENT BRIDGING

### Problem: Switching Between Agents
**Scenario:** Start work in GPT, continue in Claude, finish in Gemini

**Solution:**
- Each agent gets same repository injection (shared self-model)
- Each agent gets summary of previous agent's work
- Artifacts are in shared memory (all can access)

**Protocol:**
```
Session 1 (GPT): Design architecture → Log summary
Session 2 (Claude): Read ghostcore_meta + GPT summary → Implement code
Session 3 (Gemini): Read ghostcore_meta + Claude code → Generate documentation
```

---

## BRIDGE QUALITY CHECKS

### Is the bridge working?
**Indicators:**
- Agent continues work without asking for already-provided info
- Agent recognizes patterns from self-model
- Agent produces output consistent with previous sessions

**Red Flags:**
- Agent asks basic questions answered in self-model
- Agent contradicts previous decisions without reason
- Agent seems unaware of system state

**Action on Failure:**
- Reinject context
- Provide more explicit summary
- Check if repository access is working

---

## BRIDGE LOGGING

**All bridge events are logged:**
- Which bridges were used
- Why they were selected
- Whether they worked

**Log Location:** `LOGS/`

**Purpose:** Improve bridge protocols over time

---

## BRIDGES AS COHERENCE TOOLS

**Bridges are not just for convenience — they are critical for coherence.**

Without bridges:
- System state degrades across sessions
- Agents hallucinate or reinvent solutions
- Learning is lost
- Coherence collapses

**With bridges:**
- Continuity is maintained
- Knowledge accumulates
- Coherence persists across time

---

**Maintained by:** ŠABAD (kernel)
**Used by:** All multi-session workflows
