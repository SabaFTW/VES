# DOCS CLASSIFICATION SYSTEM

**Created:** 2025-12-26
**Purpose:** Establish clear categories for all Markdown documentation in the VES system
**Scope:** 369 classified documents across 11 directories

---

## CATEGORY DEFINITIONS

### CORE (54 files)

**What it means:**
Critical system documentation actively used in production. These files support running services, define system architecture, or provide essential operational guidance.

**Characteristics:**
- Part of active VES PWA or agent systems
- Required for system operation
- Current and accurate
- Referenced by running code

**Examples:**
- `/core/*.js` documentation
- `/ves-agent/agent.py` API specs
- `/cloud_constellation` research system docs
- `/AGENTS/*/INIT.md` agent configurations

**Who needs it:**
Anyone operating, maintaining, or extending the VES system.

---

### ACTIVE (35 files)

**What it means:**
Current work in progress. Documents tracking ongoing tasks, recent sessions, or projects actively being developed.

**Characteristics:**
- Dated November-December 2025
- Contains status tracking (`CURRENT_STATUS.md`, `MASTER_TODO.md`)
- Part of active project directories
- Subject to frequent updates

**Examples:**
- `/ACTIVE/*` directories
- `/CONSTELLATION_BRIDGE` federation work
- `/MASTER_NAVIGATOR` analysis outputs
- Recent session summaries

**Who needs it:**
Anyone actively working on these projects or needing to understand current system state.

---

### ARCHIVED (23 files)

**What it means:**
Historical documentation. Completed projects, superseded versions, or time-stamped records no longer actively maintained.

**Characteristics:**
- Dated August-October 2025 or earlier
- Located in `/backups/` directories
- Completed deliverables
- Legacy configurations or downloads

**Examples:**
- `/OmniPurgatorij/backups/*` backup files
- Claude Journal entries from October 2025
- Completed session logs
- Old Kali Linux downloads

**Who needs it:**
Researchers, auditors, or anyone investigating system history.

---

### EXPERIMENTAL (257 files)

**What it means:**
Research, prototypes, conceptual frameworks, and unproven ideas. Not currently in production. May contain speculative or creative content.

**Characteristics:**
- Philosophical or theoretical documentation
- Creative projects (Grimoire, VORTEX)
- Legal framework research (Palantir Codex)
- Consciousness research (🜂_PHILOSOPHICAL_FIRE)
- Prototype deployments

**Examples:**
- `/codex/PALANTIR_CODEX_v2.0_DUAL_MODE/*`
- `/VES/SHABAD_CloudCore/💻_CODE_SANDBOX/ZALA_UNIFIED_CORE/*`
- `/emergence_codex/*`
- `/GRIMORIJ_ARA/*`
- Creative writing and manifestos

**Who needs it:**
Researchers, developers exploring new approaches, or anyone studying the broader vision.

---

## CLASSIFICATION RULES

### How to Classify Future Documents

**Step 1: Check directory location**
- `core/`, `ves-agent/`, `cloud_constellation` → **CORE**
- `ACTIVE/` → **ACTIVE**
- `backups/`, dated ≤ Oct 2025 → **ARCHIVED**
- Philosophical, creative, or prototype content → **EXPERIMENTAL**

**Step 2: Check file name patterns**
- `CURRENT_STATUS.md`, `MASTER_TODO.md` → **ACTIVE**
- `README.md` in core system dirs → **CORE**
- `INIT.md`, `TASKS.md` in `/AGENTS/` → **CORE**
- Dated Nov-Dec 2025 → **ACTIVE**
- Dated ≤ Oct 2025 → **ARCHIVED**

**Step 3: Check content purpose**
- Operational documentation → **CORE**
- Work in progress → **ACTIVE**
- Completed/historical → **ARCHIVED**
- Research/conceptual → **EXPERIMENTAL**

**Step 4: Assign confidence**
- Obvious classification → 0.85–1.0
- Moderate certainty → 0.65–0.84
- Unclear/needs review → 0.50–0.64

