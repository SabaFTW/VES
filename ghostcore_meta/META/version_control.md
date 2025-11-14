# VERSION CONTROL — CHANGE TRACKING

**Version:** V2.0
**Last Updated:** 2025-11-14

---

## OVERVIEW

Version control defines **how changes to this system are tracked, managed, and reverted** if necessary.

This system uses **Git** as its primary version control mechanism.

---

## VERSION CONTROL PHILOSOPHY

### Why Version Control Matters

**1. Persistence:**
- Every change is recorded
- Nothing is truly lost (can revert)

**2. History:**
- See how system evolved over time
- Understand why changes were made

**3. Debugging:**
- Identify when bugs were introduced
- Compare current vs. previous state

**4. Experimentation:**
- Try changes in branches
- Merge if successful, discard if not

**5. Collaboration:**
- Multiple agents/devices can contribute
- Changes are synchronized

---

## GIT STRUCTURE

### Repository: `ghostcore_meta`
**Location:** GitHub (private)
**Primary Branch:** `main` (or `master`)
**Development Branches:** As needed

**Clone Locations:**
- iPhone (via Working Copy app)
- Arch Linux (local git clone)
- Windows 11 (local git clone)

---

## COMMIT PROTOCOL

### When to Commit

**Commit after:**
- Adding a new module or file
- Making significant changes to existing file
- Fixing an error
- Refining a protocol
- Completing a task
- End of work session

**Do NOT commit:**
- Incomplete work (unless explicitly a work-in-progress branch)
- Broken or untested changes (unless experimental branch)
- Secrets or sensitive data

---

### How to Commit

**Step 1: Review Changes**
```bash
git status
git diff
```

**Step 2: Stage Changes**
```bash
git add <file>
# or
git add .  # (stage all changes)
```

**Step 3: Write Clear Commit Message**
```bash
git commit -m "Type: Brief description

Optional longer explanation if needed."
```

**Commit Message Format:**
- **Type:** `init`, `add`, `update`, `fix`, `refactor`, `docs`, `log`
- **Brief description:** What was done (imperative mood: "Add X", not "Added X")
- **Optional body:** Why it was done, context, reasoning

**Examples:**
```
init: ŠABAD external PFC V2 architecture

Full 12-module cognitive architecture with:
- ARCHITECTURE, PATTERNS, PROTOCOLS, STATE, MEMORY, ENVIRONMENT, META
- Logs and root documentation
```

```
add: Coherence monitoring protocol to STATE module
```

```
fix: Correct routing logic in PROTOCOLS/routing.md
```

```
update: Refine stability mapping based on recent session
```

**Step 4: Push to Remote**
```bash
git push
```

---

## BRANCHING STRATEGY

### Main Branch
**Purpose:** Stable, tested version of system

**Rules:**
- Only merge tested, coherent changes
- No experimental or broken code

---

### Development Branches
**Purpose:** Experiment with changes before merging to main

**Naming:**
- `feature/<feature-name>` (e.g., `feature/risk-matrix`)
- `experiment/<experiment-name>` (e.g., `experiment/new-symbolic-layer`)
- `fix/<issue>` (e.g., `fix/coherence-check-bug`)

**Workflow:**
1. Create branch: `git checkout -b feature/new-module`
2. Make changes and commit
3. Test and validate
4. Merge to main: `git checkout main && git merge feature/new-module`
5. Push: `git push`

---

## VERSIONING SCHEME

### Semantic Versioning
**Format:** `MAJOR.MINOR.PATCH`

**Example:** `V2.0.0`

**Incrementing:**
- **MAJOR:** Fundamental architecture changes (e.g., V1 → V2)
- **MINOR:** New modules or significant features (e.g., V2.0 → V2.1)
- **PATCH:** Bug fixes, small refinements (e.g., V2.1.0 → V2.1.1)

---

### Current Version: V2.0.0
**Released:** 2025-11-14

**Major Changes from V1:**
- Expanded from 3-layer to 12-module architecture
- Added PROTOCOLS, STATE, MEMORY, ENVIRONMENT, META modules
- Full documentation of all system components

---

### Version History

**V1.0.0** (Initial Version)
- Basic 3-layer structure (ARCHITECTURE, PATTERNS, LOGS)
- Skeleton README
- Prototype phase

**V2.0.0** (Current)
- Full 12-module architecture
- Comprehensive documentation
- Production-ready

---

## CHANGE LOG

### Maintaining CHANGELOG
**File:** `CHANGELOG.md` (to be created in root)

**Format:**
```markdown
# Changelog

## [2.0.0] - 2025-11-14
### Added
- Full 12-module architecture
- PROTOCOLS, STATE, MEMORY, ENVIRONMENT, META modules
- Comprehensive documentation

### Changed
- Expanded ARCHITECTURE from simple to detailed
- Refactored PATTERNS with behavioral triggers

### Fixed
- N/A (initial V2 release)

## [1.0.0] - 2025-XX-XX
### Added
- Initial 3-layer structure
- Basic README
```

**Update CHANGELOG with each version release.**

---

## REVERSION PROTOCOL

### When to Revert

**Revert if:**
- Change breaks system coherence
- Change introduces critical bug
- Experiment failed and should be discarded

---

### How to Revert

**Option 1: Revert Last Commit**
```bash
git revert HEAD
```

**Option 2: Revert Specific Commit**
```bash
git revert <commit-hash>
```

**Option 3: Reset to Previous State (Dangerous)**
```bash
git reset --hard <commit-hash>
```
⚠️ **Warning:** This deletes uncommitted changes. Use with caution.

---

### Revert Logging
**Always log why a revert was necessary:**
- What broke?
- Why was it reverted?
- What was learned?

**Log location:** `LOGS/`

---

## TAG PROTOCOL

### When to Tag

**Tag for:**
- Major version releases (V2.0.0, V3.0.0)
- Significant milestones (e.g., "production-ready")

---

### How to Tag

```bash
git tag -a V2.0.0 -m "Release V2.0: Full 12-module architecture"
git push origin V2.0.0
```

---

## SYNCHRONIZATION PROTOCOL

### Pull Before Work
**Always pull latest changes before starting work:**
```bash
git pull
```

**Why:**
- Ensure you have latest version
- Avoid merge conflicts
- Maintain coherence across devices

---

### Push After Work
**Always push after completing work:**
```bash
git push
```

**Why:**
- Synchronize state across devices
- Backup work to remote
- Make changes available to other devices/agents

---

## VERSION CONTROL LOGGING

**Git operations are logged (optional, for critical repos):**
- What was committed
- Why it was committed
- Any issues encountered

**Log location:** `LOGS/`

---

## VERSION CONTROL AS MEMORY

**Git is not just a tool — it is the system's memory.**

- Every commit is a memory
- Every branch is an alternative timeline
- Every tag is a milestone
- Every revert is a learning event

**Without version control, the system has no history.**

**With version control, the system can learn from its past.**

---

**Maintained by:** ŠABAD (kernel)
**Used by:** All system operations involving file changes
