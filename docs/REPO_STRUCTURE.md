# Repository Structure (Post-cleanup)

This repository was reorganized to keep the active app separate from documents and legacy pages.

## Active runtime

- `APP/public` – Vite root (served in dev, built in production).
- `APP/src` – JavaScript modules powering the portal.
- `vite.config.js` – Vite config with dynamic `VITE_BASE_PATH` support.

## Documentation

- `docs/guides` – setup/deploy/integration guides.
- `docs/project` – conceptual and project-level notes.
- `docs/journals` – timeline journals and terminal logs.

## Legacy/static archive

- `web/legacy` – archived standalone HTML files not used by Vite app.
- `assets/archive` – archived binary files.

## Scripts

- `scripts/start.sh` – local dev startup helper.
- `scripts/github_token_fix.sh` – helper script.

## NPM scripts

- `npm run build` → local/default base build.
- `npm run build:pages` → GitHub Pages build (`/VES/` base).
- `npm run deploy:github` → Pages build + publish `dist` via `gh-pages`.
