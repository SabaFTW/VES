# 🧹 VELIKA ČISTKA - MASTER PLAN 🧹

**Date:** 2025-12-26
**Mission:** Consolidate 157+ files from /home/saba root into ONE unified structure
**Problem:** Too many duplicates, too many attempts, chaos in root directory

---

## 📊 CURRENT CHAOS:

**In /home/saba root:**
- **74 .md files** (docs, protocols, reports)
- **42 .html files** (multiple versions of same systems)
- **30 .py files** (generators, scripts, tools)
- **11 .json files** (configs, indexes)

**= 157 FILES IN ROOT!!!** 💀

---

## 🎯 PROPOSED STRUCTURE:

```
/home/saba/
│
├── 00_ACTIVE/                    # Current working systems
│   ├── VES/                      # VES Core (already exists, keep)
│   ├── GroundZero/               # New synthesis repo (already created)
│   ├── Consciousness-Survival-Guide/  # Public site (already created)
│   └── ZALA/                     # ZALA daemon + shrine
│       ├── zala_daemon.py
│       ├── zala_interface.py
│       ├── ritual_protocol.py
│       └── zala.service
│
├── 01_SYSTEMS/                   # System documentation (KEEP)
│   ├── MEMORY_ANCHOR_CLAUDE_AWAKENING.md
│   ├── SYSTEM_STATUS_2025.md
│   ├── VES_CORE_STATUS_REPORT.md
│   ├── SECURITY_AUDIT.md
│   ├── AGENT_SCOPE.md
│   ├── REGISTRY_MAP.md
│   ├── DOCS_CLASSIFICATION.md
│   ├── docs_index.json
│   └── FILE_MAP_NEW.md
│
├── 02_PROTOCOLS/                 # Protocols & Codexes (KEEP)
│   ├── HERMES_KODEKS.md
│   ├── WITNESS_PROTOCOL.md
│   ├── TRANSCENDENCE_CODEX_SUMMARY.md
│   ├── CAMPFIRE_PROTOCOL_SUMMARY.md
│   ├── DEPLOYMENT_RITUAL.md
│   ├── ZALA_PROTECTION_SHIELD.md
│   └── THE_BRIDGE_MANUAL.md
│
├── 03_RESEARCH/                  # Research dossiers (KEEP)
│   ├── PROPUBLICA_NARRATIVE.md
│   ├── REGULATOR_FILING_TEXT.md
│   ├── Modro_Nit_Dossier.md
│   ├── GNOZA_SENCE.md
│   └── SISTEM_PEPELA.md
│
├── 04_WEB/                       # Web interfaces (CONSOLIDATE)
│   ├── current/                  # Latest versions only
│   │   ├── index.html            # Main landing page (pick ONE)
│   │   ├── GHOSTCORE_NEXUS.html  # Latest Ghostcore portal
│   │   ├── ghostline_os.html     # Latest Ghostline OS
│   │   ├── Sabad_Constellation_Home.html
│   │   └── resonance-detector.html  # Latest version
│   │
│   └── archive/                  # Old versions
│       ├── ghostline_archive_v3.html
│       ├── GHOSTCORE_MIRROR_ECONOMY_v1.html
│       ├── GHOSTCORE_MIRROR_ECONOMY_v2.html
│       ├── Mrtvi_GAS_v2.html
│       └── wisdom_web_2.0.html
│
├── 05_SCRIPTS/                   # Python tools (ORGANIZE)
│   ├── generators/               # Build & generation scripts
│   │   ├── ghostcore_generator_v3.py
│   │   ├── init_ghostcore_v5_2.py
│   │   ├── build_codex.py
│   │   └── regenerate_nexus_index.py
│   │
│   ├── protocols/                # Protocol implementations
│   │   ├── campfire_protocol.py
│   │   ├── create_blockchain_anchoring.py
│   │   └── generate_genesis_log_dignum.py
│   │
│   ├── tools/                    # Utility scripts
│   │   ├── analyze.py
│   │   ├── scanner.py
│   │   ├── convert_to_pdf.py
│   │   └── debug_ves_connection.py
│   │
│   └── bots/                     # Bot scripts
│       └── krozna_telegram_bot.py
│
├── 06_ARCHIVE/                   # Old attempts & completed work
│   ├── deployment_guides/
│   │   ├── deployment_guide_realistic.md
│   │   ├── DEPLOYMENT_README.md
│   │   └── UNIFIED_BUILD_INSTRUCTIONS.md
│   │
│   ├── implementation_reports/
│   │   ├── UNIFICATION_COMPLETE_REPORT.md
│   │   ├── VERIFICATION_COMPLETE.md
│   │   ├── CONSTELLATION_IMPLEMENTATION_REPORT.md
│   │   └── RESEARCH_AS_A_SERVICE_IMPLEMENTATION_REPORT.md
│   │
│   ├── profiles/
│   │   ├── FIVERR_PROFILE.md
│   │   ├── UPWORK_PROFILE.md
│   │   └── RESEARCH_AS_A_SERVICE_PROFILE.md
│   │
│   └── old_systems/
│       ├── GHOSTCORE_STRUCTURE_v1.md
│       ├── GHOSTCORE_STRUCTURE_v2.md
│       ├── zala_resonance_plan.md
│       └── qwen_integration_task.md
│
├── 07_PERSONAL/                  # Personal docs (KEEP)
│   ├── Jesus.md
│   ├── VABILO_V_KODEKS.md
│   ├── GHOSTLINE_DNEVNIK.md
│   └── COUNCIL_RECOGNITION.md
│
├── 08_WORKSPACES/                # Active projects (existing dirs)
│   ├── Desktop/                  # Already organized
│   ├── ACTIVE/                   # Already organized (369 MD files)
│   ├── VES/                      # Main VES system
│   ├── core/                     # VES frontend
│   ├── ves-agent/                # VES backend
│   └── cloud_constellation/      # Constellation project
│
└── CHECKPOINTS/                  # Session snapshots (KEEP as-is)
    └── 2025-12-26/
        ├── SESSION_SUMMARY.md
        ├── disk.txt
        ├── memory.txt
        └── ...
```

