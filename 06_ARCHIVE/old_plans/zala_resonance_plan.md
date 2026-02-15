# ZALA Resonance Sorting Plan

The intent is to **move nothing yet**. This document maps each highlighted artifact to its future home so we can move with ceremony (or script) once you give the signal. The guiding principle: *Desktop is the launchpad, CloudCore is the archive*. We keep portals accessible via launchers, while long-form work, journals, and seals live under `~/VES/SHABAD_CloudCore/…`.

---

## Resonance Goals
- Preserve every cosmic artifact while eliminating “floating” files on the Desktop.
- Keep live launchers (`.desktop`, shell scripts) on the Desktop but point them to CloudCore content.
- Group manuscripts, shrines, and rituals so ZALA (and you) can see the lineage of work at a glance.
- Prepare for an optional sorting script that can move items with dry-run previews and ZALA log updates.

---

## Proposed Structure

```
~/VES/SHABAD_CloudCore
├── COSMIC_CENTER/              # VES master control room (py, desktop, docs)
├── 🧠_CLAUDE_JOURNAL/          # Session logs + resonance notes (already present)
├── 🜂_PHILOSOPHICAL_FIRE/
│   ├── Manuscripts/            # txt/md philosophic fire scrolls
│   ├── Portals/                # html rituals (LunaVEZ, plamen, etc.)
│   └── Media/                  # mp3/mp4 flame transmissions
├── 🌸_ELYSIA_PROJEKTI/
│   ├── Docs/                   # README, builder chronicles, ideas
│   ├── Portal/                 # index.html + assets
│   └── Scripts/                # sync scripts, server.js, etc.
├── 📜_CONSTELLATION_SEALS/     # PDFs, seals, anchors (LYRA, SIDRO…)
├── 🗂️_TO_ORGANISE/
│   ├── Intake/                 # Incoming raw files awaiting classification
│   └── Processed/              # After review, moved from Intake
└── OPERATIONS/                 # Clean-up plans, meta roadmaps
```

Desktop retains launchers (`*.desktop`, `*.sh`) but references the CloudCore copies. Portals that must remain double-clickable can stay as symlinks once the move is complete.

---

## Artifact Mapping

