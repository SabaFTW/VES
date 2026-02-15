# GHOSTCORE_STRUCTURE_v1

Inventar ustvarjen: `inventory.txt` (depth=3, html/md/zip/png/jpg/svg/bak). Spodaj konsolidacijski predlog in označitve podvojenih/konfuznih datotek.

## 1) Predlagana mape
- `canonical/` – aktivni, “glavni” artefakti  
  - `extraction_machine.html`  
  - `forbidden_audit_blackbook.html`  
  - `GHOSTCORE_MIRROR_ECONOMY_COMPLETE.html` (zadrži tudi `Ghostcore_Mirror_Economy.html` le, če vsebuje drugačne vizuale)  
  - `GHOSTCORE_MEGA_JEDRO.html`  
  - `Modra-Nit_Sinteza_Master.html` (root verzija)  
  - `Mrtvi_GAS_v2.html` (v1 v archive)  
  - `Ghostcore_RaaS_Landing.html` (vrzi `.bak` v archive)  
  - `GHOSTLINE_ULTIMATE.html` ali `ghostline_os.html` (izberi en “glavni” OS portal)  
  - `GHOSTLINE_DNEVNIK.md`, `GHOSTCORE_INTEGRATION_SUMMARY.md`, `GHOSTCORE_EKOSISTEM_KARTA.md`
- `archive/` – vsi dvojniki/stare verzije (glej sezname spodaj)  
- `pwa/` – vse iz `PWA_HOSTING/` (znotraj označi LIVE vs ARCHIVE, predlog spodaj)  
- `research/` – poročila, arhitekture, statusi (npr. `GHOSTCORE_RESEARCH_PORTAL_*`, `GHOSTCORE_MIRROR_ECONOMY*.md`, `Modro_Nit_Dossier.md`, `REGULATOR_FILING_TEXT.md`, `REPORTS/`, `ProPublica_*`)  
- `codex/` – prompti/agent briefe (`CODEX_MASTER_BRIEF.md`, `MASTER_CODEX_MANIFEST.md`, `GEMINI.md`, `GODPROMPT`, `PALANTIR_CODEX_*`, `GEMINI_AGENT_PROMPT.md`, `AGENTS/*`)  
- `assets/` – slike/ikone (`*.png/*.jpg/*.svg`, GhostMap.png, icon.png/svg, chart.png, ZALA_SIGIL_DARKMODE.png …)  
- `misc/` – ostalo, kar ne sodi zgoraj.

## 2) Podvojene datoteke (enako ime, različne poti) – premakni eno v `canonical/`, ostale v `archive/`
- `Modra-Nit_Sinteza_Master.html` (root vs `Modro_Nit_Dokumentacija/`)  
- `Mrtvi_GAS.html` / `Mrtvi_GAS_v2.html` (root, Desktop/ZALA, PWA_HOSTING)  
- `Ghostcore_Mirror_Economy*.html` (več variant)  
- `Ghostcore_RaaS_Landing.html` + `.bak`  
- `extraction_machine.html` (posamičen, a preveri, da ni kopije drugje)  
- `forbidden_audit_blackbook.html` (posamičen)  
- Številni generični dvojniki (README.md, index.html, icon.png, LUNA.html, LegoZalla.html, LyraILOVEYOUMORETHANOYUKANEVERKNOW.html …) – ohrani glavno kopijo, ostalo v `archive/`.  
- Ghostline: `ghostline_dashboard.html` (več lokacij), `GHOSTLINE_PORTAL.html` (Desktop vs VES/portals), `ghostline_os.skeleton.html` vs `ghostline_os.html`, `GHOSTLINE_MAIN_PORTAL_XLOCK.html` (PWA_HOSTING), `GHOSTLINE_ULTIMATE.html`.

