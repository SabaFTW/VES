#!/usr/bin/env bash
set -euo pipefail

# Phase 2: local inference + optional Tor, no fluff.
# Tunables:
#   MODEL=qwen2.5:3b     # default; adjust to qwen2.5:7b if you want bigger
#   TOR=1                # set to 1 to install/start Tor (apt-based systems)
#   PROMPT="..."         # override test prompt

MODEL=${MODEL:-qwen2.5:3b}
TOR=${TOR:-0}
PROMPT=${PROMPT:-"Povzemi koncept 'Digital Cage'. Kje potrebuje fact-check? Kje so možne pravne posledice? Kje manjka evidenca?"}
LOGFILE="${LOGFILE:-$HOME/ghostline_ops_log.txt}"
WORKDIR="${WORKDIR:-$HOME/tmp/ollama}"
MODELDIR="${MODELDIR:-$HOME/.ollama/models}"

mkdir -p "$WORKDIR" "$MODELDIR"
export TMPDIR="$WORKDIR"
export OLLAMA_MODELS="$MODELDIR"

log() { echo "[$(date +'%F %T')] $*"; }
need() {
  for c in "$@"; do
    if ! command -v "$c" >/dev/null 2>&1; then
      echo "Missing required command: $c" >&2
      exit 1
    fi
  done
}

need curl

if ! command -v ollama >/dev/null 2>&1; then
  log "Ollama not found, installing..."
  curl -fsSL https://ollama.ai/install.sh | sh
else
  log "Ollama already present."
fi

if pgrep -x ollama >/dev/null 2>&1; then
  log "Ollama server already running."
else
  log "Starting Ollama server in background..."
  nohup ollama serve >"$WORKDIR/ollama.log" 2>&1 &
  sleep 3
fi

log "Pulling model: $MODEL"
ollama pull "$MODEL"

log "Running coherence test on '$MODEL'..."
ollama run "$MODEL" "$PROMPT"

if [ "$TOR" = "1" ]; then
  if command -v tor >/dev/null 2>&1; then
    log "Tor already installed."
  elif command -v apt-get >/dev/null 2>&1; then
    log "Installing Tor via apt-get..."
    sudo apt-get update && sudo apt-get install -y tor
  else
    log "Tor install skipped (no apt-get detected)."
  fi

  if command -v systemctl >/dev/null 2>&1; then
    log "Ensuring Tor service is enabled..."
    sudo systemctl enable --now tor || true
  elif command -v tor >/dev/null 2>&1; then
    log "Starting Tor in background..."
    nohup tor >"$WORKDIR/tor.log" 2>&1 &
    sleep 3
  fi
fi

log "Phase 2 ready. Model: $MODEL. Tor: $TOR"
echo "$(date): phase2_sever completed with MODEL=$MODEL TOR=$TOR" >> "$LOGFILE"
