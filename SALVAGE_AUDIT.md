# SALVAGE AUDIT — VES REPOSITORY
**Generated:** 2026-05-09  
**Scope:** Frontend components, pages, routes, HTML apps, public assets  
**Philosophy:** Salvage engineer looking for reusable intelligence, not an architect proposing rewrites

---

## PROJECTS FOUND

| Project | Type | Build | Location |
|---|---|---|---|
| GHOSTLINE_MOBILE | React SPA | Vite + Tailwind | `APPS/GHOSTLINE_MOBILE/` |
| CODEX (VESApp) | React SPA | Vite + Tailwind + Zustand | `CODEX/` |
| digital-godzilla | React SPA | Vite + framer-motion | `09_EXTERNAL_PROJECTS/digital-godzilla/` |
| GHOSTLINE_NEXUS | React SPA | unknown | `09_EXTERNAL_PROJECTS/GHOSTLINE_NEXUS/frontend/` |
| SVETISCE | React SPA | unknown | `SVETISCE/client/` |
| trinity-command-center | React + Firebase | CRA | `09_EXTERNAL_PROJECTS/trinity-command-center/` |
| VES Navigation Hub | Static HTML | CDN Tailwind | `index.html` |
| Ghostline Dashboard | Static HTML | CDN Tailwind | `DASHBOARD/` + `ghostline_dashboard/deck/` |
| Manifest Orion | Static HTML | CDN Tailwind | `APPS/MANIFEST_ORION/` |
| GHOSTCORE Visual | Static HTML | vanilla JS | `APPS/GHOSTCORE_VISUAL/` |

---

## COMPONENT REGISTER

---

### 1 · BottomNav
**Path:** `APPS/GHOSTLINE_MOBILE/src/components/BottomNav.jsx`  
**Purpose:** Fixed bottom tab bar — 8 tabs, icon + label, horizontal scroll for overflow  
**Visual:** Dark bg, active tab in primary color, inactive gray, safe-area padding  
**Interaction:** One tap → switch active view; horizontal scroll for overflow tabs  
**Mobile:** ✅ Yes — pb-safe, no-scrollbar, fixed bottom  
**Cognitive Load:** Low  
**Reuse Value:** High  
**Extraction Difficulty:** Easy  
**Risk Flags:** none  
**Best Reuse Target:** Ghostline, shared visual library  
**Verdict:** Best mobile nav component in the repo — clean, safe-area aware, zero dependencies beyond lucide-react.

---

### 2 · MaatVerdict
**Path:** `APPS/GHOSTLINE_MOBILE/src/components/MaatVerdict.jsx`  
**Purpose:** Minimal status footer — two icons (Heart vs Feather) + one status line  
**Visual:** Thin fixed bottom bar, border-top primary, mono font, icon pair  
**Interaction:** Passive display only  
**Mobile:** ✅ Yes — fixed full-width  
**Cognitive Load:** Low  
**Reuse Value:** High  
**Extraction Difficulty:** Easy  
**Risk Flags:** routing-bound (fixed bottom may conflict with other fixed elements)  
**Best Reuse Target:** Ghostline, shared visual library  
**Verdict:** Cleanest thing in the repo. Two icons + one statement + a boundary line. Perfect minimal status bar pattern.

---

### 3 · Isfet (Live Price Monitor)
**Path:** `APPS/GHOSTLINE_MOBILE/src/components/Isfet.jsx`  
**Purpose:** Two live-data cards with trend arrows, refresh button, critical alert  
**Visual:** Large mono price text, trend arrow (red/green), spinning refresh, conditional critical alert banner  
**Interaction:** Click refresh → simulated 1s delay → update → conditional alert if threshold crossed  
**Mobile:** ✅ Yes  
**Cognitive Load:** Low  
**Reuse Value:** High  
**Extraction Difficulty:** Easy  
**Risk Flags:** mock data (simulated prices)  
**Best Reuse Target:** ConsMAP, Ghostline, shared visual library  
**Verdict:** Best live-data card pattern — spinning refresh + large mono number + trend arrow + threshold alert is production-ready.

---

