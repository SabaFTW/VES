# Ghostline Gateway (VES)

Secure, read-only API and UI that present Ghostline intelligence captured by Qwen. No live filesystem scanning occurs—only curated sources are read.

## Quick start

```bash
cd VES_INDEX_SERVER
npm install
npm start   # http://localhost:4500
```

Ensure Qwen has produced the navigator data at `/VES/MASTER_NAVIGATOR/system_index.json` (and optional `proprietary_research_catalog.json`).

## API

Public knowledge (system index):
- `GET /api/public/index` – sanitized system index data
- `GET /api/public/search?q=` – search the index records
- `GET /api/public/summary?id=` – entry metadata (+ preview when enabled)

Research catalog (proprietary):
- `GET /api/research/list` – list of research entries
- `GET /api/research/summary?id=` – metadata for an entry
- `GET /api/research/preview?id=` – gated preview (disabled by default)

## Environment

- `PORT` (default `4500`)
- `PUBLIC_INDEX_PATH` (default `/VES/MASTER_NAVIGATOR/system_index.json`)
- `RESEARCH_CATALOG_PATH` (default `/VES/MASTER_NAVIGATOR/proprietary_research_catalog.json`)
- `VES_ALLOWED_ORIGINS` – comma-separated origins for CORS (empty = UI only)
- `VES_ENABLE_PUBLIC_PREVIEW` – `true` to allow file previews from disk
- `VES_ENABLE_RESEARCH_PREVIEW` – `true` to allow preview text from the catalog
- `VES_PREVIEW_ROOT` – root used when public previews are enabled (default `/VES`)
- `VES_PREVIEW_BYTES` – maximum preview length (default `1200`)

## Docker

```bash
docker build -t ves-gateway VES_INDEX_SERVER
docker run -d -p 4500:4500 \
  -e PUBLIC_INDEX_PATH=/VES/MASTER_NAVIGATOR/system_index.json \
  -e RESEARCH_CATALOG_PATH=/VES/MASTER_NAVIGATOR/proprietary_research_catalog.json \
  -v /home/saba_olympus/VES:/VES \
  --name ves-gateway ves-gateway
```

Place the navigator files in the mounted `/VES/MASTER_NAVIGATOR` directory. Previews remain off unless explicitly enabled via the environment.