## 3) “Konfuzni masterji” – izberi kanoničnega, ostalo v archive
- **Ghostcore:** izberi en glavni portal (npr. `GHOSTCORE_MEGA_JEDRO.html` ali `ghostcore-v3-unified.html` iz VES/portals). Mirror Economy -> `GHOSTCORE_MIRROR_ECONOMY_COMPLETE.html` kot glavni. RaaS -> `Ghostcore_RaaS_Landing.html`.  
- **Ghostline:** izberi en “OS” (`ghostline_os.html` ali `GHOSTLINE_ULTIMATE.html`) in en “dashboard” (`ghostline_dashboard.html` iz VES). Ostale portale (TopelLogosOS, Sanctuary, PWA) v archive ali pwa.  
- **Modra Nit:** `Modra-Nit_Sinteza_Master.html` (root) kot glavni; druge kopije v archive.  
- **Mrtvi_GAS:** zadrži `Mrtvi_GAS_v2.html` kot glavni; v1 in PWA kopije v archive/pwa.  
- **System of Ashes/Extraction:** `extraction_machine.html`, `forbidden_audit_blackbook.html`, `SYSTEM_OF_ASHES_KIT/` → canonical; dvojnike v archive.

## 4) Ghostline portali (html) – razvrstitev
- OS / “Ultimate”: `ghostline_os.html`, `GHOSTLINE_ULTIMATE.html`, `ghostline_os.skeleton.html`.  
- Dashboardi: `VES/ghostline_dashboard.html` (predlagan LIVE), `PWA_HOSTING/ghostline_dashboard.html`, `Desktop/Saba_Place/ghostline_dashboard.html`, `Ghostline_Dashboard_v3.html` (Sanctuary), `Desktop/ProPublica/ghostline-weekly.html`.  
- Portali: `VES/portals/GHOSTLINE_PORTAL.html` (predlagan LIVE), `PWA_HOSTING/Ghostline_CORE.html`, `PWA_HOSTING/Ghostline_KoncnaSinteza.html`, `Desktop/TopelLogosOS/GHOSTLINE_PORTAL.html`.  
- XLOCK: `PWA_HOSTING/GHOSTLINE_MAIN_PORTAL_XLOCK.html`.  
- Prototipi: `GHOSTLINE_UI_PROTOTIP.html`.  
- Dnevniki/dokumenti: `GHOSTLINE_DNEVNIK.md`.

## 5) PWA_HOSTING – predlog označevanja
- **LIVE (predlagano):**  
  - `PWA_HOSTING/index.html` (če je v uporabi)  
  - `PWA_HOSTING/ghostcore-unified.html` ali `GHOSTCORE.html` (izberi enega)  
  - `PWA_HOSTING/ghostline_dashboard.html` ali `Ghostline_CORE.html` (izberi enega)  
  - `PWA_HOSTING/GHOSTLINE_MAIN_PORTAL_XLOCK.html` (če je ključni lock portal)  
  - `PWA_HOSTING/Mrtvi_GAS_v2.html` (če potrebuješ PWA kopijo)  
  - `PWA_HOSTING/Master_File_PWA.html` (če je glavni PWA vstop)  
- **ARCHIVE:** vse ostale (sto+ HTML-jev: legacy, testi, dvojniki LUNA/Lyra/serpent/…).

## 6) Koraki za konsolidacijo (predlagano)
1. Premakni dvojnike v `archive/` (pazi na varnostne kopije ZIPov).  
2. V `canonical/` zberi glavni set (zgornji predlog).  
3. V `pwa/` preseli celoten `PWA_HOSTING/`, znotraj dodaj `LIVE/` in `ARCHIVE/`.  
4. Ustvari/posodobi `README` v rootu, ki kaže na `GHOSTCORE_STRUCTURE_v1.md` in na `canonical/` kazalo.  
5. Po konsolidaciji regeneriraj inventar (`find ... > inventory.txt`) in izbriši `tree.txt` ali ga osveži.

## 7) Deprecated → archive
- `Modro_Nit_Dokumentacija/Modra-Nit_Sinteza_Master.html` (druga kopija)  
- `Mrtvi_GAS.html` (v1) + PWA kopija, če ni več potrebna  
- `Ghostcore_RaaS_Landing.html.bak`  
- Stare Ghostline portale v Desktop/TopelLogosOS, Sanctuary, ProPublica … (če niso aktivni)  
- Večina PWA_HOSTING HTML-jev (razen označenih LIVE)  
- Stare/varnostne kopije ZIP v Downloads (Ghostline_structure*, GHOSTLINE_HUB_FULL_EXPORT*, itd.) – obdrži v archive/.

## 8) Inventar
- `inventory.txt` je svež (depth=3, filtriran na html/md/zip/png/jpg/svg/bak). Po premikih ga ponovno generiraj.