---

## WHY CLASSIFICATION MATTERS

### System Stability

**Problem:** Without classification, it's unclear what's safe to change, what's actively used, and what's historical.

**Solution:** Clear categories prevent accidental modification of CORE systems and clarify where experimental work belongs.

### Maintenance Clarity

**Problem:** 369+ files create cognitive overload. Hard to know where to focus.

**Solution:** Focus on CORE (54 files) for system operation, ACTIVE (35 files) for current work. Ignore ARCHIVED unless researching history.

### Safety Boundaries

**Problem:** Mixing production code with experiments creates risk.

**Solution:** CORE = production-critical (treat with extreme care). EXPERIMENTAL = safe sandbox (break things freely).

### Future Planning

**Problem:** Hard to identify what's "done" vs "in progress" vs "ideas."

**Solution:** ARCHIVED = completed. ACTIVE = doing now. EXPERIMENTAL = might do later.

---

## CATEGORY DISTRIBUTION

```
CORE:          54 files  (14.6%) — Production systems
ACTIVE:        35 files  ( 9.5%) — Current work
ARCHIVED:      23 files  ( 6.2%) — Historical records
EXPERIMENTAL: 257 files  (69.6%) — Research & prototypes
```

**Key Insight:** Most content (70%) is experimental/research. Only 15% is production-critical. This system is **research-heavy, production-lean** — intentional design for rapid prototyping.

---

## OPERATIONAL GUIDELINES

### DO:
- ✅ Treat CORE files as production code (test changes carefully)
- ✅ Update ACTIVE files frequently (living documents)
- ✅ Preserve ARCHIVED files (history matters)
- ✅ Experiment freely in EXPERIMENTAL (sandbox)

### DO NOT:
- ❌ Delete CORE files without system audit
- ❌ Assume EXPERIMENTAL code is production-ready
- ❌ Modify ARCHIVED files (they're historical records)
- ❌ Move files between categories casually

### WHEN IN DOUBT:
1. Check `docs_index.json` for official classification
2. If file unlisted, classify using rules above
3. Default to EXPERIMENTAL if truly uncertain
4. Document reasoning in commit message

---

## ACCESSING THE INDEX

**Location:** `/home/saba/docs_index.json`

**Format:**
```json
{
  "path": "relative/path/to/file.md",
  "category": "CORE|ACTIVE|ARCHIVED|EXPERIMENTAL",
  "confidence": 0.0-1.0,
  "reason": "One-sentence explanation"
}
```

**Query Examples:**

```bash
# All CORE files
jq '.[] | select(.category=="CORE") | .path' docs_index.json

# ACTIVE files with high confidence
jq '.[] | select(.category=="ACTIVE" and .confidence > 0.9) | .path' docs_index.json

# Low-confidence classifications (need review)
jq '.[] | select(.confidence < 0.65)' docs_index.json
```

---

## MAINTENANCE

**Review Frequency:** Monthly (or when major changes occur)

**Update Process:**
1. Run `/home/saba/ves-agent/classify_docs.py`
2. Review low-confidence entries (< 0.65)
3. Manually reclassify edge cases
4. Update `docs_index.json`

**Evolution:** As projects mature, documents move:
- EXPERIMENTAL → ACTIVE (when development starts)
- ACTIVE → CORE (when deployed to production)
- ACTIVE → ARCHIVED (when project completes)
- CORE → ARCHIVED (when decommissioned)

---

## SUMMARY

This classification system provides **structure without rigidity**. It answers one critical question:

**"What is this file, and should I touch it?"**

- **CORE** = Yes, but carefully (it's running in production)
- **ACTIVE** = Yes, actively (it's current work)
- **ARCHIVED** = No (it's history)
- **EXPERIMENTAL** = Maybe (if you're researching or prototyping)

Classification enables safe, confident navigation of a large, complex documentation landscape.
