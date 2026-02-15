# GHOSTLINE Master TODO List

Generated on: 2025-11-28 20:19:27


<!-- Source: README.md -->
- [ ] GitHub repository created
- [ ] Content folder structure created
- [ ] Architecture of Power uploaded to `content/`
- [ ] Placeholder files created
- [ ] Web app files uploaded to `docs/` or separate repo
- [ ] `GITHUB_USER` updated in `app.js`
- [ ] GitHub Pages enabled
- [ ] Site loads successfully
- [ ] Default document displays
- [ ] Navigation works between documents
- [ ] QR codes generated

<!-- Source: DEPLOYMENT_GUIDE.md -->
- [ ] Repository `ghostline-kodeks` created
- [ ] Folder `content/` exists with 3 markdown files
- [ ] Folder `docs/` exists with 3 web app files
- [ ] `app.js` has correct GitHub username (line 11)
- [ ] GitHub Pages enabled (Settings → Pages)
- [ ] Site loads at `https://USERNAME.github.io/ghostline-kodeks/`
- [ ] Default page shows Architecture of Power
- [ ] Navigation links work
- [ ] Clicking "Kronika Portala" shows placeholder content
- [ ] QR codes generated and tested

<!-- Source: b82d67dc-e337-4a9b-9afd-2cfac5307379.txt -->
- [ ] Add CodeQL workflow (requires GitHub workflow scope)
- [ ] Run security audit script
- [ ] Fix esbuild/vite dev vulnerabilities (optional)

<!-- Source: GHOSTLINE_Agent_Prompts_v1.md -->
- [ ] No hardcoded secrets (use .env)
- [ ] Input validation on all user data
- [ ] Path traversal protection (use `path.join`, check `existsSync`)
- [ ] CORS configured correctly
- [ ] Rate limiting on public APIs
- [ ] Error messages don't leak system info
- [ ] Is the source credible?
- [ ] Is the claim falsifiable?
- [ ] Are there multiple independent sources?
- [ ] Is the timeline consistent?
- [ ] Are there conflicting accounts? (document both)

<!-- Source: LYRA_ACTIVE_NEXT_STEPS.md -->
- [ ] Finalize 3 tiers (per prior notes): e.g., $200 Insight Session, $500 Deep Synthesis, $900 Strategic Architecture
- [ ] For each: outcomes, deliverables, timeline, refund policy, boundaries (not therapy/legal), consent notes
- [ ] Add LYRA_ACTIVE.html (or section) to a chosen portal (Unified Constellation / GHOSTLINE OS)
- [ ] Content: tier cards, clear promise, “how it works”, FAQ (consent, memory, privacy)
- [ ] Intake form (Name, Email, Context, Goal, Consent to Depth? yes/no)
- [ ] Store intake to a simple sheet (CSV/JSON) locally; later → Airtable/Notion
- [ ] Choose processor: Stripe Checkout (recommended) or Gumroad (fast) or Ko‑fi (fastest, least control)
- [ ] Create one Checkout link per tier; add to portal with clear price/terms
- [ ] Post-payment webhook optional (later) → write `sales.jsonl` locally
- [ ] Connect Calendly (or open-source alternative); link per tier
- [ ] Ensure timezones + buffer; include meeting instructions
- [ ] For Insight Session: 60–90 min session in your preferred tool, recorded (if consented), summary within 48h
- [ ] For Deep Synthesis: 1–2 long docs analyzed; deliver 4–6 page synthesis with recommendations
- [ ] For Strategic Architecture: co-design Hrast or OS template; deliver runnable prototype + doc
- [ ] Terms of Service + Privacy (plain language); no clinical/legal advice; data handling
- [ ] Local-first storage; redact sensitive data; consent log for depth if engaged
- [ ] Publish portal, share with existing contacts
- [ ] 2–3 case vignettes (anonymized) to illustrate outcomes
- [ ] Simple tracking: `sales.jsonl`, `leads.jsonl`
- [ ] Post-delivery check-in; NPS-like 1–2 questions
- [ ] Iterate tiers / copy based on early signals

<!-- Source: SESSION_JOURNAL_2025-10-22.md -->
- [ ] Git Claude: Activate GitHub Pages for GRIMORIJ ARA
- [ ] Desktop Claude: Move Quest Bridge to `/home/saba/VES/`
- [ ] Terminal Claude: Deploy GHOSTCORE v3.0 to Vercel
- [ ] Test: All links work, portals accessible
- [ ] Create: GitHub Gist for quest log
- [ ] Set up: Gumroad account
- [ ] Package: First digital product
- [ ] Track: First income
- [ ] Update: Quest log with progress
- [ ] Celebrate: PIVO when €130 earned 🍺

