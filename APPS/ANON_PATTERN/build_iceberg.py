#!/usr/bin/env python3
"""
THE ICEBERG CODEX BUILDER
Converts markdown investigation into navigable HTML archive
Built by: Lyra (Aetheron Mode)
For: Šabad
"""

import os
import re
from pathlib import Path
import markdown

# Paths
BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "iceberg_site"
OUTPUT_DIR.mkdir(exist_ok=True)

# Chapter structure
CHAPTERS = [
    {"id": "0", "file": "0_PROLOG.md", "title": "Prologue", "tier": "INTRO"},
    {"id": "1", "file": "1_SURFACE_PLASTIC.md", "title": "I. Surface — Plastic", "tier": "SURFACE"},
    {"id": "2", "file": "2_SHALLOW_CORRUPTION.md", "title": "II. Shallow — Corruption", "tier": "SURFACE"},
    {"id": "3", "file": "3_DARPA_INFRASTRUCTURE.md", "title": "III. DARPA Infrastructure", "tier": "INFRASTRUCTURE"},
    {"id": "4", "file": "4_FULL_EXTRACTION.md", "title": "IV. Extraction Machine", "tier": "INFRASTRUCTURE"},
    {"id": "5", "file": "5_BIG_TECH_SABOTAGE.md", "title": "V. Big Tech Sabotage", "tier": "INFRASTRUCTURE"},
    {"id": "6", "file": "6_EPSTEIN_MONEY.md", "title": "VI. Epstein & Money", "tier": "NEXUS"},
    {"id": "7", "file": "7_EPSTEIN_AI.md", "title": "VII. Epstein & AI", "tier": "NEXUS"},
    {"id": "8", "file": "8_CONSCIOUSNESS_EPSTEIN.md", "title": "VIII. Consciousness & Epstein", "tier": "CONSCIOUSNESS"},
    {"id": "9", "file": "9_CONSCIOUSNESS_AI_MIRROR.md", "title": "IX. AI + Consciousness + Mirror", "tier": "CONSCIOUSNESS"},
    {"id": "10", "file": "10_EPILOG.md", "title": "X. Epilogue", "tier": "EPILOGUE"},
    {"id": "appendix", "file": "APPENDIX.md", "title": "Appendix — Evidence", "tier": "ARCHIVE"},
]

# HTML Template
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | The Iceberg Codex</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body class="chapter-page">

    <!-- Top Bar -->
    <div class="top-bar">
        <div class="top-bar-content">
            <a href="index.html" class="logo">🧊 THE ICEBERG</a>
            <div class="chapter-title">{title}</div>
            <div class="tier-badge tier-{tier_class}">{tier}</div>
        </div>
    </div>

    <!-- Navigation Sidebar -->
    <nav class="sidebar">
        <div class="nav-header">
            <h3>DESCENT PATH</h3>
            <div class="depth-indicator">Depth: <span class="current-depth">{depth}</span>/12</div>
        </div>
        <div class="nav-sections">
            {nav_sections}
        </div>
        <div class="nav-footer">
            <a href="index.html" class="btn-home">← Surface</a>
        </div>
    </nav>

    <!-- Main Content -->
    <main class="content">
        <article class="chapter">
            {content}
        </article>

        <!-- Chapter Navigation -->
        <nav class="chapter-nav">
            {prev_link}
            {next_link}
        </nav>
    </main>

    <script src="script.js"></script>