### 4 · Campfire (Text Purification)
**Path:** `APPS/GHOSTLINE_MOBILE/src/components/Campfire.jsx`  
**Purpose:** Input text → process (1.5s delay) → classified result (anchored/burned)  
**Visual:** Orange border-left accent, radial flame background (opacity-10), animated flame on processing  
**Interaction:** Textarea → button → processing state (animate-pulse flame) → result card with frequency + status  
**Mobile:** ✅ Yes  
**Cognitive Load:** Medium  
**Reuse Value:** High  
**Extraction Difficulty:** Medium (regex logic is content-specific, but the shell is universal)  
**Risk Flags:** unclear purpose to outsiders  
**Best Reuse Target:** ConsMAP, Ghostline  
**Verdict:** Best input-process-result pattern in the repo. The "ritual" framing adds warmth to a generic async-classification UX.

---

### 5 · AgentCard / SystemCard (CODEX)
**Paths:** `CODEX/src/ves/components/AgentCard.jsx` · `CODEX/src/ves/components/SystemCard.jsx`  
**Purpose:** Entity cards — gradient background per entity, 5xl emoji icon, status indicators, hover scale  
**Visual:** Full-height gradient per card, large emoji, role text, CheckCircle/XCircle status, ChevronRight on hover  
**Interaction:** hover:scale-105 + shadow glow  
**Mobile:** ✅ Yes  
**Cognitive Load:** Low  
**Reuse Value:** High  
**Extraction Difficulty:** Easy (remove hardcoded lookup maps; pass data as props)  
**Risk Flags:** hardcoded AGENT_INFO / SYSTEM_INFO lookup tables defeat reusability  
**Best Reuse Target:** ConsMAP, Ghostline, shared visual library  
**Verdict:** Beautiful entity card pattern. Emoji icon + gradient + role text + hover glow is universally reusable. Consolidate the two near-identical components into one.

---

### 6 · Harvest (Progress-to-Reveal)
**Path:** `APPS/GHOSTLINE_MOBILE/src/components/Harvest.jsx`  
**Purpose:** Select target → trigger process → watch interval progress bar → data table reveals  
**Visual:** Emerald scheme, pill selector row (overflow scroll), animated progress bar, data grid reveal  
**Interaction:** Pill select → button → setInterval fills progress bar → data populates on complete  
**Mobile:** ✅ Yes — pill row uses overflow-x + no-scrollbar  
**Cognitive Load:** Medium  
**Reuse Value:** High  
**Extraction Difficulty:** Medium  
**Risk Flags:** mock data, unclear purpose name  
**Best Reuse Target:** ConsMAP, Ghostline  
**Verdict:** Best progressive-reveal interaction in the repo. The pill selector + interval progress + table reveal is a golden UX pattern for any async data-fetch flow.

---

### 7 · Cosmos (Node Constellation Map)
**Path:** `APPS/GHOSTLINE_MOBILE/src/components/Cosmos.jsx`  
**Purpose:** Visual network — 5 nodes positioned over black canvas, SVG connection lines, click reveals tooltip  
**Visual:** Black radial background with subtle grid, colored node buttons, SVG lines (opacity-30), info tooltip with backdrop-blur  
**Interaction:** Click node → tooltip appears (slide-in-from-bottom) with name/type/status/description  
**Mobile:** ⚠️ Medium — 450px fixed height, absolute positions  
**Cognitive Load:** Medium  
**Reuse Value:** High  
**Extraction Difficulty:** Medium (positions hardcoded as percentages)  
**Risk Flags:** tightly coupled (hardcoded node positions)  
**Best Reuse Target:** ConsMAP, Ghostline, shared visual library  
**Verdict:** Best spatial navigation model in the repo. SVG lines + positioned nodes + click tooltip is a reusable spatial info pattern.

---

### 8 · VES Dashboard (CODEX)
**Path:** `CODEX/src/ves/pages/Dashboard.jsx`  
**Purpose:** Main hub — 3 stat cards + 6-system grid + 4 quick-action buttons  
**Visual:** Dark gradient (gray-900 → purple-900), backdrop-blur header, animated refresh icon  
**Interaction:** 30s polling interval, loading state, view switching via setCurrentView  
**Mobile:** ⚠️ Medium — grid at md breakpoint  
**Cognitive Load:** Medium  
**Reuse Value:** High  
**Extraction Difficulty:** Medium (Zustand dependency)  
**Risk Flags:** dependency-heavy (Zustand, polling)  
**Best Reuse Target:** ConsMAP, Ghostline  
**Verdict:** Best dashboard layout in the repo. The 3-stat row + card grid + quick-action buttons structure is reusable across any system overview page.

---