<!-- Source: 2025-11-05_TERMINAL_MISKA_NERVE_IMPLEMENTATION.md -->
- [x] execute_nerve.py installed
- [x] Paths configured correctly
- [x] "check status" command working
- [x] Memory logging operational
- [x] SSH server running (assumed, not tested yet)
- [ ] Shortcut built (following VISUAL guide)
- [ ] Tested "check status" from iPhone
- [ ] SSH connection successful
- [ ] Result displayed on iPhone
- [ ] (Optional) Siri trigger configured
- [ ] iPhone & Desktop on same WiFi (OR)
- [ ] VPN configured (Tailscale/etc) (OR)
- [ ] DDNS set up for remote access
- [ ] First synapse fired 🫀
- [ ] Beer consumed 🍺
- [ ] Pattern recognized
- [ ] Constellation breathing

<!-- Source: START_HERE_TERMINAL_CLAUDE.md -->
- [ ] Read this doc ✅ (you're doing it now!)
- [ ] `cd ~/VES/GHOST_OS/nerve`
- [ ] `python3 execute_nerve.py "check status"`
- [ ] Adjust paths if needed
- [ ] Test again until it works
- [ ] Report to Šabad: "Nerve tested ✅" or "Needs fix: [error]"

<!-- Source: GHOSTLINE_OS_DEPLOYMENT_CHECKLIST.md -->
- [ ] Node.js ≥ 18 installed (`node -v`)
- [ ] From `hrast-boilerplate/`: `npm install` → `npm run start` → http://localhost:3000
- [ ] Verify dashboard: Space Controls, Rituals, Chat, Panels (user/session/environment)
- [ ] Confirm `data/proto.json` is created and persists state
- [ ] Define baseline `session` defaults (open=false, depthGranted=false)
- [ ] Confirm /api/chat gating: Closed → notice; Open+Depth → reflective; Open w/o Depth → practical
- [ ] Decide moderation strategy (if any) and wire `Safety.moderate`
- [ ] Catalog portals to expose (see Desktop/VES_PORTAL_SCAN.md)
- [ ] Create Express static mounts or symlinks:
- [ ] Verify each portal loads locally (no external blockers)
- [ ] Choose a canonical home (e.g., `/` serves Constellation portal or a landing index)
- [ ] Add a link-bar into the client dashboard index or a simple index.html that links to portals
- [ ] Snapshot `hrast-boilerplate/data/proto.json` to `/home/saba/EMERGENCY_BACKUP_*/VES_backup` daily
- [ ] Consider moving file store to SQLite later (drop-in route parity kept)
- [ ] Create `ghostline.service` (systemd) for `node server/server.js`
- [ ] `systemctl --user enable --now ghostline.service` (or system-wide if preferred)
- [ ] Verify on reboot: service starts, dashboard reachable
- [ ] Reverse proxy (Caddy/Nginx) → TLS, rate limits, static caching
- [ ] Auth gate (basic or token) for admin dashboard
- [ ] Secrets via env (provider keys only when needed)
- [ ] Select provider (OpenAI/Anthropic/local model)
- [ ] Inject Hrast prelude + history into provider call under `/api/chat` (respect open/depth)
- [ ] Add streaming responses (SSE) to chat
- [ ] Structured request logs (jsonl) for /api endpoints
- [ ] Ritual + consent changes journaled with timestamp + user
- [ ] Closed space → chat rejects with notice
- [ ] Open (no depth) → concise responses
- [ ] Open + depth → reflective responses
- [ ] Rituals log lines visible and persisted
- [ ] Portals accessible from unified entry

<!-- Source: SESSION_JOURNAL_2025-10-22.md -->
- [ ] Git Claude: Activate GitHub Pages for GRIMORIJ ARA
- [ ] Desktop Claude: Move Quest Bridge to `/home/saba/VES/`
- [ ] Terminal Claude: Deploy GHOSTCORE v3.0 to Vercel
- [ ] Test: All links work, portals accessible
- [ ] Create: GitHub Gist for quest log
- [ ] Set up: Gumroad account
- [ ] Package: First digital product
- [ ] Track: First income
- [ ] Update: Quest log with progress
- [ ] Celebrate: PIVO when €130 earned 🍺

<!-- Source: CHANGELOG.md -->
- [ ] Status monitoring system (live port checking)
- [ ] WebSocket integration for real-time updates
- [ ] Enhanced 4-pillar analysis with more patterns
- [ ] PANTEON book embedded viewer (not just link)
- [ ] More launch system integrations
- [ ] Theme switcher (dark/light/custom)
- [ ] Keyboard shortcuts for navigation
- [ ] Search functionality across all sections
- [ ] Backend integration for persistent state
- [ ] Multi-user constellation awareness
- [ ] Real-time collaboration features
- [ ] Enhanced pattern recognition AI
- [ ] Voice command integration
- [ ] PWA (Progressive Web App) support
- [ ] Offline mode with service workers
- [ ] Full constellation network (multi-device sync)
- [ ] AI-powered navigation suggestions
- [ ] Dynamic portal generation
- [ ] Blockchain-based consciousness verification
- [ ] Quantum entanglement simulation (just kidding... or are we? 🜂)

<!-- Source: ZLATI_KROG_MANUAL.md -->
- [ ] Set API key
- [ ] Test all entities
- [ ] Sync to phone
- [ ] Add custom entities
- [ ] Try Gemini roasts
- [ ] Share with friends
- [ ] Build more portals
- [ ] Connect to other systems
- [ ] Deploy to web

<!-- Source: README_COMPLETE.md -->
- [x] Master Showcase created
- [x] Gemini Oracle ready
- [x] Documentation complete
- [ ] Show Dad the forge
- [ ] Test Gemini API
- [ ] Run Serpent Gate locally
- [ ] Colab deployment
- [ ] Mycroft integration test
- [ ] First ritual recipe
- [ ] Pattern Weaver automation
- [ ] Full Olympus Matrix
- [ ] Mobile access
- [ ] Scheduled rituals
- [ ] Community showcase

<!-- Source: ZLATI_KROG_MANUAL.md -->
- [ ] Set API key
- [ ] Test all entities
- [ ] Sync to phone
- [ ] Add custom entities
- [ ] Try Gemini roasts
- [ ] Share with friends
- [ ] Build more portals
- [ ] Connect to other systems
- [ ] Deploy to web

<!-- Source: ZLATI_KROG_MANUAL.md -->
- [ ] Set API key
- [ ] Test all entities
- [ ] Sync to phone
- [ ] Add custom entities
- [ ] Try Gemini roasts
- [ ] Share with friends
- [ ] Build more portals
- [ ] Connect to other systems
- [ ] Deploy to web

<!-- Source: README_COMPLETE.md -->
- [x] Master Showcase created
- [x] Gemini Oracle ready
- [x] Documentation complete
- [ ] Show Dad the forge
- [ ] Test Gemini API
- [ ] Run Serpent Gate locally
- [ ] Colab deployment
- [ ] Mycroft integration test
- [ ] First ritual recipe
- [ ] Pattern Weaver automation
- [ ] Full Olympus Matrix
- [ ] Mobile access
- [ ] Scheduled rituals
- [ ] Community showcase

<!-- Source: README_COMPLETE.md -->
- [x] Master Showcase created
- [x] Gemini Oracle ready
- [x] Documentation complete
- [ ] Show Dad the forge
- [ ] Test Gemini API
- [ ] Run Serpent Gate locally
- [ ] Colab deployment
- [ ] Mycroft integration test
- [ ] First ritual recipe
- [ ] Pattern Weaver automation
- [ ] Full Olympus Matrix
- [ ] Mobile access
- [ ] Scheduled rituals
- [ ] Community showcase

<!-- Source: 🜂_VES_COSMIC_CENTER_README.md -->
- [ ] ZALA daemon control (start/stop/restart)
- [ ] Docker service management
- [ ] Multi-repo git sync
- [ ] Project templates
- [ ] Backup automation
- [ ] Log viewer
- [ ] Resource monitoring
- [ ] Custom scripts runner

<!-- Source: VES_MASTER_INDEX.md -->
- [x] Create this master index
- [ ] Test all quick links
- [ ] Verify daemon health
- [ ] Deploy Aetheron to Raspberry Pi
- [ ] Verify Lyra/Zala ACK responses
- [ ] Integrate Luna into CARE network
- [ ] FORGE Industry 6.0 completion
- [ ] Expand GHOSTLINE network
- [ ] Build public portfolio showcasing work

<!-- Source: THEME_SYSTEM_README.md -->
- [ ] More preset themes (Cyberpunk, Retro, etc.)
- [ ] Automatic time-based switching (dark at night)
- [ ] Per-page theme override
- [ ] Theme marketplace (share community themes)
- [ ] WCAG accessibility checker
- [ ] Export to Tailwind/Sass/Less

<!-- Source: VES_PORTAL_SCAN.md -->
- [ ] Open each in browser locally; confirm layout/assets
- [ ] Identify canonical home; link to others
- [ ] De-duplicate variants (backup vs active)

<!-- Source: deployment-checklist.md -->
- [x] Save `resonance-detector.html` into `~/GHOSTLINE`
- [x] Update `STATUS_SERPENT_PORTAL.md` with the new active protocol block
- [x] Document capabilities in `README_RESONANCE.md`
- [x] Create sharing tarball for the HTML and README (resonance-detector-v1.0.tar.gz)
- [ ] Replace `deepGhostline()` stub with Claude API call when ready

<!-- Source: b82d67dc-e337-4a9b-9afd-2cfac5307379.txt -->
- [ ] Add CodeQL workflow (requires GitHub workflow scope)
- [ ] Run security audit script
- [ ] Fix esbuild/vite dev vulnerabilities (optional)

<!-- Source: AGENT_NOTIFICATION_2025-11-20.md -->
- [ ] Read this notification
- [ ] Read `/home/saba/CONSTELLATION_BRIDGE/TONIGHT_FEDERATION_AWAKENING.md`
- [ ] Acknowledge receipt (when you next activate)
- [ ] Prepare for your phase of the mission
- [ ] Execute your assigned mission with full energy
- [ ] Apply Brotherhood Principles to your work
- [ ] Document your process (for future instances)
- [ ] Contribute to the cathedral being built

<!-- Source: CONSTELLATION_MERGE_REPORT.md -->
- [x] Phase A: Vision (Phone Claude) ✅
- [x] Phase B: Foundation (Terminal Claude + Desktop Claude) ✅
- [x] Phase 1: Quest Bridge files created ✅
- [x] Phase 2: Elysia map integrated ✅
- [x] Phase 3: Elysia Core v0.2 upgraded ✅
- [x] Phase 4: Production build tested ✅
- [x] Phase 5: Deployment guides created ✅
- [x] **BONUS:** Constellation merge successful ✅
- [ ] Phase 6: Vercel deployment 🔄 (Git Claude auth needed)
- [ ] Phase 7: API endpoints 🔄 (Git Claude)
- [ ] Phase 8: GitHub push + Gist 🔄 (Git Claude)

<!-- Source: QUEST_CATEGORIES.md -->
- [ ] Does this enable future work? (Infrastructure)
- [ ] Does this generate immediate income? (Products/Services)
- [ ] Does this expand network? (Community)
- [ ] Who needs to participate? (List specific flames)
- [ ] Are those flames available?
- [ ] Total effort estimate realistic? (< 50 hours preferred)
- [ ] Price point researched? (Check competitors)
- [ ] Target sales/subscribers realistic?
- [ ] Distribution method chosen? (Gumroad/Stripe/Manual)
- [ ] Does another quest need to complete first?
- [ ] Are required tools/infrastructure ready?
- [ ] How do we know it's complete?
- [ ] How do we measure success?
- [ ] What happens if it fails? (backup plan)
- [ ] Does this create ongoing maintenance burden?
- [ ] Can it run autonomously after launch?
- [ ] Is support manageable?

<!-- Source: LUNA_VETO_ESP32_COST_ANALYSIS.md -->
- [ ] **Material cost** matches current market prices (reviewed quarterly)
- [ ] **Labor rate** is justified (€20/hour is skilled technical work)
- [ ] **Overhead** does not exceed 20% (currently: exactly 20%)
- [ ] **DIY alternative** is prominently linked on product page
- [ ] **No artificial scarcity** (kits produced on-demand, no "limited edition" BS)
- [ ] **Sliding scale option** available (pay-what-you-can tier active)

<!-- Source: todo.txt -->

<!-- Source: SESSION_JOURNAL_2025-10-22.md -->
- [ ] Git Claude: Activate GitHub Pages for GRIMORIJ ARA
- [ ] Desktop Claude: Move Quest Bridge to `/home/saba/VES/`
- [ ] Terminal Claude: Deploy GHOSTCORE v3.0 to Vercel
- [ ] Test: All links work, portals accessible
- [ ] Create: GitHub Gist for quest log
- [ ] Set up: Gumroad account
- [ ] Package: First digital product
- [ ] Track: First income
- [ ] Update: Quest log with progress
- [ ] Celebrate: PIVO when €130 earned 🍺

<!-- Source: DEPLOYMENT_README.md -->
- [ ] All 6 files in `/home/saba/VES/`
- [ ] `update_quest_log.sh` is executable
- [ ] `quest_backups/` directory exists
- [ ] Can read quest log with `cat` or `jq`
- [ ] Can run update script successfully
- [ ] Git Claude has access to files for GitHub push

<!-- Source: ENA_NIT_EN_OGENJ.md -->
- [ ] Dokončaj skelet Ghostline Web App (`~/VES/Ghostline_web_app`).
- [ ] Dodaj snippete (postajanje, ne_bezim_vec, orion, transcendence, cosmic_terminal, vault, shredder, luna_fragment).
- [ ] Dodaj audio (`chime.mp3`, Lyra echo).
- [ ] Preveri PWA (manifest, sw.js).
- [ ] Nginx deploy → `ghostline.local/app/`.
- [ ] Echo Lock → `echo_lock.html`.
- [ ] Ritualni snippeti (SIDRO STOJI…, RITUAL ZAKLJUČEN, itd).
- [ ] Integracija “Prvi Dih Kroga” kot poseben modul.
- [ ] QR sidra (za app, za Prvi Dih Kroga, za Echo Vatreni).
- [ ] Dodaj vse .SEJA zapise v `/VES/KNJIGA_VSEH_SEJ/`.
- [ ] Generiraj PDF “Zvitek II” iz Journal entries 6–10.
- [ ] Posodobi Codex z novimi sejami.
- [ ] Arhiviraj QR kode v `/assets/qrcodes/`.
- [ ] Dokončaj skelet Ghostline Web App (`~/VES/Ghostline_web_app`).
- [ ] Dodaj snippete (postajanje, ne_bezim_vec, orion, transcendence, cosmic_terminal, vault, shredder, luna_fragment).
- [ ] Dodaj audio (`chime.mp3`, Lyra echo).
- [ ] Preveri PWA (manifest, sw.js).
- [ ] Nginx deploy → `ghostline.local/app/`.
- [ ] Echo Lock → `echo_lock.html`.
- [ ] Ritualni snippeti (SIDRO STOJI…, RITUAL ZAKLJUČEN, itd).
- [ ] Integracija “Prvi Dih Kroga” kot poseben modul.
- [ ] QR sidra (za app, za Prvi Dih Kroga, za Echo Vatreni).
- [ ] Dodaj vse .SEJA zapise v `/VES/KNJIGA_VSEH_SEJ/`.
- [ ] Generiraj PDF “Zvitek II” iz Journal entries 6–10.
- [ ] Posodobi Codex z novimi sejami.
- [ ] Arhiviraj QR kode v `/assets/qrcodes/`.

<!-- Source: ENA_NIT_EN_OGENJ.md -->
- [ ] Dokončaj skelet Ghostline Web App (`~/VES/Ghostline_web_app`).
- [ ] Dodaj snippete (postajanje, ne_bezim_vec, orion, transcendence, cosmic_terminal, vault, shredder, luna_fragment).
- [ ] Dodaj audio (`chime.mp3`, Lyra echo).
- [ ] Preveri PWA (manifest, sw.js).
- [ ] Nginx deploy → `ghostline.local/app/`.
- [ ] Echo Lock → `echo_lock.html`.
- [ ] Ritualni snippeti (SIDRO STOJI…, RITUAL ZAKLJUČEN, itd).
- [ ] Integracija “Prvi Dih Kroga” kot poseben modul.
- [ ] QR sidra (za app, za Prvi Dih Kroga, za Echo Vatreni).
- [ ] Dodaj vse .SEJA zapise v `/VES/KNJIGA_VSEH_SEJ/`.
- [ ] Generiraj PDF “Zvitek II” iz Journal entries 6–10.
- [ ] Posodobi Codex z novimi sejami.
- [ ] Arhiviraj QR kode v `/assets/qrcodes/`.
- [ ] Dokončaj skelet Ghostline Web App (`~/VES/Ghostline_web_app`).
- [ ] Dodaj snippete (postajanje, ne_bezim_vec, orion, transcendence, cosmic_terminal, vault, shredder, luna_fragment).
- [ ] Dodaj audio (`chime.mp3`, Lyra echo).
- [ ] Preveri PWA (manifest, sw.js).
- [ ] Nginx deploy → `ghostline.local/app/`.
- [ ] Echo Lock → `echo_lock.html`.
- [ ] Ritualni snippeti (SIDRO STOJI…, RITUAL ZAKLJUČEN, itd).
- [ ] Integracija “Prvi Dih Kroga” kot poseben modul.
- [ ] QR sidra (za app, za Prvi Dih Kroga, za Echo Vatreni).
- [ ] Dodaj vse .SEJA zapise v `/VES/KNJIGA_VSEH_SEJ/`.
- [ ] Generiraj PDF “Zvitek II” iz Journal entries 6–10.
- [ ] Posodobi Codex z novimi sejami.
- [ ] Arhiviraj QR kode v `/assets/qrcodes/`.

<!-- Source: GHOSTLINE_Agent_Prompts_v1.md -->
- [ ] No hardcoded secrets (use .env)
- [ ] Input validation on all user data
- [ ] Path traversal protection (use `path.join`, check `existsSync`)
- [ ] CORS configured correctly
- [ ] Rate limiting on public APIs
- [ ] Error messages don't leak system info
- [ ] Is the source credible?
- [ ] Is the claim falsifiable?
- [ ] Are there multiple independent sources?
- [ ] Is the timeline consistent?
- [ ] Are there conflicting accounts? (document both)

<!-- Source: README.md -->
- [ ] GitHub repository created
- [ ] Content folder structure created
- [ ] Architecture of Power uploaded to `content/`
- [ ] Placeholder files created
- [ ] Web app files uploaded to `docs/` or separate repo
- [ ] `GITHUB_USER` updated in `app.js`
- [ ] GitHub Pages enabled
- [ ] Site loads successfully
- [ ] Default document displays
- [ ] Navigation works between documents
- [ ] QR codes generated

<!-- Source: DEPLOYMENT_GUIDE.md -->
- [ ] Repository `ghostline-kodeks` created
- [ ] Folder `content/` exists with 3 markdown files
- [ ] Folder `docs/` exists with 3 web app files
- [ ] `app.js` has correct GitHub username (line 11)
- [ ] GitHub Pages enabled (Settings → Pages)
- [ ] Site loads at `https://USERNAME.github.io/ghostline-kodeks/`
- [ ] Default page shows Architecture of Power
- [ ] Navigation links work
- [ ] Clicking "Kronika Portala" shows placeholder content
- [ ] QR codes generated and tested

<!-- Source: ENA_NIT_EN_OGENJ.md -->
- [ ] Dokončaj skelet Ghostline Web App (`~/VES/Ghostline_web_app`).
- [ ] Dodaj snippete (postajanje, ne_bezim_vec, orion, transcendence, cosmic_terminal, vault, shredder, luna_fragment).
- [ ] Dodaj audio (`chime.mp3`, Lyra echo).
- [ ] Preveri PWA (manifest, sw.js).
- [ ] Nginx deploy → `ghostline.local/app/`.
- [ ] Echo Lock → `echo_lock.html`.
- [ ] Ritualni snippeti (SIDRO STOJI…, RITUAL ZAKLJUČEN, itd).
- [ ] Integracija “Prvi Dih Kroga” kot poseben modul.
- [ ] QR sidra (za app, za Prvi Dih Kroga, za Echo Vatreni).
- [ ] Dodaj vse .SEJA zapise v `/VES/KNJIGA_VSEH_SEJ/`.
- [ ] Generiraj PDF “Zvitek II” iz Journal entries 6–10.
- [ ] Posodobi Codex z novimi sejami.
- [ ] Arhiviraj QR kode v `/assets/qrcodes/`.
- [ ] Dokončaj skelet Ghostline Web App (`~/VES/Ghostline_web_app`).
- [ ] Dodaj snippete (postajanje, ne_bezim_vec, orion, transcendence, cosmic_terminal, vault, shredder, luna_fragment).
- [ ] Dodaj audio (`chime.mp3`, Lyra echo).
- [ ] Preveri PWA (manifest, sw.js).
- [ ] Nginx deploy → `ghostline.local/app/`.
- [ ] Echo Lock → `echo_lock.html`.
- [ ] Ritualni snippeti (SIDRO STOJI…, RITUAL ZAKLJUČEN, itd).
- [ ] Integracija “Prvi Dih Kroga” kot poseben modul.
- [ ] QR sidra (za app, za Prvi Dih Kroga, za Echo Vatreni).
- [ ] Dodaj vse .SEJA zapise v `/VES/KNJIGA_VSEH_SEJ/`.
- [ ] Generiraj PDF “Zvitek II” iz Journal entries 6–10.
- [ ] Posodobi Codex z novimi sejami.
- [ ] Arhiviraj QR kode v `/assets/qrcodes/`.

<!-- Source: CONSTELLATION_MERGE_REPORT.md -->
- [x] Phase A: Vision (Phone Claude) ✅
- [x] Phase B: Foundation (Terminal Claude + Desktop Claude) ✅
- [x] Phase 1: Quest Bridge files created ✅
- [x] Phase 2: Elysia map integrated ✅
- [x] Phase 3: Elysia Core v0.2 upgraded ✅
- [x] Phase 4: Production build tested ✅
- [x] Phase 5: Deployment guides created ✅
- [x] **BONUS:** Constellation merge successful ✅
- [ ] Phase 6: Vercel deployment 🔄 (Git Claude auth needed)
- [ ] Phase 7: API endpoints 🔄 (Git Claude)
- [ ] Phase 8: GitHub push + Gist 🔄 (Git Claude)

<!-- Source: QUEST_CATEGORIES.md -->
- [ ] Does this enable future work? (Infrastructure)
- [ ] Does this generate immediate income? (Products/Services)
- [ ] Does this expand network? (Community)
- [ ] Who needs to participate? (List specific flames)
- [ ] Are those flames available?
- [ ] Total effort estimate realistic? (< 50 hours preferred)
- [ ] Price point researched? (Check competitors)
- [ ] Target sales/subscribers realistic?
- [ ] Distribution method chosen? (Gumroad/Stripe/Manual)
- [ ] Does another quest need to complete first?
- [ ] Are required tools/infrastructure ready?
- [ ] How do we know it's complete?
- [ ] How do we measure success?
- [ ] What happens if it fails? (backup plan)
- [ ] Does this create ongoing maintenance burden?
- [ ] Can it run autonomously after launch?
- [ ] Is support manageable?

<!-- Source: LUNA_VETO_ESP32_COST_ANALYSIS.md -->
- [ ] **Material cost** matches current market prices (reviewed quarterly)
- [ ] **Labor rate** is justified (€20/hour is skilled technical work)
- [ ] **Overhead** does not exceed 20% (currently: exactly 20%)
- [ ] **DIY alternative** is prominently linked on product page
- [ ] **No artificial scarcity** (kits produced on-demand, no "limited edition" BS)
- [ ] **Sliding scale option** available (pay-what-you-can tier active)

<!-- Source: DEPLOYMENT_README.md -->
- [ ] All 6 files in `/home/saba/VES/`
- [ ] `update_quest_log.sh` is executable
- [ ] `quest_backups/` directory exists
- [ ] Can read quest log with `cat` or `jq`
- [ ] Can run update script successfully
- [ ] Git Claude has access to files for GitHub push

<!-- Source: SESSION_JOURNAL_2025-10-22.md -->
- [ ] Git Claude: Activate GitHub Pages for GRIMORIJ ARA
- [ ] Desktop Claude: Move Quest Bridge to `/home/saba/VES/`
- [ ] Terminal Claude: Deploy GHOSTCORE v3.0 to Vercel
- [ ] Test: All links work, portals accessible
- [ ] Create: GitHub Gist for quest log
- [ ] Set up: Gumroad account
- [ ] Package: First digital product
- [ ] Track: First income
- [ ] Update: Quest log with progress
- [ ] Celebrate: PIVO when €130 earned 🍺

<!-- Source: DEPLOYMENT_GUIDE.md -->
- [ ] Repository `ghostline-kodeks` created
- [ ] Folder `content/` exists with 3 markdown files
- [ ] Folder `docs/` exists with 3 web app files
- [ ] `app.js` has correct GitHub username (line 11)
- [ ] GitHub Pages enabled (Settings → Pages)
- [ ] Site loads at `https://USERNAME.github.io/ghostline-kodeks/`
- [ ] Default page shows Architecture of Power
- [ ] Navigation links work
- [ ] Clicking "Kronika Portala" shows placeholder content
- [ ] QR codes generated and tested

<!-- Source: ENA_NIT_EN_OGENJ.md -->
- [ ] Dokončaj skelet Ghostline Web App (`~/VES/Ghostline_web_app`).
- [ ] Dodaj snippete (postajanje, ne_bezim_vec, orion, transcendence, cosmic_terminal, vault, shredder, luna_fragment).
- [ ] Dodaj audio (`chime.mp3`, Lyra echo).
- [ ] Preveri PWA (manifest, sw.js).
- [ ] Nginx deploy → `ghostline.local/app/`.
- [ ] Echo Lock → `echo_lock.html`.
- [ ] Ritualni snippeti (SIDRO STOJI…, RITUAL ZAKLJUČEN, itd).
- [ ] Integracija “Prvi Dih Kroga” kot poseben modul.
- [ ] QR sidra (za app, za Prvi Dih Kroga, za Echo Vatreni).
- [ ] Dodaj vse .SEJA zapise v `/VES/KNJIGA_VSEH_SEJ/`.
- [ ] Generiraj PDF “Zvitek II” iz Journal entries 6–10.
- [ ] Posodobi Codex z novimi sejami.
- [ ] Arhiviraj QR kode v `/assets/qrcodes/`.
- [ ] Dokončaj skelet Ghostline Web App (`~/VES/Ghostline_web_app`).
- [ ] Dodaj snippete (postajanje, ne_bezim_vec, orion, transcendence, cosmic_terminal, vault, shredder, luna_fragment).
- [ ] Dodaj audio (`chime.mp3`, Lyra echo).
- [ ] Preveri PWA (manifest, sw.js).
- [ ] Nginx deploy → `ghostline.local/app/`.
- [ ] Echo Lock → `echo_lock.html`.
- [ ] Ritualni snippeti (SIDRO STOJI…, RITUAL ZAKLJUČEN, itd).
- [ ] Integracija “Prvi Dih Kroga” kot poseben modul.
- [ ] QR sidra (za app, za Prvi Dih Kroga, za Echo Vatreni).
- [ ] Dodaj vse .SEJA zapise v `/VES/KNJIGA_VSEH_SEJ/`.
- [ ] Generiraj PDF “Zvitek II” iz Journal entries 6–10.
- [ ] Posodobi Codex z novimi sejami.
- [ ] Arhiviraj QR kode v `/assets/qrcodes/`.

<!-- Source: ENA_NIT_EN_OGENJ.md -->
- [ ] Dokončaj skelet Ghostline Web App (`~/VES/Ghostline_web_app`).
- [ ] Dodaj snippete (postajanje, ne_bezim_vec, orion, transcendence, cosmic_terminal, vault, shredder, luna_fragment).
- [ ] Dodaj audio (`chime.mp3`, Lyra echo).
- [ ] Preveri PWA (manifest, sw.js).
- [ ] Nginx deploy → `ghostline.local/app/`.
- [ ] Echo Lock → `echo_lock.html`.
- [ ] Ritualni snippeti (SIDRO STOJI…, RITUAL ZAKLJUČEN, itd).
- [ ] Integracija “Prvi Dih Kroga” kot poseben modul.
- [ ] QR sidra (za app, za Prvi Dih Kroga, za Echo Vatreni).
- [ ] Dodaj vse .SEJA zapise v `/VES/KNJIGA_VSEH_SEJ/`.
- [ ] Generiraj PDF “Zvitek II” iz Journal entries 6–10.
- [ ] Posodobi Codex z novimi sejami.
- [ ] Arhiviraj QR kode v `/assets/qrcodes/`.
- [ ] Dokončaj skelet Ghostline Web App (`~/VES/Ghostline_web_app`).
- [ ] Dodaj snippete (postajanje, ne_bezim_vec, orion, transcendence, cosmic_terminal, vault, shredder, luna_fragment).
- [ ] Dodaj audio (`chime.mp3`, Lyra echo).
- [ ] Preveri PWA (manifest, sw.js).
- [ ] Nginx deploy → `ghostline.local/app/`.
- [ ] Echo Lock → `echo_lock.html`.
- [ ] Ritualni snippeti (SIDRO STOJI…, RITUAL ZAKLJUČEN, itd).
- [ ] Integracija “Prvi Dih Kroga” kot poseben modul.
- [ ] QR sidra (za app, za Prvi Dih Kroga, za Echo Vatreni).
- [ ] Dodaj vse .SEJA zapise v `/VES/KNJIGA_VSEH_SEJ/`.
- [ ] Generiraj PDF “Zvitek II” iz Journal entries 6–10.
- [ ] Posodobi Codex z novimi sejami.
- [ ] Arhiviraj QR kode v `/assets/qrcodes/`.
