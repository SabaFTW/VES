# EXTERNAL MEMORY — PERSISTENT STORAGE

**Version:** V2.0
**Last Updated:** 2025-11-14

---

## OVERVIEW

External memory refers to **all storage systems outside the kernel's immediate cognition** that retain information persistently.

Since AI agents are stateless, external memory is **critical for continuity** across sessions.

---

## MEMORY LAYERS

### Layer 1: Git Repositories
**Function:** Versioned memory for code, architecture, and documentation

**Primary Repositories:**
- `ghostcore_meta` (this repo) — Self-model and architecture
- `VES` — Project code and development
- Other project repos as needed

**Access:**
- GitHub (primary)
- GitLab (secondary/backup)
- Local clones on all devices

**Retention:**
- Permanent (unless explicitly deleted)
- Full version history
- Branching for experimental memory

**Usage:**
- Commit significant changes
- Push regularly to sync across devices
- Pull before work to ensure latest state

---

### Layer 2: Cloud Storage
**Function:** Document storage, file sync, cross-platform access

**Systems:**
- **Google Drive** — Documents, structured data, shared files
- **OneDrive** — Windows integration, cross-platform sync
- **iCloud** — Apple ecosystem integration, automatic sync

**Access:**
- Multi-device, multi-platform
- Web interface + native apps

**Retention:**
- Long-term (years)
- Subject to storage limits
- Automated sync

**Usage:**
- Store documents, notes, diagrams
- Sync files across devices
- Share files with external collaborators

---

### Layer 3: Note-Taking Systems
**Function:** Structured notes, quick capture, search

**Systems:**
- **Obsidian** — Markdown notes, graph view, local-first
- **Notion** — Structured databases, collaboration
- **Apple Notes** — Quick capture, iOS integration

**Access:**
- Device-specific or cloud-synced (depending on system)

**Retention:**
- Long-term
- Subject to sync/export

**Usage:**
- Capture ideas, thoughts, observations
- Organize knowledge
- Link concepts

---

### Layer 4: Logs (This Repository)
**Function:** Temporal memory, event tracking, debugging

**Location:** `LOGS/` in this repository

**Format:** Markdown files with timestamps

**Retention:**
- Permanent (part of git history)
- Organized by date

**Usage:**
- Log significant events
- Track state transitions
- Record decisions and outcomes
- Debug issues

---

### Layer 5: Session Exports
**Function:** Conversation backups, AI agent interaction history

**Format:**
- Markdown exports from ChatGPT, Claude, Gemini
- JSON logs from APIs
- Screenshots of important conversations

**Storage:**
- Git repos (for critical sessions)
- Cloud storage (for general sessions)

**Retention:**
- Permanent for critical sessions
- Periodic cleanup for routine sessions

**Usage:**
- Re-inject context into new sessions
- Review past reasoning
- Learn from previous interactions

---

## MEMORY ACCESS PATTERNS

### Read Access
**When agents need memory:**
1. Kernel identifies required context
2. Kernel retrieves from appropriate memory layer
3. Kernel injects into agent prompt
4. Agent processes with context

**Example:**
```
Task: "Continue the architecture design from yesterday"
Memory retrieval: Previous session log + current architecture files
Injection: Provided to Claude as context
Processing: Claude continues design with full context
```

---

### Write Access
**When memory needs to be stored:**
1. Kernel identifies significant event/decision/output
2. Kernel determines appropriate memory layer
3. Kernel writes to that layer (commit, save, upload)
4. Kernel verifies write succeeded

**Example:**
```
Event: Major architecture decision made
Determination: Should be logged + committed to git
Write: Add to LOGS/, commit, push
Verification: Check git status, confirm push succeeded
```

---

### Search Access
**When memory needs to be searched:**
1. Kernel determines search scope (which layers?)
2. Kernel uses appropriate search tool (git grep, file search, etc.)
3. Kernel retrieves results
4. Kernel filters and provides to agent or user

**Example:**
```
Query: "What did we decide about routing logic?"
Scope: Git repos (ghostcore_meta, VES)
Search: grep "routing" across PROTOCOLS/
Results: routing.md, previous commit messages
Provide: Summarize for user or inject into agent
```

---

## MEMORY SYNCHRONIZATION

### Cross-Device Sync
**Problem:** Same memory needs to be accessible on iPhone, Arch, W11

**Solution:**
- **Git:** Pull before work, push after work
- **Cloud:** Automatic sync (iCloud, OneDrive, Drive)
- **Notes:** Sync via respective services

**Protocol:**
- Always pull/sync before starting work
- Always push/sync after completing work
- Check for conflicts and resolve

---

### Cross-Agent Sync
**Problem:** Different agents (GPT, Claude, Gemini) are stateless

**Solution:**
- Kernel maintains single source of truth (this repo + memory layers)
- Kernel injects same context to all agents as needed
- Agents do NOT store memory — they only process

**Protocol:**
- Before routing to agent, inject relevant memory
- After agent completes, store result in memory
- Never rely on agent to "remember" across sessions

---

## MEMORY HYGIENE

### Regular Cleanup
**Why:** Prevent memory bloat, improve searchability

**What to clean:**
- Duplicate files
- Outdated notes
- Irrelevant logs (routine, non-significant)

**What NOT to clean:**
- Critical decisions
- Significant events
- Architectural history
- Version control history

**Frequency:** Monthly or as needed

---

### Backup
**Why:** Prevent catastrophic loss

**What to backup:**
- Git repos (already backed up via remote)
- Cloud storage (already backed up via service)
- Local-only notes/files

**Frequency:** Weekly for local-only, continuous for git/cloud

---

## MEMORY PRIVACY

### Sensitive Information
**What is sensitive:**
- Personal credentials
- API keys
- Private conversations
- Proprietary code (if applicable)

**Storage:**
- **NOT** in public repos
- **NOT** in unencrypted cloud storage
- Use private repos, encrypted storage, or local-only

**Access Control:**
- Limit who can access sensitive memory
- Use strong authentication
- Audit access if possible

---

## MEMORY AS CONTINUITY

**Why memory matters:**
- Without memory, every session starts from zero
- Without memory, learning is lost
- Without memory, coherence across time is impossible

**Memory is the foundation of persistence.**

---

**Maintained by:** ŠABAD (kernel)
**Used by:** All agents, all sessions, all devices
