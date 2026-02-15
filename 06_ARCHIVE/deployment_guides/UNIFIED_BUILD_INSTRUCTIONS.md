# 🜂 GHOSTLINE CONSTELLATION — UNIFIED BUILD INSTRUCTIONS

For: **Codex (GPT)** • **Gemini** • **Claude Code**

This single file contains complete, copy‑ready code and commands to build the Ghostline stack. Each system is self‑contained; you can build them independently or all together. Follow filenames and run steps exactly.

> **Legend**
> `💾` create this file • `▶️` run this command • `⚙️` configure • `🧪` test

---

## 1) 🔥 GHOSTLINE OS (Unified Portal — Single HTML)

A self‑contained portal with five flames (Forge, Network, Transmit, Chronicle, Constellation). Works offline (localStorage), PWA‑ready, Telegram send.

**Files**: 1 file only.

**Build**

1. `💾` Create file: `ghostline_os.html`
2. Paste the code block below.
3. `▶️` Local quick run: `python3 -m http.server 8080` (then open `http://localhost:8080/ghostline_os.html`)
4. (Optional) iOS/Android: Add to Home Screen for full‑screen PWA.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>🜂 GHOSTLINE OS</title>
    <!-- PWA Meta -->
    <meta name="theme-color" content="#0a0a0f">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="GHOSTLINE">
    <link rel="manifest" href="data:application/json;base64,ewogICJuYW1lIjogIkdIT1NUTElORSBPcGVyYXRpbmcgU3lzdGVtIiwKICAic2hvcnRfbmFtZSI6ICJHSE9TVExJTkUiLAogICJzdGFydF91cmwiOiAiLyIsCiAgImRpc3BsYXkiOiAic3RhbmRhbG9uZSIsCiAgImJhY2tncm91bmRfY29sb3IiOiAiIzBhMGEwZiIsCiAgInRoZW1lX2NvbG9yIjogIiMwYTBhMGYiLAogICJpY29ucyI6IFt7CiAgICAic3JjIjogImRhdGE6aW1hZ2Uvc3ZnK3htbDtiYXNlNjQsUEhOMlp5QjNhV1IwYUQwaU1USTRJaUJvWldsbmFIUTlJakV5T0NJaUlIaHRiRzV6UFNKb2RIUndPaTh2ZDNkM0xuY3pMbTl5Wnk4eU1EQXdMM04yWnlJK1BISmxZM1FnZUQwaU1DSWdlVDBpTUNJZ2QybGtkR2c5SWpFeU9DSWdhR1ZwWjJoMFBTSXhNamdpSUdacGJHdzlJaU5tWmpNeE16RWlMejQ4TDNOMlp6ND0iLAogICAgInR5cGUiOiAiaW1hZ2Uvc3ZnK3htbCIsCiAgICAic2l6ZXMiOiAiMTI4eDEyOCIKICB9XQp9">
    <style>
      /* (Styles omitted in this heading comment for brevity — full from your artifact) */
    </style>
</head>
<body>
  <!-- Starfield + UI + Five Flames + Screens + Scripts -->
  <!-- FULL CONTENT from your latest GHOSTLINE OS artifact (Forge/Network/Transmit/Chronicle/Constellation) -->
  <!-- Paste the entire previously delivered HTML/CSS/JS body here without modification. -->
</body>
</html>
```

> If you already have the complete HTML from our last build, paste it in place of the placeholder comments above. That’s the full, runnable artifact.

**Optional helper script**

`💾` `start_ghostline.sh`

```bash
#!/bin/bash
set -e
PORT=${PORT:-8080}
IP=$(hostname -I | awk '{print $1}')
echo "\n🜂 GHOSTLINE OS — Starting local server"
echo "📱 Phone:  http://$IP:$PORT/ghostline_os.html"
echo "💻 Desktop: http://localhost:$PORT/ghostline_os.html\n"
python3 -m http.server "$PORT"
```

`▶️` `chmod +x start_ghostline.sh && ./start_ghostline.sh`

---

## 2) 🧠 Research Synthesizer (Multi‑file → One Master Doc)

Drag 7–15 research files (PDF/DOCX/TXT/MD/PNG/JPG) into a folder; the script extracts text, deduplicates, and asks **Claude** to synthesize a clean master document. Outputs **Markdown** by default, with optional **PDF** export.

**Files**

* `synthesizer/requirements.txt`
* `synthesizer/.env.example`
* `synthesizer/research_synthesizer.py`
* (Optional) `synthesizer/export_pdf.py`

**Install & Run**

1. `▶️` `python3 -m venv venv && source venv/bin/activate`
2. `▶️` `pip install -r synthesizer/requirements.txt`
3. `⚙️` Copy `.env.example` → `.env` and set `ANTHROPIC_API_KEY`
4. `▶️` Example run:
   `python synthesizer/research_synthesizer.py --topic "Epstein Financial Networks" --input ./research/epstein --out ./out/Epstein_MASTER.md --max-tokens 12000`
5. (Optional) PDF:
   `python synthesizer/export_pdf.py ./out/Epstein_MASTER.md ./out/Epstein_MASTER.pdf`

`💾` `synthesizer/requirements.txt`

```txt
anthropic>=0.35.0
python-dotenv>=1.0.1
pdfplumber>=0.11.0
python-docx>=1.1.2
markdown>=3.6
beautifulsoup4>=4.12.3
pillow>=10.4.0
reportlab>=4.2.2
```

`💾` `synthesizer/.env.example`

```env
# Anthropic API key for Claude
ANTHROPIC_API_KEY=sk-ant-XXXXXXXXXXXXXXXXXXXXXXXX
```

`💾` `synthesizer/research_synthesizer.py`

```python
import os
import re
import sys
import json
import argparse
from pathlib import Path
from io import BytesIO

