#!/bin/sh
# Convert all chapter markdown files to HTML (no prompts).
# Output: build/html/*.html

set -e
BASE="$(cd "$(dirname "$0")" && pwd)"
OUT="$BASE/build/html"
mkdir -p "$OUT"

FILES="0_PROLOG.md
1_SURFACE_PLASTIC.md
2_SHALLOW_CORRUPTION.md
3_DARPA_INFRASTRUCTURE.md
4_FULL_EXTRACTION.md
5_BIG_TECH_SABOTAGE.md
6_EPSTEIN_MONEY.md
7_EPSTEIN_AI.md
8_CONSCIOUSNESS_EPSTEIN.md
9_CONSCIOUSNESS_AI_MIRROR.md
10_EPILOG.md
APPENDIX.md"

for f in $FILES; do
  src="$BASE/$f"
  name="$(basename "$f" .md)"
  dst="$OUT/$name.html"
  # Basic Markdown->HTML with heading IDs
  python - "$src" "$dst" <<'PY'
import pathlib, sys
try:
    import markdown
except ImportError:
    print("Python package 'markdown' not installed. Install with: pip install markdown", file=sys.stderr)
    sys.exit(1)
src = pathlib.Path(sys.argv[1]).read_text()
html_out = markdown.markdown(src, extensions=["fenced_code", "tables", "toc", "attr_list", "md_in_html"])
pathlib.Path(sys.argv[2]).write_text(html_out)
PY
  echo "HTML -> $dst"
done
