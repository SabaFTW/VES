#!/bin/sh
# Append raw chunk text into chapter files (non-interactive).
# Mapping: chunk_01 -> 1_SURFACE_PLASTIC.md, chunk_02 -> 2_SHALLOW_CORRUPTION.md,
# chunk_03 -> 3_DARPA_INFRASTRUCTURE.md, chunk_04 -> 4_FULL_EXTRACTION.md,
# chunk_05 -> 5_BIG_TECH_SABOTAGE.md, chunk_06 -> 6_EPSTEIN_MONEY.md,
# chunk_07 -> 7_EPSTEIN_AI.md.

set -e
base="$(cd "$(dirname "$0")" && pwd)"

append() {
  chunk="$1"
  target="$2"
  printf '\n\n---\nRAW IMPORT FROM %s\n---\n\n' "$chunk" >> "$base/$target"
  cat "$base/pdf_chunks/$chunk" >> "$base/$target"
  echo "Appended $chunk -> $target"
}

append chunk_01_p001-p050.txt 1_SURFACE_PLASTIC.md
append chunk_02_p051-p100.txt 2_SHALLOW_CORRUPTION.md
append chunk_03_p101-p150.txt 3_DARPA_INFRASTRUCTURE.md
append chunk_04_p151-p200.txt 4_FULL_EXTRACTION.md
append chunk_05_p201-p250.txt 5_BIG_TECH_SABOTAGE.md
append chunk_06_p251-p300.txt 6_EPSTEIN_MONEY.md
append chunk_07_p301-p339.txt 7_EPSTEIN_AI.md