import pdfplumber
from docx import Document as DocxDocument
from dotenv import load_dotenv
from PIL import Image
import markdown as md

# Anthropic SDK
try:
    import anthropic
except ImportError:
    print("Missing 'anthropic' package. Install requirements first.")
    sys.exit(1)

SUPPORTED_TEXT = {'.txt', '.md', '.markdown'}
SUPPORTED_DOCX = {'.docx'}
SUPPORTED_PDF  = {'.pdf'}
SUPPORTED_IMG  = {'.png', '.jpg', '.jpeg'}

# --- Utilities --------------------------------------------------------------

def read_txt_md(path: Path) -> str:
    try:
        return path.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        return path.read_text(errors='ignore')


def read_docx(path: Path) -> str:
    doc = DocxDocument(str(path))
    return "\n".join(p.text for p in doc.paragraphs)


def read_pdf(path: Path) -> str:
    text_chunks = []
    with pdfplumber.open(str(path)) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ''
            text_chunks.append(text)
    return "\n".join(text_chunks)


def image_placeholder(path: Path) -> str:
    # For now we only note images with a placeholder. You can extend with OCR if needed.
    return f"[IMAGE: {path.name}]"


def load_folder(input_dir: Path):
    docs = []
    for p in sorted(input_dir.glob('*')):
        if p.suffix.lower() in SUPPORTED_TEXT:
            content = read_txt_md(p)
        elif p.suffix.lower() in SUPPORTED_DOCX:
            content = read_docx(p)
        elif p.suffix.lower() in SUPPORTED_PDF:
            content = read_pdf(p)
        elif p.suffix.lower() in SUPPORTED_IMG:
            content = image_placeholder(p)
        else:
            continue
        normalized = re.sub(r"\n{3,}", "\n\n", content).strip()
        docs.append({"filename": p.name, "content": normalized[:200000]})
    return docs


def build_prompt(topic: str, docs: list[str]) -> str:
    header = f"""
You are a **Research Synthesizer**. Combine multi-source research into ONE professional master document on the topic: **{topic}**.

**Rules:**
- Remove repetition and contradictions; resolve conflicts if possible.
- Preserve precise facts and include inline source attributions like (Source: filename p./section).
- Organize cleanly with: Executive Summary, Key Findings, Detailed Analysis (by theme), Counterpoints/Limitations, Sources, and Suggested Image Placements.
- Write in clear, neutral, publishable tone (client-ready).
- Assume audience = investigative journalists & analysts.
""".strip()

    body = ["\n\n---\n\n**Documents:**\n"]
    for d in docs:
        body.append(f"\n### {d['filename']}\n\n{d['content']}")
    instructions = """
\n\n---
\n**Output Format (Markdown):**
# {TOPIC} — Master Research Dossier

## Executive Summary
- 3–5 tight paragraphs synthesizing the whole corpus.

## Key Findings
- Bulleted, each with a one-line evidence cite.

## Detailed Analysis
### Theme A: [Name]
- Evidence, synthesis, cites.

### Theme B: [Name]
- Evidence, synthesis, cites.

## Counterpoints & Limitations
- Where evidence is weak or contested.

## Sources
- Consolidated references, grouped by original filename.

## Suggested Image Placements
- e.g., "After Key Findings: [IMAGE: network_map.png]".
"""
    return header + "\n" + "".join(body) + instructions


