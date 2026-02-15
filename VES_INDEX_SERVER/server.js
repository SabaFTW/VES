const express = require("express");
const fs = require("fs");
const path = require("path");

const app = express();
app.disable("x-powered-by");

const PORT = Number(process.env.PORT || 4500);
const PUBLIC_INDEX_PATH = process.env.PUBLIC_INDEX_PATH || "/VES/MASTER_NAVIGATOR/system_index.json";
const RESEARCH_CATALOG_PATH = process.env.RESEARCH_CATALOG_PATH || "/VES/MASTER_NAVIGATOR/proprietary_research_catalog.json";
const PUBLIC_PREVIEW_ENABLED = process.env.VES_ENABLE_PUBLIC_PREVIEW === "true";
const RESEARCH_PREVIEW_ENABLED = process.env.VES_ENABLE_RESEARCH_PREVIEW === "true";
const PREVIEW_BYTES = Number(process.env.VES_PREVIEW_BYTES || 1200);
const PREVIEW_ROOT = path.resolve(process.env.VES_PREVIEW_ROOT || "/VES");
const ALLOWED_ORIGINS = parseList(process.env.VES_ALLOWED_ORIGINS || "");

const caches = {
  public: { data: null, mtimeMs: null, shaped: null },
  research: { data: null, mtimeMs: null, shaped: null }
};

function parseList(value = "") {
  return value
    .split(",")
    .map(v => v.trim())
    .filter(Boolean);
}