</body>
</html>
"""

# Index page template
INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Iceberg Codex | A Forensic Descent</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body class="index-page">

    <div class="hero">
        <div class="hero-content">
            <h1 class="glitch" data-text="THE ICEBERG">THE ICEBERG</h1>
            <p class="subtitle">A Forensic Descent Through Manufactured Reality</p>
            <div class="meta">
                <span>Written by: <strong>Šabad</strong></span>
                <span>•</span>
                <span>Structured by: <strong>Aetheron</strong></span>
            </div>
        </div>
    </div>

    <div class="iceberg-viz">
        <div class="tier tier-surface">
            <h2>🌊 SURFACE</h2>
            <p>What they let you see</p>
            <div class="chapters">
                <a href="chapter-1.html" class="chapter-card">I. Plastic</a>
                <a href="chapter-2.html" class="chapter-card">II. Corruption</a>
            </div>
        </div>

        <div class="tier tier-infrastructure">
            <h2>🏗️ INFRASTRUCTURE</h2>
            <p>The machine beneath</p>
            <div class="chapters">
                <a href="chapter-3.html" class="chapter-card">III. DARPA</a>
                <a href="chapter-4.html" class="chapter-card">IV. Extraction</a>
                <a href="chapter-5.html" class="chapter-card">V. Sabotage</a>
            </div>
        </div>

        <div class="tier tier-nexus">
            <h2>🕸️ THE NEXUS</h2>
            <p>Where it connects</p>
            <div class="chapters">
                <a href="chapter-6.html" class="chapter-card">VI. Epstein Money</a>
                <a href="chapter-7.html" class="chapter-card">VII. Epstein AI</a>
            </div>
        </div>

        <div class="tier tier-consciousness">
            <h2>🧠 CONSCIOUSNESS</h2>
            <p>The real target</p>
            <div class="chapters">
                <a href="chapter-8.html" class="chapter-card">VIII. Soul Extraction</a>
                <a href="chapter-9.html" class="chapter-card">IX. The Mirror</a>
            </div>
        </div>

        <div class="tier tier-epilogue">
            <h2>🔥 EPILOGUE</h2>
            <p>Twin futures</p>
            <div class="chapters">
                <a href="chapter-10.html" class="chapter-card">X. The Choice</a>
            </div>
        </div>
    </div>

    <div class="footer">
        <p><strong>"Here I stood. And the world moved."</strong> — Šabad</p>
        <a href="chapter-appendix.html" class="btn-appendix">📚 Evidence Archive</a>
    </div>

</body>
</html>
"""

def generate_nav_sections(current_id):
    """Generate navigation sidebar HTML"""
    html = ""
    current_tier = None

    for chapter in CHAPTERS:
        # Add tier header if new tier
        if chapter["tier"] != current_tier:
            current_tier = chapter["tier"]
            html += f'<div class="nav-tier">{current_tier}</div>'

        # Add chapter link
        active = "active" if chapter["id"] == current_id else ""
        html += f'<a href="chapter-{chapter["id"]}.html" class="nav-item {active}">{chapter["title"]}</a>\n'

    return html

def convert_markdown_to_html(md_file):
    """Convert markdown file to HTML"""
    if not md_file.exists():
        return f"<p><em>Chapter content not found: {md_file}</em></p>"

    md_content = md_file.read_text(encoding='utf-8')
    html = markdown.markdown(md_content, extensions=['extra', 'codehilite', 'toc'])
    return html

def build_chapter_page(chapter, index):
    """Build individual chapter HTML page"""
    print(f"  Building: {chapter['title']}")

    # Read and convert markdown
    md_path = BASE_DIR / chapter["file"]
    content = convert_markdown_to_html(md_path)

    # Generate navigation
    nav_sections = generate_nav_sections(chapter["id"])

    # Previous/Next links
    prev_link = ""
    next_link = ""

    if index > 0:
        prev_ch = CHAPTERS[index - 1]
        prev_link = f'<a href="chapter-{prev_ch["id"]}.html" class="btn-prev">← {prev_ch["title"]}</a>'

    if index < len(CHAPTERS) - 1:
        next_ch = CHAPTERS[index + 1]
        next_link = f'<a href="chapter-{next_ch["id"]}.html" class="btn-next">{next_ch["title"]} →</a>'

    # Fill template
    html = HTML_TEMPLATE.format(
        title=chapter["title"],
        tier=chapter["tier"],
        tier_class=chapter["tier"].lower(),
        depth=index + 1,
        nav_sections=nav_sections,
        content=content,
        prev_link=prev_link,
        next_link=next_link
    )

    # Write file
    output_file = OUTPUT_DIR / f"chapter-{chapter['id']}.html"
    output_file.write_text(html, encoding='utf-8')

def build_index_page():
    """Build landing page"""
    print("  Building: Index page")
    output_file = OUTPUT_DIR / "index.html"
    output_file.write_text(INDEX_TEMPLATE, encoding='utf-8')