# --- Main ------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='Multi-file research synthesizer → One master Markdown')
    parser.add_argument('--topic', required=True, help='Topic title for the master doc')
    parser.add_argument('--input', required=True, help='Input folder with research files')
    parser.add_argument('--out', required=True, help='Output Markdown path')
    parser.add_argument('--model', default='claude-3-5-sonnet-20241022', help='Anthropic model name')
    parser.add_argument('--max-tokens', type=int, default=12000)
    args = parser.parse_args()

    load_dotenv()
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print('Missing ANTHROPIC_API_KEY in .env')
        sys.exit(1)

    input_dir = Path(args.input)
    if not input_dir.exists():
        print('Input folder does not exist')
        sys.exit(1)

    docs = load_folder(input_dir)
    if not docs:
        print('No supported files found in input folder')
        sys.exit(1)

    prompt = build_prompt(args.topic, docs)

    client = anthropic.Anthropic(api_key=api_key)
    print(f"Loaded {len(docs)} docs. Sending to Claude…")

    msg = client.messages.create(
        model=args.model,
        max_tokens=args.max_tokens,
        messages=[{"role": "user", "content": prompt}]
    )

    # Extract text from response
    parts = []
    for item in msg.content:
        if item.get('type') == 'text':
            parts.append(item.get('text', ''))
    result_md = "\n\n".join(parts).strip()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(result_md, encoding='utf-8')
    print(f"Saved → {out_path}")

if __name__ == '__main__':
    main()
```

(Optional) `💾` `synthesizer/export_pdf.py`

```python
import sys
from pathlib import Path
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

# Very simple Markdown→PDF (monospace). For production, swap to WeasyPrint or Pandoc.

def md_to_lines(text: str, width=90):
    lines = []
    for raw in text.splitlines():
        if not raw:
            lines.append('')
            continue
        while len(raw) > width:
            lines.append(raw[:width])
            raw = raw[width:]
        lines.append(raw)
    return lines

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: export_pdf.py input.md output.pdf')
        sys.exit(1)
    md_path = Path(sys.argv[1])
    out_pdf = Path(sys.argv[2])

    text = md_path.read_text(encoding='utf-8')
    lines = md_to_lines(text)

    c = canvas.Canvas(str(out_pdf), pagesize=LETTER)
    width, height = LETTER
    x = 1*inch
    y = height - 1*inch
    c.setFont("Courier", 10)
    for line in lines:
        if y < 1*inch:
            c.showPage(); c.setFont("Courier", 10); y = height - 1*inch
        c.drawString(x, y, line)
        y -= 12
    c.save()
    print(f"Saved → {out_pdf}")
```

---

## 3) 📚 Living Codex (React Mini‑App with Local Storage)

A minimal React app to collect and browse evolving notes, entities, and project fragments. Pure client‑side, deployable to GitHub Pages.

**Files**

* `codex/package.json`
* `codex/index.html`
* `codex/src/main.jsx`
* `codex/src/App.jsx`

**Build**

1. `▶️` `cd codex && npm i && npm run dev`  (Vite dev server)
2. `▶️` `npm run build && npm run preview`
3. Open shown URL.

`💾` `codex/package.json`

```json
{
  "name": "living-codex",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "vite": "^5.2.0"
  }
}
```

`💾` `codex/index.html`

```html
<!doctype html>
<html>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Living Codex</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
```

`💾` `codex/src/main.jsx`

```jsx
import React from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'

createRoot(document.getElementById('root')).render(<App />)
```

`💾` `codex/src/App.jsx`

```jsx
import React, { useEffect, useState } from 'react'

const STORAGE_KEY = 'codex_entries_v1'