### 9 · AgentConsole (CODEX)
**Path:** `CODEX/src/ves/pages/AgentConsole.jsx`  
**Purpose:** Two-state UI: agent selector grid → chat interface with role-colored messages  
**Visual:** Grid of agent cards → chat window with cyan (user) / white/10 (assistant) / yellow/20 (system) bubbles  
**Interaction:** Click agent → enter chat → type + send → 1s simulated reply → messages append  
**Mobile:** ⚠️ Medium — agent grid at md: 2col, lg: 3col  
**Cognitive Load:** Medium  
**Reuse Value:** High  
**Extraction Difficulty:** Medium (Zustand, CONSTELLATION_BRIDGE placeholder)  
**Risk Flags:** tightly coupled, graph placeholder not wired  
**Best Reuse Target:** Ghostline, ConsMAP  
**Verdict:** Best chat UI in the repo. Role-colored message bubbles + two-state (select→chat) is a clean production pattern.

---

### 10 · Codex Accordion (digital-godzilla)
**Path:** `09_EXTERNAL_PROJECTS/digital-godzilla/src/pages/Codex.jsx`  
**Purpose:** Expandable knowledge entries with toggle, special glow on select entries  
**Visual:** Green/amber border-left coding, hz-432-glow animation on special entry, scroll-delay stagger  
**Interaction:** Click header → toggle expand/collapse section  
**Mobile:** ✅ Yes  
**Cognitive Load:** Low  
**Reuse Value:** High  
**Extraction Difficulty:** Easy  
**Risk Flags:** lore-specific content  
**Best Reuse Target:** ConsMAP, Ghostline, shared visual library  
**Verdict:** Best accordion/docs pattern in the repo — clean toggle, color-coded special entries, no library required.

---

### 11 · NavBar + Glitch CSS (digital-godzilla)
**Path:** `09_EXTERNAL_PROJECTS/digital-godzilla/src/components/NavBar.jsx`  
**Purpose:** Top nav with VHS glitch logo effect + scan-lines  
**Visual:** Dark gray + green border, monospace font, scan-lines overlay, data-text glitch CSS  
**Interaction:** React Router links, hover color transitions  
**Mobile:** ⚠️ Medium  
**Cognitive Load:** Low  
**Reuse Value:** High  
**Extraction Difficulty:** Easy (CSS is the valuable piece)  
**Risk Flags:** routing-bound (react-router-dom Link)  
**Best Reuse Target:** Ghostline, shared visual library  
**Verdict:** Most visually distinctive nav pattern in the repo. The glitch + scan-lines CSS is a direct steal.

---

### 12 · Characters Grid (digital-godzilla)
**Path:** `09_EXTERNAL_PROJECTS/digital-godzilla/src/pages/Characters.jsx`  
**Purpose:** Responsive 3-column entity grid with corner-accent cards and stagger entrance  
**Visual:** Absolute-positioned corner border accents (4px lines), staggered framer-motion, episode badge, group hover  
**Interaction:** hover:scale + color shift per card  
**Mobile:** ✅ Yes — md:2, lg:3 responsive  
**Cognitive Load:** Low  
**Reuse Value:** High  
**Extraction Difficulty:** Easy (framer-motion dependency)  
**Risk Flags:** dependency-heavy (framer-motion), hardcoded data  
**Best Reuse Target:** ConsMAP, Ghostline, shared visual library  
**Verdict:** Best grid card layout in the repo. Corner-accent + stagger entrance is a strong pattern for any entity list.

---

### 13 · CharacterHoverCard (digital-godzilla)
**Path:** `09_EXTERNAL_PROJECTS/digital-godzilla/src/components/CharacterHoverCard.jsx`  
**Purpose:** Motion-animated popup card for entity info on hover  
**Visual:** Scale/opacity entrance via framer-motion, gradient bg, border effects  
**Interaction:** isVisible state → spring animation in/out  
**Mobile:** ❌ Low (absolute positioned, hover-only)  
**Cognitive Load:** Low  
**Reuse Value:** High  
**Extraction Difficulty:** Medium (framer-motion)  
**Risk Flags:** low mobile (tooltip is click-based on mobile)  
**Best Reuse Target:** Ghostline, shared visual library  
**Verdict:** Elegant hover card. Pattern translates to click-triggered on mobile with minor rework.

---