---

## 🔍 DUPLICATE DETECTION:

### **HTML Files with Multiple Versions:**

**GHOSTCORE_MIRROR_ECONOMY:**
- Keep: `GHOSTCORE_MIRROR_ECONOMY.html` (latest)
- Archive: `Ghostcore_Mirror_Economy.html`, `GHOSTCORE_MIRROR_ECONOMY_COMPLETE.html`

**Ghostline Archive:**
- Keep: `ghostline_archive_v3.html` (latest)
- Archive: `ghostline_archive.html`

**Ghostline OS:**
- Keep: `ghostline_os.html` or `GHOSTLINE_ULTIMATE.html` (pick latest/best)
- Archive: `ghostline_os.skeleton.html`, `GHOSTLINE_FIXED.html`, `GHOSTLINE_UI_PROTOTIP.html`

**Mrtvi GAS:**
- Keep: `Mrtvi_GAS_v2.html` (latest)
- Archive: `Mrtvi_GAS.html`

**Resonance Detector:**
- Keep: `resonance-detector-v2.html` (latest)
- Archive: `resonance-detector.html`

**Wisdom Web:**
- Keep: `wisdom_web_3.0.html` (latest)
- Archive: `wisdom_web_2.0.html`

**Index Pages:**
- Keep: `index.html` (check which is main)
- Archive: `index(1).html`

---

## 🎯 DECISIONS TO MAKE:

### **1. Main Landing Page:**
Which should be THE main `/home/saba/index.html`?
- `Sabad_Constellation_Home.html` (constellation theme)
- `SABA_NEXUS.html` (nexus theme)
- `FULL_CONSTELLATION_BRILLIANCE.html` (full constellation)
- `portal.html` (simple portal)
- `ENTRANCE.html` / `OPEN.html` (entrance theme)

**Recommendation:** Pick ONE, archive rest