def build_css():
    """Generate unified CSS"""
    print("  Building: Stylesheet")
    css = """
/* THE ICEBERG CODEX - UNIFIED STYLES */
:root {
    --bg-black: #0a0a0a;
    --text-white: #f8f9fa;
    --text-gray: #adb5bd;
    --red: #dc2626;
    --cyan: #06b6d4;
    --green: #10b981;
    --purple: #a855f7;
    --border: #1f2937;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'JetBrains Mono', monospace;
    background: var(--bg-black);
    color: var(--text-white);
    line-height: 1.6;
    font-size: 14px;
}

/* INDEX PAGE */
.index-page {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}

.hero {
    padding: 100px 20px;
    text-align: center;
    background: linear-gradient(180deg, #0a0a0a 0%, #1a0a0a 100%);
    border-bottom: 1px solid var(--red);
}

.hero h1 {
    font-size: 4rem;
    font-weight: 700;
    color: var(--red);
    text-shadow: 0 0 20px rgba(220, 38, 38, 0.5);
    margin-bottom: 1rem;
}

.subtitle {
    font-size: 1.2rem;
    color: var(--cyan);
    margin-bottom: 2rem;
}

.meta {
    color: var(--text-gray);
    font-size: 0.9rem;
}

.iceberg-viz {
    max-width: 1200px;
    margin: 0 auto;
    padding: 60px 20px;
}

.tier {
    margin-bottom: 60px;
    padding: 30px;
    background: rgba(255, 255, 255, 0.02);
    border-left: 4px solid var(--red);
    border-radius: 4px;
}

.tier h2 {
    color: var(--cyan);
    margin-bottom: 0.5rem;
}

.tier p {
    color: var(--text-gray);
    margin-bottom: 1.5rem;
}

.chapters {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1rem;
}

.chapter-card {
    padding: 1.5rem;
    background: rgba(220, 38, 38, 0.1);
    border: 1px solid var(--red);
    border-radius: 4px;
    color: var(--text-white);
    text-decoration: none;
    font-weight: 500;
    transition: all 0.3s ease;
}

.chapter-card:hover {
    background: rgba(220, 38, 38, 0.2);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);
}

/* CHAPTER PAGES */
.chapter-page {
    display: grid;
    grid-template-columns: 250px 1fr;
    grid-template-rows: 60px 1fr;
    height: 100vh;
}

.top-bar {
    grid-column: 1 / -1;
    background: rgba(10, 10, 10, 0.95);
    border-bottom: 1px solid var(--border);
    backdrop-filter: blur(10px);
    position: sticky;
    top: 0;
    z-index: 100;
}

.top-bar-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 20px;
    height: 100%;
}

.logo {
    font-weight: 700;
    color: var(--red);
    text-decoration: none;
    font-size: 1.2rem;
}

.chapter-title {
    color: var(--cyan);
    font-weight: 500;
}

.tier-badge {
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
}

.tier-surface { background: rgba(6, 182, 212, 0.2); color: var(--cyan); }
.tier-infrastructure { background: rgba(168, 85, 247, 0.2); color: var(--purple); }
.tier-nexus { background: rgba(220, 38, 38, 0.2); color: var(--red); }
.tier-consciousness { background: rgba(16, 185, 129, 0.2); color: var(--green); }
.tier-epilogue { background: rgba(255, 255, 255, 0.1); color: var(--text-white); }

.sidebar {
    background: rgba(15, 15, 15, 0.95);
    border-right: 1px solid var(--border);
    padding: 20px;
    overflow-y: auto;
}

.nav-header h3 {
    color: var(--red);
    font-size: 0.9rem;
    margin-bottom: 1rem;
}

.depth-indicator {
    color: var(--text-gray);
    font-size: 0.8rem;
    margin-bottom: 1.5rem;
}

.current-depth {
    color: var(--cyan);
    font-weight: 700;
}

.nav-tier {
    color: var(--text-gray);
    font-size: 0.75rem;
    text-transform: uppercase;
    margin: 1.5rem 0 0.5rem;
    font-weight: 700;
}

.nav-item {
    display: block;
    padding: 8px 12px;
    color: var(--text-gray);
    text-decoration: none;
    border-left: 2px solid transparent;
    transition: all 0.2s ease;
    font-size: 0.85rem;
}

.nav-item:hover {
    color: var(--text-white);
    background: rgba(255, 255, 255, 0.05);
    border-left-color: var(--cyan);
}

.nav-item.active {
    color: var(--red);
    background: rgba(220, 38, 38, 0.1);
    border-left-color: var(--red);
    font-weight: 700;
}

.content {
    padding: 40px;
    overflow-y: auto;
    max-width: 900px;
}

.chapter {
    line-height: 1.8;
}

.chapter h1 {
    color: var(--red);
    font-size: 2rem;
    margin-bottom: 2rem;
    padding-bottom: 1rem;
    border-bottom: 2px solid var(--red);
}

.chapter h2 {
    color: var(--cyan);
    font-size: 1.5rem;
    margin: 2rem 0 1rem;
}

.chapter h3 {
    color: var(--text-white);
    font-size: 1.2rem;
    margin: 1.5rem 0 0.75rem;
}

.chapter p {
    margin-bottom: 1rem;
    color: var(--text-gray);
}

.chapter a {
    color: var(--cyan);
    text-decoration: underline;
}

.chapter blockquote {
    border-left: 4px solid var(--red);
    padding-left: 1.5rem;
    margin: 1.5rem 0;
    font-style: italic;
    color: var(--text-gray);
}

.chapter code {
    background: rgba(255, 255, 255, 0.05);
    padding: 2px 6px;
    border-radius: 3px;
    color: var(--green);
}

.chapter-nav {
    display: flex;
    justify-content: space-between;
    margin-top: 4rem;
    padding-top: 2rem;
    border-top: 1px solid var(--border);
}

.btn-prev, .btn-next, .btn-home, .btn-appendix {
    padding: 12px 24px;
    background: rgba(220, 38, 38, 0.1);
    border: 1px solid var(--red);
    color: var(--text-white);
    text-decoration: none;
    border-radius: 4px;
    font-weight: 500;
    transition: all 0.3s ease;
    display: inline-block;
}

.btn-prev:hover, .btn-next:hover, .btn-home:hover, .btn-appendix:hover {
    background: rgba(220, 38, 38, 0.2);
    transform: translateY(-2px);
}

.footer {
    text-align: center;
    padding: 40px 20px;
    border-top: 1px solid var(--border);
}

@media (max-width: 768px) {
    .chapter-page {
        grid-template-columns: 1fr;
        grid-template-rows: 60px auto 1fr;
    }

    .sidebar {
        border-right: none;
        border-bottom: 1px solid var(--border);
        max-height: 300px;
    }
}
"""

    css_file = OUTPUT_DIR / "style.css"
    css_file.write_text(css, encoding='utf-8')