### 14 · Episode Scene Reader (digital-godzilla)
**Path:** `09_EXTERNAL_PROJECTS/digital-godzilla/src/pages/Episode.jsx`  
**Purpose:** Scene-by-scene narrative reader — prev/next, kino mode, progress persistence  
**Visual:** Gradient progress bar (neon-green → retro-cyan), kino mode toggle, corner accents  
**Interaction:** Next/prev scene button, kino toggle, localStorage progress save  
**Mobile:** ✅ Yes  
**Cognitive Load:** Medium  
**Reuse Value:** High  
**Extraction Difficulty:** Medium (useParams, localStorage, hardcoded episode data)  
**Risk Flags:** tightly coupled to episode data structure  
**Best Reuse Target:** ConsMAP, Ghostline  
**Verdict:** Most interesting content navigation pattern in the repo. Scene reader with kino mode is a genuine progressive-disclosure mechanic worth stealing.

---

### 15 · ConstellationPulse (SVETISCE)
**Path:** `SVETISCE/client/src/components/ConstellationPulse.jsx`  
**Purpose:** Full-screen animated starfield with orbiting nodes and hover reveal  
**Visual:** Static stars + pulsing colored nodes in circular orbit, hover shows label/description  
**Interaction:** setInterval phase loop (pulse animation), hover → show label  
**Mobile:** ⚠️ Medium (full-screen positioning)  
**Cognitive Load:** Low  
**Reuse Value:** High  
**Extraction Difficulty:** Medium (setInterval, useMemo for stars, dynamic hue → box-shadow)  
**Risk Flags:** none  
**Best Reuse Target:** ConsMAP, Ghostline, shared visual library  
**Verdict:** Most atmospheric component in the repo. Slow pulse loop on a star field is a perfect idle/ambient background system.

---

### 16 · Chat (GHOSTLINE_NEXUS)
**Path:** `09_EXTERNAL_PROJECTS/GHOSTLINE_NEXUS/frontend/src/components/Chat.jsx`  
**Purpose:** Persistent chat with session management, auto-scroll, localStorage persistence  
**Visual:** Role-styled messages, typing indicator (3-dot pulse)  
**Interaction:** Send → API → append message → auto-scroll via useRef; localStorage session  
**Mobile:** ⚠️ Unknown (external stylesheet)  
**Cognitive Load:** Low  
**Reuse Value:** High  
**Extraction Difficulty:** Medium (api service dependency)  
**Risk Flags:** tightly coupled to api service  
**Best Reuse Target:** Ghostline  
**Verdict:** Best backend-wired chat component. The useRef auto-scroll + localStorage session persistence is production-ready.

---

### 17 · System Health Monitor (GHOSTLINE_NEXUS)
**Path:** `09_EXTERNAL_PROJECTS/GHOSTLINE_NEXUS/frontend/src/components/System.jsx`  
**Purpose:** Categorized service health grid with AbortSignal-timeout polling  
**Visual:** Status badges (online/offline/checking), service links, category headers  
**Interaction:** 30s useEffect interval → AbortSignal(2s) per request → badge updates  
**Mobile:** ⚠️ Unknown  
**Cognitive Load:** Medium  
**Reuse Value:** High  
**Extraction Difficulty:** Medium  
**Risk Flags:** hardcoded service URLs  
**Best Reuse Target:** Ghostline, ConsMAP  
**Verdict:** Best service monitoring pattern — AbortSignal timeout + no-cors probe + badge update is production-grade.

---

### 18 · Stat-Card + Log-Entry CSS (DASHBOARD HTML)
**Paths:** `DASHBOARD/index.html` · `ghostline_dashboard/deck/index.html`  
**Purpose:** Static dashboard with neon-box glassmorphism + stat cards + log entries  
**Visual:** neon-box (border rgba cyan 0.3 + box-shadow + backdrop-blur), stat-card (border-left accent + translateX hover), log-entry (border-left green + font-size 12)  
**Interaction:** Hover stat-card → translateX(5px); refresh button  
**Mobile:** ✅ Yes (max-w-7xl, Tailwind)  
**Cognitive Load:** Low  
**Reuse Value:** High  
**Extraction Difficulty:** Easy (CSS classes, no framework)  
**Risk Flags:** duplicate (identical file in DASHBOARD/ and ghostline_dashboard/deck/)  
**Best Reuse Target:** Ghostline, shared visual library  
**Verdict:** The `.stat-card` + `.log-entry` CSS micro-patterns are the cleanest direct-copy fodder in the repo.

---

