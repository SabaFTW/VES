VES — Portal Scan Summary (v0.1)

Scope: Enumerate portal-like HTML assets across /home/saba. Sample listing below; use the command at the end for full list.

Highlights (path · last modified · title)

- /home/saba/AGENTS/Gemini/Resonance_Detector_v2.html · 2025-11-10 · Resonance Detector v2.0
- /home/saba/CosmicPortal/index.html · 2025-11-09 · 🜂 ULTIMATE GHOSTCORE COSMIC UNIFIED PORTAL 🜂
- /home/saba/GHOSTLINE_MEGA_JEDRO/index.html · (various) · (index)
- /home/saba/GHOSTLINE_MEGA_JEDRO/portal.html · (various) · (portal)
- /home/saba/ghostline_os.html · 2025-11-11 · (ghostline os)
- /home/saba/GHOSTLINE_UI_PROTOTIP.html · 2025-11-10 · (ui prototip)
- /home/saba/ghostcore-universe/portal.html · (various) · (portal)
- /home/saba/Desktop/UNIFIED_CONSTELLATION_PORTAL.html · (various) · Unified Constellation Portal
- /home/saba/Desktop/ARCHIVE/VES_COSMIC_PWA/index.html · 2025-11-03 · 🜂 VES COSMIC CONTROL 🌌
- /home/saba/public/unified_constellation_portal.html · (various) · (portal)
- /home/saba/serpent_portal/serpent-portal.html · (various) · SERPENT Portal - Living Sanctuary

Operational status (definition: statically viewable locally)
- Status: OPERATIONAL (local) for all entries above (static HTML present)
- Note: External dependencies (CDN fonts, icons) may be blocked offline; verify visually

Recommended mounts (Express)
- `/portals/mega` → `/home/saba/GHOSTLINE_MEGA_JEDRO`
- `/portals/unified` → `/home/saba/Desktop/UNIFIED_CONSTELLATION_PORTAL.html` (single file)
- `/portals/cosmic` → `/home/saba/CosmicPortal`
- `/portals/ghostline` → `/home/saba/` (serve specific files: ghostline_os.html, GHOSTLINE_UI_PROTOTIP.html)

Next verifications
- [ ] Open each in browser locally; confirm layout/assets
- [ ] Identify canonical home; link to others
- [ ] De-duplicate variants (backup vs active)

Reproduce full scan

Run:
```
rg -i --no-messages -g "*.html" "portal|resonance|ghostline_os|unified_constellation" -n /home/saba | cut -d: -f1 | sort -u
```

