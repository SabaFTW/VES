# GitHub Pages setup (VES)

Ta repo zdaj uporablja **GitHub Actions workflow** za deployment Vite builda v `dist/`.

## 1) Nastavi GitHub Pages na Actions

1. Odpri: `Settings -> Pages`
2. Pod **Build and deployment** izberi **Source: GitHub Actions**
3. Shrani.

## 2) Deploy flow

- Workflow datoteka: `.github/workflows/deploy-pages.yml`
- Trigger: push na `main` (ali ročno z `workflow_dispatch`)
- Build command: `npm run build:pages`
- Artifact: `dist/`

## 3) Lokalni ukazi

```bash
npm ci
npm run build          # local base '/'
npm run build:pages    # production base '/VES/'
npm run preview
```

## 4) Zakaj je to bolj stabilno

- Ne deployamo več “root branch mape”, ampak točno build artifact.
- `vite.config.js` uporablja ločen mode `github-pages`, da je `base` pravilen (`/VES/`).
- Enotna pot za CI in lokalni build zmanjšuje “na mojem računalniku dela” napake.