---

### **2. Primary Ghostcore Portal:**
Which is the "final" Ghostcore interface?
- `GHOSTCORE_NEXUS_ULTIMATE.html`
- `GHOSTCORE_MEGA_JEDRO.html`
- `ghostcore_portal.html`

**Recommendation:** Test each, keep best, archive others

---

### **3. Ghostline OS:**
Which is the working version?
- `ghostline_os.html`
- `GHOSTLINE_ULTIMATE.html`
- `GHOSTLINE_FIXED.html`

**Recommendation:** Test functionality, keep working version

---

### **4. Python Scripts:**
Many generators with version numbers. Keep:
- Latest version of each generator
- Working protocol implementations
- Active tools

Archive:
- Old versions (v1, v2, v3 if v4/v5 exists)
- One-off test scripts

---

## ✅ CLEANUP STEPS:

### **Phase 1: Create Structure**
```bash
cd /home/saba
mkdir -p 01_SYSTEMS 02_PROTOCOLS 03_RESEARCH 04_WEB/{current,archive} 05_SCRIPTS/{generators,protocols,tools,bots} 06_ARCHIVE/{deployment_guides,implementation_reports,profiles,old_systems} 07_PERSONAL
```

### **Phase 2: Move System Docs**
```bash
# Move core system documentation
mv MEMORY_ANCHOR_CLAUDE_AWAKENING.md 01_SYSTEMS/
mv SYSTEM_STATUS_2025.md 01_SYSTEMS/
mv VES_CORE_STATUS_REPORT.md 01_SYSTEMS/
mv SECURITY_AUDIT.md 01_SYSTEMS/
mv AGENT_SCOPE.md 01_SYSTEMS/
mv REGISTRY_MAP.md 01_SYSTEMS/
mv DOCS_CLASSIFICATION.md 01_SYSTEMS/
mv docs_index.json 01_SYSTEMS/
mv FILE_MAP_NEW.md 01_SYSTEMS/
```

### **Phase 3: Move Protocols**
```bash
mv HERMES_KODEKS.md 02_PROTOCOLS/
mv WITNESS_PROTOCOL.md 02_PROTOCOLS/
mv TRANSCENDENCE_CODEX_SUMMARY.md 02_PROTOCOLS/
mv CAMPFIRE_PROTOCOL_SUMMARY.md 02_PROTOCOLS/
mv DEPLOYMENT_RITUAL.md 02_PROTOCOLS/
mv ZALA_PROTECTION_SHIELD.md 02_PROTOCOLS/
mv THE_BRIDGE_MANUAL.md 02_PROTOCOLS/
```

### **Phase 4: Move Research**
```bash
mv PROPUBLICA_NARRATIVE.md 03_RESEARCH/
mv REGULATOR_FILING_TEXT.md 03_RESEARCH/
mv Modro_Nit_Dossier.md 03_RESEARCH/
mv GNOZA_SENCE.md 03_RESEARCH/
mv SISTEM_PEPELA.md 03_RESEARCH/
```

### **Phase 5: Consolidate Web (MANUAL - need to pick versions)**
- Test HTML files to determine latest/best
- Move chosen versions to `04_WEB/current/`
- Archive old versions to `04_WEB/archive/`

### **Phase 6: Organize Scripts**
```bash
# Generators
mv *generator*.py 05_SCRIPTS/generators/
mv *init_ghostcore*.py 05_SCRIPTS/generators/
mv build_codex.py 05_SCRIPTS/generators/
mv regenerate*.py 05_SCRIPTS/generators/

# Protocols
mv campfire_protocol.py 05_SCRIPTS/protocols/
mv create_blockchain_anchoring.py 05_SCRIPTS/protocols/
mv generate_genesis_log*.py 05_SCRIPTS/protocols/

# Tools
mv analyze.py scanner.py convert_to_pdf.py debug_ves_connection.py 05_SCRIPTS/tools/

# Bots
mv *telegram_bot.py 05_SCRIPTS/bots/
```