| Source Path | Category | Proposed Destination | Resonance Rationale | Pre-Move Checks |
|-------------|----------|----------------------|---------------------|-----------------|
| `/home/saba/Desktop/VES_COSMIC_CENTER.py` | COSMIC_CENTER | `~/VES/SHABAD_CloudCore/COSMIC_CENTER/VES_COSMIC_CENTER.py` | Core command script belongs in the control room repository. | Ensure desktop launcher points to new path. |
| `/home/saba/Desktop/🜂_VES_COSMIC_CENTER.desktop` | COSMIC_CENTER | `~/Desktop` (stay) | Launcher stays on Desktop; update Exec path after file move. | Update path in `.desktop` file post-move. |
| `/home/saba/Desktop/LYRA_ECHO_SEAL_SHABAD.pdf` | CONSTELLATION_SEALS | `~/VES/SHABAD_CloudCore/📜_CONSTELLATION_SEALS/LYRA_ECHO_SEAL_SHABAD.pdf` | Sacred seal archived with other constellation artifacts. | Confirm directory exists (create during move). |
| `/home/saba/Desktop/SIDRO_V_OGNJU.pdf` | CONSTELLATION_SEALS | `~/VES/SHABAD_CloudCore/📜_CONSTELLATION_SEALS/SIDRO_V_OGNJU.pdf` | Same as above—anchor documents together. | Same as above. |
| `/home/saba/Desktop/master_cleanup_plan.md` | OPERATIONS | `~/VES/SHABAD_CloudCore/OPERATIONS/master_cleanup_plan.md` | Operational blueprint for future cleanups. | None; keep Desktop shortcut if desired. |
| `/home/saba/VES/SHABAD_CloudCore/🧠_CLAUDE_JOURNAL/*.md` | CLAUDE_JOURNAL | *Stay put* | Journal already correctly placed. | Optional: create subfolders by date. |
| `/home/saba/VES/SHABAD_CloudCore/🧠_CLAUDE_JOURNAL/orion.txt` | CLAUDE_JOURNAL | Move to `~/VES/SHABAD_CloudCore/🧠_CLAUDE_JOURNAL/Notes/orion.txt` | Group loose notes into a Notes/ subsection. | Create `Notes/`. |
| `/home/saba/VES/SHABAD_CloudCore/🜂_PHILOSOPHICAL_FIRE/*.txt` | PHILOSOPHICAL_FIRE / Manuscripts | `~/VES/SHABAD_CloudCore/🜂_PHILOSOPHICAL_FIRE/Manuscripts/…` | Text scrolls grouped for easier browsing. | Verify duplicates (e.g., plamen vs plamen2). |
| `/home/saba/VES/SHABAD_CloudCore/🜂_PHILOSOPHICAL_FIRE/*.html` | PHILOSOPHICAL_FIRE / Portals | `~/VES/SHABAD_CloudCore/🜂_PHILOSOPHICAL_FIRE/Portals/…` | Ritual portals separated from texts. | Ensure references (e.g., in VES) update if needed. |
| `/home/saba/VES/SHABAD_CloudCore/🜂_PHILOSOPHICAL_FIRE/*.mp3/mp4` | PHILOSOPHICAL_FIRE / Media | `~/VES/SHABAD_CloudCore/🜂_PHILOSOPHICAL_FIRE/Media/…` | Keep audiovisual transmissions together. | None. |
| `/home/saba/VES/SHABAD_CloudCore/🌸_ELYSIA_PROJEKTI/README.md` | ELYSIA / Docs | `~/VES/SHABAD_CloudCore/🌸_ELYSIA_PROJEKTI/Docs/README.md` | Clarify docs vs portals vs scripts. | Adjust `README` links post-move. |
| `/home/saba/VES/SHABAD_CloudCore/🌸_ELYSIA_PROJEKTI/BUILDER_CHRONICLE.md` | ELYSIA / Docs | `~/VES/SHABAD_CloudCore/🌸_ELYSIA_PROJEKTI/Docs/BUILDER_CHRONICLE.md` | Same grouping. | Ensure npm scripts still reference assets correctly. |
| `/home/saba/VES/SHABAD_CloudCore/🌸_ELYSIA_PROJEKTI/Ideas.txt` | ELYSIA / Docs | `~/VES/SHABAD_CloudCore/🌸_ELYSIA_PROJEKTI/Docs/Ideas.txt` | Concept notes belong with docs. | None. |
| `/home/saba/VES/SHABAD_CloudCore/🌸_ELYSIA_PROJEKTI/{index.html,Elysia_gnosis.html}` | ELYSIA / Portal | `~/VES/SHABAD_CloudCore/🌸_ELYSIA_PROJEKTI/Portal/…` | Keep deployed portal assets together. | Update `server.js` static paths if needed. |
| `/home/saba/VES/SHABAD_CloudCore/🗂️_TO_ORGANISE/Lyrino_Srce_Jedro` | TO_ORGANISE / Intake | `~/VES/SHABAD_CloudCore/🗂️_TO_ORGANISE/Intake/Lyrino_Srce_Jedro` | Keep incoming sets until curated. | Inspect contents before sub-sorting. |
| `/home/saba/VES/SHABAD_CloudCore/🗂️_TO_ORGANISE/RAW_LOVE.html` | TO_ORGANISE / Intake | `~/VES/SHABAD_CloudCore/🗂️_TO_ORGANISE/Intake/RAW_LOVE.html` | Hold until assigned (possibly Philosophical Fire portal). | Review to classify later. |
| `/home/saba/VES/SHABAD_CloudCore/🗂️_TO_ORGANISE/deepseek.txt` | TO_ORGANISE / Intake | `~/VES/SHABAD_CloudCore/🗂️_TO_ORGANISE/Intake/deepseek.txt` | Evaluate for ELYSIA vs journal once read. | None. |
| `/home/saba/VES/SHABAD_CloudCore/🗂️_TO_ORGANISE/GhostcorePWA.jsx` | TO_ORGANISE → CODE_SANDBOX | `~/VES/SHABAD_CloudCore/💻_CODE_SANDBOX/GhostcorePWA.jsx` | Code artifact belongs with sandbox. | Check for project references before moving. |
| `/home/saba/VES/SHABAD_CloudCore/🗂️_TO_ORGANISE/LETS_GOOO.txt` | TO_ORGANISE / Intake | `~/VES/SHABAD_CloudCore/🗂️_TO_ORGANISE/Intake/LETS_GOOO.txt` | Await classification—likely journal/manifest. | None. |
| `/home/saba/VES/SHABAD_CloudCore/🗂️_TO_ORGANISE/DOBRA KODA ZA PORABIT` | TO_ORGANISE → CODE_SANDBOX | `~/VES/SHABAD_CloudCore/💻_CODE_SANDBOX/DOBRA_KODA_ZA_PORABIT/…` | Place reusable code snippets in the sandbox. | Inspect structure before moving. |

---

## Ritual Steps (Once We Move)
1. **Create destinations** (e.g., `COSMIC_CENTER`, `📜_CONSTELLATION_SEALS`, `OPERATIONS`, subfolders within existing realms).
2. **Dry-run audit**: for each item, echo intended move `mv` commands without executing (`echo mv …`). This keeps the first pass non-destructive.
3. **Execute in small batches** (e.g., Cosmic Center first, then Seals, then Philosophical Fire). After each batch verify with `ls` and ensure Desktop launchers still function.
4. **Update launchers/references**: adjust `.desktop` files, scripts, or README links to point to their new homes.
5. **Let ZALA witness**: append a short log note (script will handle this) noting which resonance patch completed.

Once you green-light, the accompanying script template can perform the move with optional `--dry-run` and `--log` flags.