### 19 · Manifest Orion Landing
**Path:** `APPS/MANIFEST_ORION/index.html`  
**Purpose:** Static portal landing page — two navigation cards (Grimoire + Platform)  
**Visual:** Deep emerald radial gradient, JetBrains Mono + Inter, glassmorphism cards, .btn-portal link buttons  
**Interaction:** Card hover (translateY(-5px) + border-glow), .btn-portal hover  
**Mobile:** ✅ Yes  
**Cognitive Load:** Low  
**Reuse Value:** High  
**Extraction Difficulty:** Easy  
**Risk Flags:** none  
**Best Reuse Target:** ConsMAP, shared visual library  
**Verdict:** Cleanest static landing page in the repo. The card:hover + .btn-portal + emerald radial bg is directly portable.

---

### 20 · GHOSTCORE Visual Archive
**Path:** `APPS/GHOSTCORE_VISUAL/index.html`  
**Purpose:** Minimal markdown book reader — nav, marked.js render, status bar, keyboard shortcuts  
**Visual:** Border-left accent, live-dot pulsing indicator, status bar (live + system-status + version)  
**Interaction:** Book click → load + render markdown; Ctrl+1/2/3 keyboard shortcuts; status bar updates  
**Mobile:** ⚠️ Medium  
**Cognitive Load:** Low  
**Reuse Value:** High  
**Extraction Difficulty:** Easy  
**Risk Flags:** app.min.js is a black box (not auditable), marked.js CDN dependency  
**Best Reuse Target:** ConsMAP, Ghostline  
**Verdict:** The status-bar layout (live-dot + text + version) and keyboard-shortcut navigation are clean patterns worth lifting.

---

### 21 · Rattmann Toggle List
**Path:** `APPS/GHOSTLINE_MOBILE/src/components/Rattmann.jsx`  
**Purpose:** Toggleable item list with protected/vulnerable states and glow feedback  
**Visual:** Amber accent, glow box-shadow on protected items, lock/unlock icons  
**Interaction:** Click toggle → flip state → recalculate survival rate  
**Mobile:** ✅ Yes  
**Cognitive Load:** Low  
**Reuse Value:** High  
**Extraction Difficulty:** Easy  
**Risk Flags:** unclear purpose name  
**Best Reuse Target:** Ghostline, shared visual library  
**Verdict:** Clean toggleable item card. The glow-shadow on the "active" state is a warm, clear feedback pattern.

---

### 22 · BloodTax Metric Cards
**Path:** `APPS/GHOSTLINE_MOBILE/src/components/BloodTax.jsx`  
**Purpose:** Calculator inputs → 4 metric cards with icon + label + value  
**Visual:** 2-column grid, highlight border on active metric, icon + label + bold value  
**Interaction:** Two inputs → live-update via useEffect  
**Mobile:** ✅ Yes  
**Cognitive Load:** Low  
**Reuse Value:** High  
**Extraction Difficulty:** Easy (isolate the Metric sub-component)  
**Risk Flags:** tightly coupled to calculateBloodTax utility  
**Best Reuse Target:** ConsMAP, shared visual library  
**Verdict:** The `<Metric icon label value highlight>` sub-component is the most extraction-ready atomic component in the repo.

---

### 23 · NewsTicker
**Path:** `APPS/GHOSTLINE_MOBILE/src/components/NewsTicker.jsx`  
**Purpose:** Scrolling horizontal text ticker — CSS-only animation  
**Visual:** Accent-colored strip, whitespace-nowrap, 20s linear ticker loop  
**Interaction:** Passive/decorative  
**Mobile:** ✅ Yes  
**Cognitive Load:** Low  
**Reuse Value:** Medium  
**Extraction Difficulty:** Easy  
**Risk Flags:** hardcoded satirical content  
**Best Reuse Target:** Ghostline, inspiration only  
**Verdict:** Elegant zero-dep ticker. Steal the `@keyframes ticker` CSS block.

---

### 24 · ARKHON_TRINITY
**Path:** `CODEX/src/ARKHON_TRINITY.jsx`  
**Purpose:** Audio synthesis (Web Audio API) + canvas mandala visualization + ritual invocation log  
**Visual:** Three gradient arkhon cards, canvas mandala (300x300) with glow, scrollable ritual log  
**Interaction:** Click arkhon → invoke → oscillator plays + mandala draws + log appends  
**Mobile:** ⚠️ Medium  
**Cognitive Load:** High  
**Reuse Value:** Medium (Web Audio + canvas patterns are interesting)  
**Extraction Difficulty:** Hard  
**Risk Flags:** unclear purpose, dependency-heavy, high cognitive load  
**Best Reuse Target:** inspiration only  
**Verdict:** Most technically ambitious component in the repo. The canvas mandala + Web Audio oscillator pattern is unique and worth studying; too complex to extract wholesale.