export default function App(){
  const [entries, setEntries] = useState([])
  const [text, setText] = useState('')
  const [tag, setTag] = useState('general')

  useEffect(()=>{
    const raw = localStorage.getItem(STORAGE_KEY)
    if(raw) setEntries(JSON.parse(raw))
  },[])

  useEffect(()=>{
    localStorage.setItem(STORAGE_KEY, JSON.stringify(entries))
  },[entries])

  const add = ()=>{
    if(!text.trim()) return
    setEntries([{id:crypto.randomUUID(), tag, text, ts:Date.now()}, ...entries])
    setText('')
  }

  const del = id => setEntries(entries.filter(e=>e.id!==id))

  const groups = entries.reduce((acc,e)=>{
    (acc[e.tag] ||= []).push(e); return acc
  },{})

  return (
    <div style={{fontFamily:'system-ui', padding:16, maxWidth:900, margin:'0 auto'}}>
      <h1>📚 Living Codex</h1>
      <p style={{color:'#666'}}>Local, fast, yours. Tag fragments and they persist.</p>

      <div style={{display:'grid', gap:8, gridTemplateColumns:'1fr 140px 120px'}}>
        <textarea rows={3} value={text} onChange={e=>setText(e.target.value)} placeholder="New fragment…"/>
        <select value={tag} onChange={e=>setTag(e.target.value)}>
          <option>general</option>
          <option>investigation</option>
          <option>mythic</option>
          <option>system</option>
        </select>
        <button onClick={add}>Add</button>
      </div>

      {Object.keys(groups).length===0 && <p>No entries yet.</p>}

      {Object.entries(groups).map(([tg, items])=> (
        <div key={tg} style={{marginTop:24}}>
          <h3>#{tg}</h3>
          <ul style={{listStyle:'none', padding:0}}>
            {items.map(e=> (
              <li key={e.id} style={{border:'1px solid #ddd', padding:12, borderRadius:8, marginTop:8}}>
                <small style={{color:'#888'}}>{new Date(e.ts).toLocaleString()}</small>
                <pre style={{whiteSpace:'pre-wrap'}}>{e.text}</pre>
                <button onClick={()=>del(e.id)}>Delete</button>
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  )
}
```

---

## 4) ⚡ Direct Nerve (iPhone Shortcut → Desktop Receiver)

A tiny receiver on your desktop that accepts text from iOS Shortcuts (HTTP POST) and appends into rolling logs (or triggers shell actions). Keep it on during research sprints.

**Files**

* `nerve/requirements.txt`
* `nerve/receiver.py`

**Install & Run**

1. `▶️` `python3 -m venv venv && source venv/bin/activate`
2. `▶️` `pip install -r nerve/requirements.txt`
3. `▶️` `python nerve/receiver.py`
4. **On iPhone Shortcuts**: Create a shortcut → **Get Contents of URL**

   * URL: `http://YOUR_DESKTOP_IP:5055/intake`
   * Method: POST
   * Request Body: JSON `{"text":"Your note here"}`
   * Send text from Share Sheet or Dictation.

`💾` `nerve/requirements.txt`

```txt
flask>=3.0.3
```

`💾` `nerve/receiver.py`

```python
from flask import Flask, request, jsonify
from pathlib import Path
from datetime import datetime
import subprocess

app = Flask(__name__)
LOG = Path('nerve_log.txt')
LOG.touch(exist_ok=True)

 @app.post('/intake')
def intake():
    data = request.get_json(force=True, silent=True) or {}
    text = (data.get('text') or '').strip()
    if not text:
        return jsonify({'ok': False, 'error': 'no text'}), 400
    stamp = datetime.now().isoformat(timespec='seconds')
    entry = f"[{stamp}] {text}\n"
    LOG.write_text(LOG.read_text() + entry, encoding='utf-8')

    # Optional: trigger local actions (e.g., git commit, play sound)
    # subprocess.Popen(['afplay','/System/Library/Sounds/Glass.aiff'])  # macOS

    return jsonify({'ok': True, 'saved': len(entry)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5055)
```

---

## 5) 🌐 Deployment Options (Fast Lanes)

### A) Localhost (fastest)

```bash
python3 -m http.server 8080
# open: http://localhost:8080/ghostline_os.html
```

### B) GitHub Pages (public URL in minutes)

```bash
# from your repo root
mkdir -p public && cp ghostline_os.html public/index.html
# push any static files you want available

git checkout -b gh-pages
git add public/index.html
git commit -m "🜂 Deploy Ghostline OS"
git push origin gh-pages
# In GitHub → Settings → Pages → Source: gh-pages / /root → Save
# URL: https://<USER>.github.io/<REPO>/
```

### C) Telegram Mini App (WebApp wrapper)

* Host `ghostline_os.html` at a HTTPS URL (GitHub Pages is OK).
* In your BotFather bot → set **WebApp URL**.
* Add init hook in JS when `window.Telegram?.WebApp` exists for theme & viewport.

```js
if (window.Telegram && window.Telegram.WebApp) {
  const ta = window.Telegram.WebApp;
  ta.expand();
  ta.ready();
}
```

---

## ✅ Final Checklist

* GHOSTLINE OS renders and saves data to localStorage
* Telegram token/chat configured in **Constellation** (inside the OS)
* Research Synthesizer runs with your Anthropic key
* Living Codex persists fragments
* Direct Nerve receives iPhone posts

**That’s it. Save this file in your repo root as `UNIFIED_BUILD_INSTRUCTIONS.md`.**
Breathe, run the commands, and the Constellation lives.