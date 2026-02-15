# VES FRONTEND REGISTRY MAP

**Location:** `/home/saba/core/`
**Architecture:** Modular vanilla JavaScript (no framework)
**Entry Point:** `/home/saba/index.html`
**Loading:** Sequential script loading via `main.js`

---

## ARCHITECTURE OVERVIEW

```
index.html (shell)
    ↓
main.js (orchestrator)
    ↓
├── services/api.js         (HTTP client)
├── services/markdown.js    (MD renderer)
├── router.js               (hash routing)
├── components/nav.js       (sidebar)
└── views/
    ├── dashboard.js        (system overview)
    ├── reports.js          (report list)
    └── docs.js             (doc explorer)
```

**Pattern:** Shell → Core → Services → Router → Components → Views

---

## FILE INVENTORY

| File | Type | Size | Purpose |
|------|------|------|---------|
| `main.js` | Module | ~3KB | Application bootstrapper |
| `router.js` | Module | ~2KB | Hash-based routing |
| `services/api.js` | Service | ~2KB | Agent API client |
| `services/markdown.js` | Service | ~2KB | Markdown renderer |
| `components/nav.js` | Component | ~3KB | Fixed sidebar navigation |
| `views/dashboard.js` | View | ~5KB | System overview + stats |
| `views/reports.js` | View | ~3KB | Report list view |
| `views/docs.js` | View | ~8KB | Document explorer |
| `style.css` | Styles | ~2KB | Global styles |
| `app.js` | Unused | ~1KB | Legacy placeholder |

**Total:** 10 files, ~31KB uncompressed

---

## LOAD ORDER

### Phase 1: HTML Shell (`index.html`)

```html
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="./core/style.css" />
</head>
<body>
  <div id="app"></div>
  <script type="module" src="./core/main.js"></script>
</body>
</html>
```

**Dependencies:**
- External: Tailwind CSS (CDN)
- External: Chart.js (CDN)
- External: Font Awesome (CDN)

---

### Phase 2: Core Initialization (`main.js`)

**Execution Order:**

```javascript
1. Define loadScript() helper
2. Define init() function
3. Show loading spinner in #app
4. Load services:
   - services/api.js
   - services/markdown.js
   - router.js
5. Load components:
   - components/nav.js
6. Load views:
   - views/dashboard.js
   - views/reports.js
   - views/docs.js
7. Check agent health
8. Register routes
9. Initialize navigation
10. Initialize router
```

**Key Function:**

```javascript
async function loadScript(src) {
  return new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.src = src;
    script.onload = () => resolve();
    script.onerror = (err) => reject(err);
    document.body.appendChild(script);
  });
}
```

**Result:** All modules loaded and registered before first render.

---

## MODULE DEPENDENCY GRAPH

### `services/api.js`

**Namespace:** `window.VES.API`

**Exports:**
- `health()` → `GET /health`
- `readFile(path)` → `GET /read?path=`
- `listDir(path)` → `GET /list?path=`
- `scanSystem()` → `GET /scan`
- `listReports()` → `GET /reports`

**Dependencies:** None

**Used By:**
- `views/dashboard.js` (calls `scanSystem()`)
- `views/reports.js` (calls `listReports()`, `readFile()`)
- `views/docs.js` (calls `listDir()`, `readFile()`)

---

### `services/markdown.js`

**Namespace:** `window.VES.Markdown`

**Exports:**
- `render(markdown)` → Returns HTML string

**Dependencies:** None

**Used By:**
- `views/docs.js` (renders MD file content)
- `views/reports.js` (renders report content)

---

### `router.js`

**Namespace:** `window.VES.Router`

**Exports:**
- `register(name, viewFn)` - Register route
- `navigate(name)` - Change route
- `init()` - Start routing

**Dependencies:**
- `window.VES.routes` (object)

**Used By:**
- `main.js` (registers routes, calls `init()`)
- `components/nav.js` (changes hash to navigate)

**Mechanism:** Hash-based routing
- Listens to `hashchange` event
- Reads `window.location.hash`
- Calls registered view function

---

### `components/nav.js`

**Namespace:** `window.VES.Navigation`

**Exports:**
- `render()` - Create nav DOM element
- `init()` - Attach nav to body

**Dependencies:**
- Reads `window.location.hash` to highlight active route

**Used By:**
- `main.js` (calls `init()`)

**Side Effects:**
- Appends `<nav id="ves-nav">` to `<body>`
- Sets `#app` left margin to `280px`

---

### `views/dashboard.js`

**Namespace:** `window.VES.DashboardView`

**Signature:** `async function(mountEl)`

**Dependencies:**
- `VES.API.scanSystem()`

**Renders:**
- Summary cards (total dirs, MD files, HTML, JSON, size)
- Directory cards (file type breakdown, subdirs)
- Root files list

**Mount Point:** `#app`

---

### `views/reports.js`

**Namespace:** `window.VES.ReportsView`

**Signature:** `async function(mountEl)`

**Dependencies:**
- `VES.API.listReports()`
- `VES.API.readFile()`
- `VES.Markdown.render()`

**Renders:**
- List of Cloud Constellation reports
- Click → renders report content

**Mount Point:** `#app`

---

### `views/docs.js`

**Namespace:** `window.VES.DocsView`

**Signature:** `async function(mountEl)`

**Dependencies:**
- `VES.API.listDir()`
- `VES.API.readFile()`
- `VES.Markdown.render()`

**Renders:**
- Left sidebar: directory tree
- Right panel: file list or rendered MD content
- Breadcrumb navigation

**Mount Point:** `#app`

**State Management:**
- `currentPath` (string)
- `breadcrumb` (array)

---

## ROUTE REGISTRY