---

### 25 · TrinityTemple
**Path:** `SVETISCE/client/src/components/TrinityTemple.jsx`  
**Purpose:** 9-section shrine — memorial, story, philosophy, archont layers, sigil gallery, ritual invocations  
**Visual:** Amber gradients, expandable layers, SVG constellation, embeds ConstellationPulse  
**Interaction:** Section navigation, expandable archont layer accordion  
**Mobile:** ⚠️ Medium  
**Cognitive Load:** High  
**Reuse Value:** Low (monolithic)  
**Extraction Difficulty:** Hard (800+ lines, switch-based)  
**Risk Flags:** tightly coupled, visual clutter, high cognitive load  
**Best Reuse Target:** archive only  
**Verdict:** A cathedral in a single file. The individual sub-patterns (sigil cards, accordion layers) are good if extracted separately. The monolith itself is unsalvageable.

---

### 26 · ToneSimulator
**Path:** `APPS/GHOSTLINE_MOBILE/src/components/ToneSimulator.jsx`  
**Purpose:** Auto-updating doughnut chart + metrics + event log feed  
**Visual:** Chart.js Doughnut (centered with overlay text), 2-col grid, scrollable event log  
**Interaction:** 2s interval auto-update, two action buttons, alert on > 50% risk  
**Mobile:** ⚠️ Medium  
**Cognitive Load:** High  
**Reuse Value:** Medium (event log sub-pattern is good)  
**Extraction Difficulty:** Hard  
**Risk Flags:** dependency-heavy (chart.js), high cognitive load, missing Activity import  
**Best Reuse Target:** archive only  
**Verdict:** Too dense. The auto-updating event feed (timestamp + color-coded status rows) is worth isolating, but the full component is cognitively overloaded.

---

### 27 · JustificationMetrics
**Path:** `APPS/GHOSTLINE_MOBILE/src/components/JustificationMetrics.jsx`  
**Purpose:** Analytics dashboard with 4 stat cards + log table  
**Visual:** Green accent, dual-color progress bar, emoji indicators, hover log rows  
**Interaction:** Passive (mock data display)  
**Mobile:** ⚠️ Medium  
**Cognitive Load:** High  
**Reuse Value:** Low  
**Extraction Difficulty:** Hard  
**Risk Flags:** unclear purpose, mock data, visual clutter  
**Best Reuse Target:** archive only  
**Verdict:** Good log-table hover pattern buried under opaque abstraction. Too coupled to mock data to extract cleanly.

---

### 28 · GhostcorePortal.jsx
**Path:** `CODEX/src/GhostcorePortal.jsx`  
**Purpose:** Legacy duplicate of App.jsx with syntax error and unused imports  
**Visual:** Same as App.jsx  
**Interaction:** Same as App.jsx  
**Mobile:** Unknown  
**Cognitive Load:** High  
**Reuse Value:** Low  
**Extraction Difficulty:** N/A  
**Risk Flags:** stale, duplicate, syntax error (unclosed div), not loaded  
**Best Reuse Target:** archive only  
**Verdict:** Delete this file. It is a broken copy of superseded code.

---

### 29 · Trivia (GHOSTLINE_NEXUS)
**Path:** `09_EXTERNAL_PROJECTS/GHOSTLINE_NEXUS/frontend/src/components/Trivia.jsx`  
**Purpose:** Tier-based knowledge game with AI evaluator (T0–T9)  
**Visual:** Color-coded tier cards, glitch text, answer textarea, LYRA response  
**Interaction:** Select tier → generate question via API → submit answer → AI evaluates → score  
**Mobile:** ⚠️ Unknown  
**Cognitive Load:** High  
**Reuse Value:** Low  
**Extraction Difficulty:** Hard  
**Risk Flags:** tightly coupled (api service), high complexity, unclear purpose  
**Best Reuse Target:** archive only  
**Verdict:** Interesting AI-evaluation loop but too entangled to reuse. The tier color-coding (T0–T9 with gradients) is the only extractable visual pattern.

---

