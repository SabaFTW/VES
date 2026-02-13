# VES / GHOSTCORE Portal

Repo je bil reorganiziran, da je jasno kaj je **aktivna aplikacija** in kaj je **arhiva**.

## Aktivni app (to je edino, kar vpliva na build/deploy)

- `APP/public/` – Vite root, HTML entrypointi in statični asseti.
- `APP/src/` – JS moduli.
- `vite.config.js` – build konfiguracija (`APP/public` -> `dist/`, base `/VES/`).
- `package.json` – npm skripte.

## Dokumentacija

- `docs/guides/` – setup/deploy navodila.
- `docs/reports/` – implementacijska poročila in checkpointi.
- `docs/reference/` – konceptualni dokumenti in plani.
- `docs/journals/` – dnevniški/archivski zapisi.

## Arhiva

- `legacy/static-pages/` – stare standalone HTML strani.
- `legacy/artifacts/` – večji binarni artefakti (npr. PDF).
- Ostale tematske mape (`ARCHIVE/`, `ASSETS/`, `DATA/`, …) so ohranjene kot vsebinska baza.

## Lokalni zagon

```bash
npm ci
npm run dev
```

## Build za GitHub Pages

```bash
npm run build
```

Output je v `dist/`. Workflow deploya na Pages iz `dist/`.