Routes are registered in `main.js` (lines 80-82):

```javascript
VES.Router.register('dashboard', VES.DashboardView);
VES.Router.register('reports', VES.ReportsView);
VES.Router.register('docs', VES.DocsView);
```

**URL Mapping:**

| Hash | View | Function |
|------|------|----------|
| `#dashboard` | Dashboard | `VES.DashboardView` |
| `#reports` | Reports | `VES.ReportsView` |
| `#docs` | Docs | `VES.DocsView` |
| (empty) | Dashboard | `VES.DashboardView` (default) |

---

## GLOBAL NAMESPACE

**Structure:**

```javascript
window.VES = {
  API: {
    health: Function,
    readFile: Function,
    listDir: Function,
    scanSystem: Function,
    listReports: Function
  },
  Markdown: {
    render: Function
  },
  Router: {
    routes: Object,
    currentView: String,
    register: Function,
    navigate: Function,
    init: Function
  },
  Navigation: {
    render: Function,
    createNavItem: Function,
    init: Function
  },
  DashboardView: AsyncFunction,
  ReportsView: AsyncFunction,
  DocsView: AsyncFunction
}
```

**Initialization:** Each module extends `window.VES` on load.

---

## EXTERNAL DEPENDENCIES

**CDN Resources (from `index.html`):**

1. **Tailwind CSS**
   - URL: `https://cdn.tailwindcss.com`
   - Purpose: Utility-first CSS framework
   - Usage: Minimal (mostly custom inline styles)

2. **Chart.js**
   - URL: `https://cdn.jsdelivr.net/npm/chart.js`
   - Purpose: Data visualization
   - Usage: Currently unused in active views

3. **Font Awesome**
   - URL: `https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css`
   - Purpose: Icon library
   - Usage: Minimal (mostly emoji icons used instead)

**Risk:** CDN availability required for page load. Consider local fallback.

---

## INITIALIZATION SEQUENCE

```
T+0ms    index.html loads
T+50ms   Tailwind, Chart.js, Font Awesome load from CDN
T+100ms  core/style.css loads
T+150ms  core/main.js executes
T+200ms  Loading spinner appears in #app
T+250ms  services/api.js loads
T+300ms  services/markdown.js loads
T+350ms  router.js loads
T+400ms  components/nav.js loads
T+450ms  views/dashboard.js loads
T+500ms  views/reports.js loads
T+550ms  views/docs.js loads
T+600ms  Agent health check (async)
T+650ms  Routes registered
T+700ms  Navigation initialized
T+750ms  Router initialized
T+800ms  First view renders
```

**Total Cold Start:** ~800ms (on localhost with cached CDN)

---

## VIEW LIFECYCLE

### View Function Pattern

```javascript
VES.ExampleView = async function(mountEl) {
  // 1. Clear mount point
  mountEl.innerHTML = '<p>Loading...</p>';

  // 2. Fetch data
  const data = await VES.API.someMethod();

  // 3. Render HTML
  mountEl.innerHTML = `<div>...</div>`;

  // 4. Attach event listeners
  mountEl.querySelector('#btn').addEventListener('click', handler);
}
```

**Every view:**
- Is an async function
- Receives `mountEl` (the `#app` div)
- Manages its own DOM
- Cleans up on unmount (router clears `innerHTML`)

---

## COMMUNICATION FLOW

```
User clicks nav link
    ↓
Hash changes (#dashboard → #docs)
    ↓
Router detects hashchange event
    ↓
Router finds view function for new hash
    ↓
View function called with #app element
    ↓
View fetches data via VES.API
    ↓
Agent responds with data
    ↓
View renders HTML
    ↓
User sees new view
```

**Data Flow:** User → Router → View → API → Agent → API → View → User

---

## UNUSED FILES

### `core/app.js`

**Status:** Loaded but unused

**Content:** Empty or placeholder code

**Action:** Can be deleted (not referenced by any module)

---

## DEPENDENCY RESOLUTION

**No conflicts:**
- All modules extend `window.VES`
- No overlapping property names
- Sequential loading ensures availability

**Load Order Requirements:**

| Module | Must Load Before |
|--------|------------------|
| `api.js` | All views (they call `VES.API`) |
| `markdown.js` | `docs.js`, `reports.js` (they call `VES.Markdown.render`) |
| `router.js` | `main.js` route registration |
| All views | `router.init()` call |

**Current order satisfies all requirements.**

---

## EXTENSION POINTS

To add a new view:

1. Create `/core/views/newview.js`
2. Define `VES.NewView = async function(mountEl) { ... }`
3. Add to `main.js` load sequence: `await loadScript('./core/views/newview.js')`
4. Register route: `VES.Router.register('newview', VES.NewView)`
5. Add nav item in `components/nav.js`

**Example:** Adding a settings view

```javascript
// In main.js:
await loadScript('./core/views/settings.js');
VES.Router.register('settings', VES.SettingsView);

// In nav.js:
${this.createNavItem('settings', '⚙️', 'Settings', currentHash === 'settings')}
```

**No refactoring needed** - architecture is append-only for new views.

---

## SUMMARY

**Architecture Type:** Modular vanilla JS (no build step)
**Total Modules:** 10 files
**Dependency Management:** Global namespace (`window.VES`)
**Routing:** Hash-based client-side routing
**State:** Per-view local state (no global store)
**Build:** None (runs directly in browser)

**Key Strengths:**
- Zero build complexity
- Debuggable in browser
- Fast load times
- Easy to extend

**Key Constraints:**
- No TypeScript
- No tree shaking
- CDN dependencies
- Global namespace pollution

**Overall:** Intentionally simple architecture suitable for a single-user localhost PWA.
