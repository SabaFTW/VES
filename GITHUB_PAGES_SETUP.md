# GitHub Pages setup (VES)

Repo uporablja **en sam** deployment workflow: `.github/workflows/deploy-pwa.yml`.

## 1) Nastavi GitHub Pages na Actions

1. Odpri `Settings -> Pages`
2. Pod **Build and deployment** izberi **Source: GitHub Actions**
3. Shrani

## 2) Deploy flow

- Workflow: `.github/workflows/deploy-pwa.yml`
- Trigger: push na `main` ali ročno (`workflow_dispatch`)
- Build: `npm run build:pages`
- Artifact za Pages: `dist/`

## 3) Lokalni ukazi

```bash
npm ci
npm run build          # lokalni build (base '/')
npm run build:pages    # GitHub Pages build (base '/VES/')
npm run preview
```

## 4) Zakaj je to stabilno

- Samo en workflow deploya na Pages (ni več konfliktov med workflowi).
- `build:pages` vedno nastavi pravilen Vite `base` za repo path `/VES/`.
- Enak build proces lokalno in v CI zmanjša random deployment napake.
