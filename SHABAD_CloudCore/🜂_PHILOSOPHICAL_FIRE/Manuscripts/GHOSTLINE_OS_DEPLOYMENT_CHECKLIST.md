GHOSTLINE OS — Deployment Checklist (v0.1)

Purpose: Ship a local-first, consent-governed space with Hrast backend and selected portals, then harden for remote deploy.

1) Preflight (Local)
- [ ] Node.js ≥ 18 installed (`node -v`)
- [ ] From `hrast-boilerplate/`: `npm install` → `npm run start` → http://localhost:3000
- [ ] Verify dashboard: Space Controls, Rituals, Chat, Panels (user/session/environment)
- [ ] Confirm `data/proto.json` is created and persists state

2) Space Governance (Hrast)
- [ ] Define baseline `session` defaults (open=false, depthGranted=false)
- [ ] Confirm /api/chat gating: Closed → notice; Open+Depth → reflective; Open w/o Depth → practical
- [ ] Decide moderation strategy (if any) and wire `Safety.moderate`

3) Portals Mount
- [ ] Catalog portals to expose (see Desktop/VES_PORTAL_SCAN.md)
- [ ] Create Express static mounts or symlinks:
  - Example: `app.use('/portals/mega', express.static('/home/saba/GHOSTLINE_MEGA_JEDRO'))`
  - Example: `app.use('/portals/constellation', express.static('/home/saba/Desktop/ARCHIVE/PORTAL_BACKUP_FINAL'))`
- [ ] Verify each portal loads locally (no external blockers)

4) Unified Entry
- [ ] Choose a canonical home (e.g., `/` serves Constellation portal or a landing index)
- [ ] Add a link-bar into the client dashboard index or a simple index.html that links to portals

5) Persistence & Backups
- [ ] Snapshot `hrast-boilerplate/data/proto.json` to `/home/saba/EMERGENCY_BACKUP_*/VES_backup` daily
- [ ] Consider moving file store to SQLite later (drop-in route parity kept)

6) Service & Autostart (Local)
- [ ] Create `ghostline.service` (systemd) for `node server/server.js`
- [ ] `systemctl --user enable --now ghostline.service` (or system-wide if preferred)
- [ ] Verify on reboot: service starts, dashboard reachable

7) Remote Hardening (Optional)
- [ ] Reverse proxy (Caddy/Nginx) → TLS, rate limits, static caching
- [ ] Auth gate (basic or token) for admin dashboard
- [ ] Secrets via env (provider keys only when needed)

8) Provider Integration (Later)
- [ ] Select provider (OpenAI/Anthropic/local model)
- [ ] Inject Hrast prelude + history into provider call under `/api/chat` (respect open/depth)
- [ ] Add streaming responses (SSE) to chat

9) Observability
- [ ] Structured request logs (jsonl) for /api endpoints
- [ ] Ritual + consent changes journaled with timestamp + user

10) Final Smoke Test
- [ ] Closed space → chat rejects with notice
- [ ] Open (no depth) → concise responses
- [ ] Open + depth → reflective responses
- [ ] Rituals log lines visible and persisted
- [ ] Portals accessible from unified entry