### 30 · TrinityCommandCenter App
**Path:** `09_EXTERNAL_PROJECTS/trinity-command-center/src/App.js`  
**Purpose:** Firebase-backed multi-tab dashboard with SVG network graph  
**Visual:** Sidebar + tabs, SVG nodes with click popup, log viewer  
**Interaction:** Firebase auth, Firestore data, tab switching, SVG node click  
**Mobile:** ❌ Low (desktop layout)  
**Cognitive Load:** High  
**Reuse Value:** Medium (SVG graph pattern)  
**Extraction Difficulty:** Hard  
**Risk Flags:** dependency-heavy (Firebase), stale (CRA), routing-bound  
**Best Reuse Target:** archive only  
**Verdict:** The SVG network graph with clickable nodes is the only extractable pattern, and it's buried under Firebase coupling.

---

## TOP 10 LISTS

---

### TOP 10 BEST REUSABLE COMPONENTS

1. **BottomNav** — mobile tab bar, zero friction lift
2. **MaatVerdict** — minimal status bar, two icons + one line
3. **Isfet** — live-data card with refresh + threshold alert
4. **AgentCard / SystemCard** (merged) — entity card with gradient + emoji + status
5. **Campfire** — input → process → result shell (content is swappable)
6. **Harvest** — pill selector + interval progress + data reveal
7. **Codex accordion** (digital-godzilla) — clean toggle, no library
8. **ConstellationPulse** — ambient star + node pulse background
9. **Chat** (GHOSTLINE_NEXUS) — backend-wired chat with role bubbles
10. **Metric sub-component** (BloodTax) — icon + label + value card atom

---

### TOP 10 BEST VISUAL PATTERNS

1. **NavBar glitch + scan-lines** (digital-godzilla) — VHS aesthetic CSS
2. **stat-card + log-entry** (DASHBOARD HTML) — border-left + hover translateX
3. **Manifest Orion card hover glow** — translateY + border-color + box-shadow
4. **Campfire radial flame bg** — orange accent + opacity-10 radial behind input
5. **AgentCard gradient per entity** — per-entity color coding via gradient
6. **ConstellationPulse pulsing nodes** — hue-mapped box-shadow on pulse loop
7. **Isfet large mono price + trend arrow** — data readability at a glance
8. **Rattmann glow-shadow on toggle** — shadow-[0_0_15px_rgba(16,185,129,0.1)] warmth
9. **Characters corner-accent cards** — absolute 4px border fragments as corners
10. **ARKHON_TRINITY canvas mandala** — canvas + shadowBlur = beautiful; study this

---

### TOP 10 BEST NAVIGATION IDEAS

1. **BottomNav** — mobile tab bar with horizontal overflow scroll
2. **Episode scene reader** — one scene at a time, prev/next, kino mode
3. **Harvest pill selector** — horizontal scroll pills = quick filter
4. **Cosmos node-click** — spatial map with click-to-reveal info
5. **AgentConsole two-state** — select entity → enter interaction
6. **GHOSTCORE keyboard shortcuts** — Ctrl+1/2/3 for section jump
7. **BiasSection two-path** — both choices lead to same reveal (clever)
8. **VES Hub tab switching** — pure JS tab with active-tab border-bottom
9. **Codex accordion** — expand/collapse without routing
10. **Manifest Orion two-card** — clear 2-option portal landing

---

### TOP 10 BEST DOCS UX PATTERNS

1. **GHOSTCORE keyboard shortcuts** — Ctrl+1/2/3 navigation + status bar
2. **Codex accordion** — expandable entries, color-coded special items
3. **Episode scene reader** — progressive chapter navigation + kino mode
4. **FileBrowserSection** — category hierarchy (MANUSCRIPTS/PORTALS/MEDIA)
5. **Manuscript.jsx + marked** — clean markdown-to-HTML render
6. **Manifest Orion two-card portal** — clear entry-point selection
7. **SheepWolfSection three-column** — historical / modern / detection analysis
8. **Settings collapsible guides** — HTML `<details>` for setup guides
9. **Status bar live-dot** — persistent system status without a modal
10. **TrinityTemple sigil gallery** — visual index of concepts with hover descriptions

---

### TOP 10 BEST LOW-ENTROPY INTERACTIONS

1. **MaatVerdict** — passive status, zero cognitive demand
2. **BottomNav** — one tap = one view
3. **Isfet refresh** — one button, one outcome, clear threshold feedback
4. **Rattmann toggle** — one click = lock/unlock, glow confirms
5. **Campfire** — one textarea + one button = classified result
6. **Challenge** — binary choice per screen (deny/override), no ambiguity
7. **Codex accordion** — one click = expand/collapse
8. **Episode prev/next** — one decision at a time, linear progression
9. **Manifest Orion two-card** — two options, zero ambiguity
10. **GHOSTCORE live-dot status** — pure passive indicator, no interaction required