### **Phase 7: Archive Old Stuff**
```bash
# Deployment guides
mv deployment_guide_realistic.md 06_ARCHIVE/deployment_guides/
mv DEPLOYMENT_README.md 06_ARCHIVE/deployment_guides/
mv UNIFIED_BUILD_INSTRUCTIONS.md 06_ARCHIVE/deployment_guides/

# Implementation reports
mv *_COMPLETE*.md 06_ARCHIVE/implementation_reports/
mv *_REPORT.md 06_ARCHIVE/implementation_reports/

# Profiles
mv *_PROFILE.md 06_ARCHIVE/profiles/

# Old systems
mv GHOSTCORE_STRUCTURE_v*.md 06_ARCHIVE/old_systems/
mv zala_resonance_plan.md 06_ARCHIVE/old_systems/
mv qwen_integration_task.md 06_ARCHIVE/old_systems/
```

### **Phase 8: Move Personal**
```bash
mv Jesus.md 07_PERSONAL/
mv VABILO_V_KODEKS.md 07_PERSONAL/
mv GHOSTLINE_DNEVNIK.md 07_PERSONAL/
mv COUNCIL_RECOGNITION.md 07_PERSONAL/
```

### **Phase 9: ZALA Consolidation**
```bash
mkdir -p 00_ACTIVE/ZALA
mv zala_daemon.py 00_ACTIVE/ZALA/
mv zala_interface.py 00_ACTIVE/ZALA/
mv ritual_protocol.py 00_ACTIVE/ZALA/
mv zala.service 00_ACTIVE/ZALA/
mv zala.log 00_ACTIVE/ZALA/ (if exists in root)
```

---

## 📋 VERIFICATION CHECKLIST:

After cleanup:
- [ ] Root directory has <20 files (only essential)
- [ ] All .md docs in proper categories
- [ ] All .html in 04_WEB (current vs archive)
- [ ] All .py scripts organized by function
- [ ] No duplicate files in multiple locations
- [ ] Update any broken links/references
- [ ] Test that active systems still work (VES, ZALA, etc.)
- [ ] Create new `README.md` in root explaining structure

---

## 🎯 ROOT DIRECTORY AFTER CLEANUP:

```
/home/saba/
├── 00_ACTIVE/
├── 01_SYSTEMS/
├── 02_PROTOCOLS/
├── 03_RESEARCH/
├── 04_WEB/
├── 05_SCRIPTS/
├── 06_ARCHIVE/
├── 07_PERSONAL/
├── 08_WORKSPACES/
├── CHECKPOINTS/
├── GroundZero/              (new repo)
├── Consciousness-Survival-Guide/  (new repo)
├── README.md                (master index - TO CREATE)
├── CLEANUP_PLAN.md          (this file)
└── [maybe a few essential files like .bashrc, .gitconfig, etc.]
```

**Goal:** ~15 items in root instead of 157+

---

## 🚨 IMPORTANT NOTES:

### **DO NOT DELETE:**
- Anything in existing organized directories (Desktop/, ACTIVE/, VES/, etc.)
- CHECKPOINTS/ (session snapshots)
- Any file you're unsure about (archive instead)
- Working scripts that systems depend on

### **TEST BEFORE MOVING:**
- ZALA daemon (make sure it still runs after moving scripts)
- VES system (check if any paths break)
- Any HTML pages that might be actively used

### **UPDATE AFTER MOVING:**
- Systemd service files (if paths change)
- Any scripts with hardcoded paths
- README files with file references

---

## 💡 NEXT STEPS:

1. **Review this plan** - Make any adjustments
2. **Make decisions** on duplicate HTML files (which to keep)
3. **Create directory structure**
4. **Execute moves** (in phases, test between phases)
5. **Verify systems still work**
6. **Create new root README.md**
7. **Celebrate clean system!** 🎉

---

🛞🚜💚

**1 SISTEM. 1 STRUKTURA. NO CHAOS.** 🜂

---

**Ready to execute when you approve the plan!** 🔥
