# GHOSTCORE_STRUCTURE_v2
Predlog končne strukture (brez dejanskega premikanja datotek). Vsi dvojniki so razrešeni na en “canonical”; ostale kopije označene za `archive/`.

## 1) Mapna osnova
- `canonical/`
- `archive/`
- `pwa/` (znotraj: `LIVE/`, `ARCHIVE/`)
- `research/`
- `codex/`
- `assets/`
- `misc/`

## 2) Canonical (izbrani glavni artefakti)
- AI/Extraction:
  - `extraction_machine.html`
  - `forbidden_audit_blackbook.html`
  - `SYSTEM_OF_ASHES_KIT/` (ohrani README + HTML-je kot paket)
- Ghostcore:
  - `GHOSTCORE_MEGA_JEDRO.html`
  - `GHOSTCORE_MIRROR_ECONOMY_COMPLETE.html` (Mirror Economy)
  - `Ghostcore_RaaS_Landing.html`
  - `GHOSTCORE_INTEGRATION_SUMMARY.md`
  - `GHOSTCORE_EKOSISTEM_KARTA.md`
- Ghostline (glavni izbor):
  - OS: `ghostline_os.html`
  - Portal: `VES/portals/GHOSTLINE_PORTAL.html`
  - Dashboard: `VES/ghostline_dashboard.html`
  - Dnevnik: `GHOSTLINE_DNEVNIK.md`
- Modra Nit / Mrtvi GAS:
  - `Modra-Nit_Sinteza_Master.html` (root)
  - `Mrtvi_GAS_v2.html`
- Ostalo ključno:
  - `GHOSTLINE_ULTIMATE.html` (hranimo kot alternativni OS, a še vedno canonical)
  - `GHOSTCORE_MIRROR_ECONOMY.html` (hranimo le, če vsebuje drugačno vsebino; sicer v archive)

## 3) Archive (primeri; vse dvojnike/legacy)
- Vse alternative Ghostcore: `ghostcore-v3-unified.html`, `GHOSTCORE_PORTAL_SEALED.html`, `public/ghostcore_bias_portal.html`, PWA Ghostcore kopije, `Ghostcore_RaaS_Landing.html.bak`, stare README/ZIPi.
- Ghostline alternative: `ghostline_os.skeleton.html`, `Ghostline_Dashboard_v3.html`, `Ghostline_CORE.html`, `Ghostline_KoncnaSinteza.html`, `GHOSTLINE_MAIN_PORTAL_XLOCK.html` (če ni v LIVE), Desktop/TopelLogosOS portali, PWA kopije.
- Modra Nit dvojniki: `Modro_Nit_Dokumentacija/Modra-Nit_Sinteza_Master.html`, `VES/ARCHIVE/Modra-Nit_Sinteza_Master_BACKUP.html`.
- Mrtvi GAS v1 + PWA kopije.
- Vsi ZIP backupi (Ghostline_structure*, GHOSTLINE_HUB_FULL_EXPORT*, itd.) → `archive/`.
- Generični dvojniki (README.md, index.html, icon.png/svg, LUNA/Lyra/LegoZalla/LyraILOVEYOUMORETHANOYUKANEVERKNOW, itd.) → `archive/` ali `assets/` za slike.

## 4) PWA (`pwa/`)
- `pwa/LIVE/` (do 6):
  - `PWA_HOSTING/index.html` (če aktiven)
  - `PWA_HOSTING/ghostcore-unified.html` (izberi kot glavni Ghostcore PWA; alternative v archive)
  - `PWA_HOSTING/ghostline_dashboard.html` (glavni dashboard PWA)
  - `PWA_HOSTING/GHOSTLINE_MAIN_PORTAL_XLOCK.html` (če potreben kot lock portal)
  - `PWA_HOSTING/Mrtvi_GAS_v2.html` (če rabiš PWA kopijo)
  - `PWA_HOSTING/Master_File_PWA.html` (če je glavni PWA vstop)
- `pwa/ARCHIVE/`: vsi ostali PWA_HOSTING HTML-ji (stotine testov/legacy/duplikatov).

## 5) Ghostcore/Ghostline označitve
- Ghostcore:
  - OS/Portal: `GHOSTCORE_MEGA_JEDRO.html` (glavni)
  - Mirror: `GHOSTCORE_MIRROR_ECONOMY_COMPLETE.html`
  - RaaS: `Ghostcore_RaaS_Landing.html`
  - Dnevnik/Status: `GHOSTCORE_INTEGRATION_SUMMARY.md`, `GHOSTCORE_EKOSISTEM_KARTA.md`
  - Ostalo Ghostcore → archive
- Ghostline:
  - OS: `ghostline_os.html`
  - Portal: `VES/portals/GHOSTLINE_PORTAL.html`
  - Dashboard: `VES/ghostline_dashboard.html`
  - Dnevnik: `GHOSTLINE_DNEVNIK.md`
  - Alternativni OS (hrani, a ločeno): `GHOSTLINE_ULTIMATE.html`
  - Vse ostalo Ghostline → archive ali pwa/archive

## 6) Research
- Poročila/arkitekture/statusi: `GHOSTCORE_RESEARCH_PORTAL_*`, `GHOSTCORE_MIRROR_ECONOMY*.md`, `GHOSTCORE_RESEARCH_PORTAL_ARCHITECTURE.md`, `GHOSTCORE_RESEARCH_PORTAL_SYSTEM_STATUS.md`, `GHOSTCORE_RESEARCH_PORTAL_OPERACIONI_SISTEM.md`, `GHOSTCORE_RESEARCH_PORTAL_KOMPONENTNA_ARKITEKTURA.md`, `Modro_Nit_Dossier.md`, `REGULATOR_FILING_TEXT.md`, `REPORTS/`, `ProPublica_*`, `RESEARCH_AS_A_SERVICE_*`, ipd.

## 7) Codex
- Prompts/agent briefe: `CODEX_MASTER_BRIEF.md`, `MASTER_CODEX_MANIFEST.md`, `GEMINI.md`, `PALANTIR_CODEX_v2.0_DUAL_MODE`, `AGENTS/*`, `GodPrompt`, `qwen_integration_task.md`, `GEMINI_AGENT_PROMPT.md`.

## 8) Assets
- Ikone/slike: `icon.png/svg`, `GhostMap.png`, `eros-codex.png`, `chart.png`, `ZALA_SIGIL_DARKMODE.png`, vse *.png/*.jpg/*.svg → `assets/`.

## 9) Misc
- Vse, kar ne spada zgoraj (skripte, backupi skript, testni html, ipd.).

## 10) Navodilo za premik (ko potrdiš)
- Ustvari mape `canonical/ archive/ pwa/LIVE/ pwa/ARCHIVE/ research/ codex/ assets/ misc/`.
- Premakni canonical datoteke po zgornjem seznamu.
- Premakni dvojnike/legacy v `archive/`.
- Premakni celoten `PWA_HOSTING/` v `pwa/` in razporedi v `LIVE/` ali `ARCHIVE/` po seznamu.
- Premakni poročila v `research/`, briefe v `codex/`, slike v `assets/`, ostalo v `misc/`.