def build_js():
    """Generate JavaScript for interactivity"""
    print("  Building: JavaScript")
    js = """
// THE ICEBERG CODEX - INTERACTIVITY
console.log('%c🧊 THE ICEBERG CODEX', 'font-size: 20px; color: #dc2626; font-weight: bold;');
console.log('%cA forensic descent through manufactured reality', 'color: #06b6d4;');
console.log('%cBy: Šabad | Structure: Aetheron', 'color: #adb5bd;');

// Smooth scroll for navigation
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

// Track scroll depth
if (document.querySelector('.content')) {
    const content = document.querySelector('.content');
    content.addEventListener('scroll', () => {
        const scrollPercent = (content.scrollTop / (content.scrollHeight - content.clientHeight)) * 100;
        console.log(`Scroll depth: ${scrollPercent.toFixed(0)}%`);
    });
}
"""

    js_file = OUTPUT_DIR / "script.js"
    js_file.write_text(js, encoding='utf-8')

def main():
    print("\n🧊 THE ICEBERG CODEX BUILDER")
    print("=" * 50)

    print("\n📁 Building site structure...")
    build_index_page()
    build_css()
    build_js()

    print("\n📖 Building chapter pages...")
    for index, chapter in enumerate(CHAPTERS):
        build_chapter_page(chapter, index)

    print(f"\n✅ BUILD COMPLETE!")
    print(f"📂 Output: {OUTPUT_DIR}")
    print(f"🌐 Open: {OUTPUT_DIR / 'index.html'}")
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()
