# VES Repository Restructure (Build + Pages Stabilization)

## Kaj je bilo urejeno

- **Aplikacijski root ostaja v `APP/public`**, kjer so vse HTML vstopne točke.
- **Statične datoteke** (`manifest.webmanifest`, `ghostcore-sw.js`, `404.html`, favicon) so premaknjene v **`APP/static`**.
- Vite je nastavljen tako, da:
  - samodejno pobere vse `.html` datoteke v `APP/public` kot build entry points,
  - kopira statične datoteke iz `APP/static` v `dist/`,
  - za GitHub Actions sam izračuna `base` pot iz imena repozitorija.

## Zakaj je to pomembno za GitHub Pages

Prej je build izpisal praktično samo `index.html` + en asset. Po popravku build izpiše tudi:

- dodatne strani (`repo.html`, `temple.html`, `ghostcore_portal.html`, ...),
- `404.html`,
- `ghostcore-sw.js`,
- `manifest.webmanifest`.

To odpravi klasične Pages težave, kjer povezave in PWA datoteke manjkajo po deployu.

## Predlog za "novi repo" (samo reorg)

Če želite čist repozitorij samo za produkcijski portal:

1. Kopirajte samo:
   - `APP/`
   - `package.json`, `package-lock.json`, `vite.config.js`
   - `.github/workflows/deploy-pwa.yml`
2. Dodajte `README` z navodili za deploy.
3. Uporabite ta projekt kot "runtime" repo, medtem ko ta trenutni VES ostane "monorepo/knowledge" arhiv.