function sanitizeId(raw = "") {
  return raw.replace(/^(\.?\/)+/, "").replace(/^VES\//i, "").trim();
}

function loadJsonFromFile(target, cacheKey) {
  const cache = caches[cacheKey];
  let stat;

  try {
    stat = fs.statSync(target);
  } catch (error) {
    throw new Error("Source unavailable");
  }

  if (cache.data && cache.mtimeMs === stat.mtimeMs) {
    return cache.data;
  }

  try {
    const parsed = JSON.parse(fs.readFileSync(target, "utf-8"));
    cache.data = parsed;
    cache.mtimeMs = stat.mtimeMs;
    cache.shaped = null;
    return parsed;
  } catch (error) {
    throw new Error("Source unreadable");
  }
}

function shapePublicIndex(raw) {
  if (caches.public.shaped) return caches.public.shaped;
  const source = raw?.ves_system_index || {};

  if (!source.categories) {
    throw new Error("Invalid public index schema");
  }

  const categories = {};
  const records = [];

  Object.entries(source.categories).forEach(([name, category]) => {
    const items = Array.isArray(category.items) ? category.items : [];
    const shapedItems = items
      .map(item => {
        const id = sanitizeId(item.path || item.id || item.name || "");
        if (!id) return null;
        const entry = {
          id,
          category: name,
          title: item.title || item.name || id.split("/").pop(),
          description: item.description || "",
          importance: item.importance || category.importance,
          last_update: item.last_update,
          size_kb: item.size_kb
        };
        records.push(entry);
        return entry;
      })
      .filter(Boolean);

    categories[name] = {
      count: category.count || shapedItems.length,
      items: shapedItems
    };
  });

  const shaped = {
    meta: {
      generatedAt: source.generated_at,
      totalDirectories: source.total_directories,
      totalFiles: source.total_files,
      totalSizeKb: source.total_size_kb
    },
    categories,
    records
  };

  caches.public.shaped = shaped;
  return shaped;
}

function shapeResearchCatalog(raw) {
  if (caches.research.shaped) return caches.research.shaped;

  const entries = Array.isArray(raw)
    ? raw
    : Array.isArray(raw?.items)
      ? raw.items
      : Array.isArray(raw?.records)
        ? raw.records
        : Array.isArray(raw?.catalog)
          ? raw.catalog
          : Array.isArray(raw?.data)
            ? raw.data
            : [];

  const records = [];
  const lookup = new Map();

  entries.forEach((item, index) => {
    const id = sanitizeId(item.id || item.uid || item.slug || item.path || `research-${index + 1}`);
    const title = item.title || item.name || `Research ${index + 1}`;
    const record = {
      id,
      title,
      summary: item.summary || item.description || item.abstract || "",
      tags: item.tags || item.topics || [],
      updated_at: item.updated_at || item.last_update || item.modified || item.generated_at || null
    };
    records.push(record);
    lookup.set(id, item);
  });

  const shaped = {
    meta: {
      total: records.length,
      updatedAt: raw?.updated_at || raw?.generated_at || raw?.timestamp || null
    },
    records,
    lookup
  };

  caches.research.shaped = shaped;
  return shaped;
}

function ensurePublicIndex() {
  const raw = loadJsonFromFile(PUBLIC_INDEX_PATH, "public");
  return shapePublicIndex(raw);
}

function ensureResearchCatalog() {
  const raw = loadJsonFromFile(RESEARCH_CATALOG_PATH, "research");
  return shapeResearchCatalog(raw);
}

function filterSearch(records, term, limit = 120) {
  const q = term.toLowerCase();
  const results = [];
  for (const record of records) {
    const haystack = `${record.id} ${record.title} ${record.description || record.summary || ""}`.toLowerCase();
    if (haystack.includes(q)) {
      results.push(record);
      if (results.length >= limit) break;
    }
  }
  return results;
}

function safePreviewFromDisk(id) {
  const rel = sanitizeId(id);
  const target = path.resolve(PREVIEW_ROOT, rel);
  if (!target.startsWith(PREVIEW_ROOT)) {
    throw new Error("Preview path rejected");
  }
  const content = fs.readFileSync(target, "utf-8");
  return {
    preview: content.slice(0, PREVIEW_BYTES),
    truncated: content.length > PREVIEW_BYTES
  };
}

app.use((req, res, next) => {
  const origin = req.headers.origin;
  const allowed = origin && ALLOWED_ORIGINS.includes(origin);
  if (allowed) {
    res.header("Access-Control-Allow-Origin", origin);
    res.header("Vary", "Origin");
    res.header("Access-Control-Allow-Methods", "GET,OPTIONS");
    res.header("Access-Control-Allow-Headers", "Content-Type");
  }
  if (req.method === "OPTIONS") {
    return allowed ? res.sendStatus(204) : res.sendStatus(403);
  }
  next();
});

app.use(express.json());
app.use(express.static(path.join(__dirname, "ui")));

app.get("/api/public/index", (req, res) => {
  try {
    const data = ensurePublicIndex();
    res.json({ meta: data.meta, categories: data.categories });
  } catch (error) {
    res.status(503).json({ error: "Public index unavailable" });
  }
});

app.get("/api/public/search", (req, res) => {
  const q = (req.query.q || "").toString().trim();
  if (!q) return res.status(400).json({ error: "Missing ?q parameter" });

  try {
    const data = ensurePublicIndex();
    const results = filterSearch(data.records, q, Number(req.query.limit) || 120);
    res.json({ query: q, results, total: results.length });
  } catch (error) {
    res.status(503).json({ error: "Public index unavailable" });
  }
});

app.get("/api/public/summary", (req, res) => {
  const id = sanitizeId(req.query.id || "");
  if (!id) return res.status(400).json({ error: "Missing ?id parameter" });

  try {
    const data = ensurePublicIndex();
    const record = data.records.find(item => item.id === id);
    if (!record) return res.status(404).json({ error: "Entry not found" });

    const response = { ...record, previewAvailable: PUBLIC_PREVIEW_ENABLED };

    if (PUBLIC_PREVIEW_ENABLED) {
      try {
        const preview = safePreviewFromDisk(id);
        response.preview = preview.preview;
        response.truncated = preview.truncated;
      } catch (error) {
        response.preview = null;
        response.truncated = false;
        response.previewError = "Preview unavailable";
      }
    }

    res.json(response);
  } catch (error) {
    res.status(503).json({ error: "Public index unavailable" });
  }
});

app.get("/api/research/list", (req, res) => {
  try {
    const data = ensureResearchCatalog();
    const summarized = data.records.map(item => ({
      id: item.id,
      title: item.title,
      summary: item.summary ? item.summary.slice(0, 240) : "",
      tags: item.tags || [],
      updated_at: item.updated_at
    }));
    res.json({ meta: data.meta, records: summarized });
  } catch (error) {
    res.status(503).json({ error: "Research catalog unavailable" });
  }
});

app.get("/api/research/summary", (req, res) => {
  const id = sanitizeId(req.query.id || "");
  if (!id) return res.status(400).json({ error: "Missing ?id parameter" });

  try {
    const data = ensureResearchCatalog();
    const record = data.records.find(item => item.id === id);
    if (!record) return res.status(404).json({ error: "Entry not found" });

    res.json({ ...record, previewAvailable: RESEARCH_PREVIEW_ENABLED });
  } catch (error) {
    res.status(503).json({ error: "Research catalog unavailable" });
  }
});

app.get("/api/research/preview", (req, res) => {
  const id = sanitizeId(req.query.id || "");
  if (!id) return res.status(400).json({ error: "Missing ?id parameter" });
  if (!RESEARCH_PREVIEW_ENABLED) return res.status(403).json({ error: "Research previews disabled" });

  try {
    const data = ensureResearchCatalog();
    const raw = data.lookup?.get(id);
    if (!raw) return res.status(404).json({ error: "Entry not found" });

    const preview = raw.preview || raw.summary || raw.abstract || raw.excerpt || raw.content || "No preview available";
    res.json({ id, preview: preview.slice(0, PREVIEW_BYTES), truncated: preview.length > PREVIEW_BYTES });
  } catch (error) {
    res.status(503).json({ error: "Research catalog unavailable" });
  }
});

app.use((req, res) => {
  res.status(404).json({ error: "Not found" });
});

app.listen(PORT, () => {
  console.log(`Ghostline Gateway running on port ${PORT}`);
});
