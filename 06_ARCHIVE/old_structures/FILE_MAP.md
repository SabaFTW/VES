# CONSTELLATION_OS File Map

Generated: 2025-11-05  
Scope: `/home/saba/Desktop/CONSTELLATION_OS` (excludes `node_modules/` contents for brevity)

## Root Files
- `README.md` — Project overview and setup notes for Constellation OS.
- `server.js` — Unified Node.js backend (Express server, Telegram bot, auto-backups, GitHub sync).
- `start.sh` — Convenience launcher for the core server.
- `start-all.sh` — Launch script that chains multiple services/processes.
- `install-autostart.sh` — Installs `constellation.service` into systemd for auto-start.
- `constellation.service` — systemd unit definition consumed by `install-autostart.sh`.
- `telegram-bot.js` — Telegram bot integration entrypoint.
- `package.json` / `package-lock.json` — Node.js dependencies and lock file.
- `.env` / `.env.example` — Environment configuration (API keys, ports, bot tokens).
- `ELYSIA_MEGA_GUIDE.md` — Extended instructions for operating the Elysia interface.
- `GEMINI_AGENT_BRIEF.md` — Briefing document for Gemini agent responsibilities.
- `PROMPT_FOR_GEMINI.md` — Prompt template for Gemini automation flows.
- `KODEKS_CONTRIBUTIONS.md` — Contribution log and recognition ledger.
- `ves-ghostline-synthesizer/` — Ghostline Research Synthesizer package (backend Python + frontend React).

## Data Directory (`data/`)
- `constellation.json` — Primary persisted state for Constellation OS.
- `backup-*.json` — Timestamped JSON snapshots created by the auto-backup routine.

## Public Assets (`public/`)
- `index.html` — Landing page / default entry.
- `hub.html` — Hub interface served by the unified server.
- `elysia.html` — Full Elysia experience with widgets (weather, fleet status, sigil library, Lyra prompts).
- `elysia-simple.html` — Lightweight variant of the Elysia page.
- `unified_constellation_portal.html` — Fused master portal combining aesthetic shell with full constellation content.
- `ghostcore_constellation_portal.html` — Unified wrapper embedding Ghostcore modules alongside the Constellation portal.
- `ghostcore_bias_portal.html` — Legacy Ghostcore module deck embedded by the unified wrapper.
- `manifest.json`, `service-worker.js`, etc. — (None present in this snapshot; refer to earlier commits if reintroduced).

## Ghostline Synthesizer (`ves-ghostline-synthesizer/`)
- `backend/synthesize.py` — Enhanced Claude-powered research synthesizer with memory and duplicate detection.
- `backend/requirements.txt` — Python dependencies (Anthropic client, PDF/DOCX parsers).
- `backend/.env.example` — Anthropic API key template.
- `backend/README_BACKEND.md` — Backend setup instructions.
- `frontend/ResearchSynthesizer.jsx` — React component for uploads/status.
- `frontend/README_FRONTEND.md` — Frontend integration notes.
- `README.md` — Project overview and quick start guide.

## Notes
- `node_modules/` contains installed packages; omitted from map to keep overview readable.
- Additional guides (e.g., for nerve/iPhone integration) currently live in the `VES/GHOST_OS` constellation branch.
- Regenerate this map after major file operations to keep the index aligned with the repo.