---

### TOP 10 THINGS TO AVOID

1. **TrinityTemple as a single component** — 800+ line switch-render monolith; cathedral != reusable
2. **ToneSimulator density** — chart + metrics + live feed + 2 buttons simultaneously; cognitive flood
3. **JustificationMetrics** — mock data masquerading as analytics; opaque, useless to outsiders
4. **TrinityCommandCenter Firebase coupling** — Firebase auth baked into rendering logic; near impossible to detach
5. **VES Navigation Hub "all 12 systems" tab dump** — every system on one screen; dashboard worship
6. **GhostcorePortal.jsx** — broken duplicate; dead code with syntax error
7. **Hardcoded AGENT_INFO / SYSTEM_INFO lookup tables** — defeats the reusability of the cards they serve
8. **OracleViewer graph placeholder** — ships a "LIVE VISUALIZATION" div that is literally an empty div; fake depth
9. **Trivia.jsx all-in-one** — game state + AI eval + tier grid + localStorage all in one 200-line component; no seams
10. **ARKHON_TRINITY in production UX** — beautiful experiment; wrong tool for clear communication

---

## EXECUTIVE VERDICT

---

### What Actually Feels Alive

**GHOSTLINE_MOBILE** is the most cohesive thing in the repo. It has a consistent visual language, a clear mobile-first intent, and several components that work as standalone atoms (BottomNav, MaatVerdict, Isfet, Campfire, Rattmann). The design voice is dark but warm — amber, emerald, and orange accents against slate, which avoids the cold sterility of pure cyan-on-black.

**CODEX/VESApp** (Dashboard + AgentConsole + AgentCard) is the most structurally sound React architecture. The entity card pattern (gradient + emoji + status) is genuinely lovely and could anchor a shared component library.

**Manifest Orion** is the cleanest single page. It makes two decisions visible without overloading the screen — the `.card:hover` interaction and the `.btn-portal` buttons are immediately portable.

**digital-godzilla**'s CSS is the most distinctive — the scan-lines + glitch logo + corner-accent cards are the most visually memorable patterns in the repo.

---

### What Is Fake Complexity

- **TrinityTemple** — a single 800-line component that does 9 completely different things. Not a component; a codebase that refused to split.
- **OracleViewer** — ships a "live graph visualization" placeholder that is an empty div. Visual theater.
- **JustificationMetrics** — hardcoded mock data presented as a real analytics dashboard.
- **ToneSimulator** — three dashboards bolted together calling themselves one feature.
- **VES Navigation Hub terminal** — fake terminal input (`<input placeholder="Enter navigation command...">`) that runs no commands.

---

### What Should Never Be Reused

- **GhostcorePortal.jsx** — broken duplicate, delete it
- **JustificationMetrics** — unclear purpose + mock data + high load = no salvage value
- **Trivia.jsx** — too entangled (AI eval + game state + localStorage) to extract cleanly
- **TrinityCommandCenter** — Firebase too deeply embedded in render logic
- The **AGENT_INFO / SYSTEM_INFO lookup tables** as-is — replace with prop-driven data before lifting the cards

---

### Safest Next Adoption Steps

**Step 1 — Lift the atoms:**  
Extract the Metric card (BloodTax), MaatVerdict, and BottomNav as standalone components. These are zero-risk lifts with no entanglement.

**Step 2 — Copy the CSS primitives:**  
Take `.stat-card`, `.log-entry`, `.neon-box` (DASHBOARD HTML), `.card:hover` glow (Manifest Orion), and the `@keyframes ticker` (NewsTicker) into a shared stylesheet. Pure CSS, no React coupling.

**Step 3 — Consolidate AgentCard + SystemCard:**  
Merge into one prop-driven `EntityCard` component. Remove the hardcoded lookup maps. This unlocks the most reusable card pattern in the repo.

**Step 4 — Port the Campfire shell:**  
Strip the ritual content, keep the `idle → processing → result` state machine + visual. This becomes a universal async-classification shell.

**Step 5 — Study ARKHON_TRINITY:**  
Don't extract — read. The canvas mandala + Web Audio oscillator is the most technically interesting pattern here. Understand it before considering any immersive interaction work.

---

*Audit complete. 45 components inspected across 10 projects.*  
*No files modified. No implementations invented. Uncertain items marked uncertain.*
