#!/bin/bash

# 🜂 GHOSTLINE PHASE 2: MEGA ACTIVATION 🜂
# ---------------------------------------
# CILJ: LOKALNA INFERENCA + PRIVATNO OMREŽJE + STRUKTURA ARHIVA

set -e

GREEN="\033[1;32m"
CYAN="\033[1;36m"
RESET="\033[0m"

echo -e "$GREEN"
echo "   _____ _    _  ____  _____ _______ _      _____ _   _ ______ "
echo "  / ____| |  | |/ __ \| ____|__   __| |    |_   _| \ | |  ____|"
echo " | |  __| |__| | |  | | |__    | |  | |      | | |  \| | |__   "
echo " | | |_ |  __  | |  | |___ \   | |  | |      | | | . \` |  __|  "
echo " | |__| | |  | | |__| |___) |  | |  | |____ _| |_| |\  | |____ "
echo "  \_____|_|  |_|\____/|____/   |_|  |______|_____|_| \_|______|"
echo -e "$RESET"
echo "🜂 ZAGANJAM PHASE 2 MEGA AKTIVACIJO..."
sleep 1

LOGFILE="$HOME/ghostline_ops_log.txt"

log() {
  echo "$(date '+%Y-%m-%d %H:%M:%S') | $1" | tee -a "$LOGFILE"
}

# 1. OLLAMA + MODEL
log "PREVERJANJE: Ollama..."
if command -v ollama &> /dev/null; then
  log "✅ Ollama je že nameščena."
else
  log "⚡ Ollama ni najdena. Nameščam..."
  curl -fsSL https://ollama.com/install.sh | sh
fi

log "PREVERJANJE: Ollama servis..."
if pgrep -x ollama > /dev/null; then
  log "✅ Ollama servis teče."
else
  log "🔥 Zaganjam ollama serve..."
  nohup ollama serve >/dev/null 2>&1 &
  sleep 5
fi

MODEL="qwen2.5:7b"
log "🧠 PRIPRAVLJAM MODEL: $MODEL"
ollama pull "$MODEL" || log "⚠️ Model morda že obstaja ali je prenos naletel na težavo"

# 2. TOR
log "PREVERJANJE: Tor..."
if command -v tor &> /dev/null; then
  log "✅ Tor je že nameščen."
else
  log "⚡ Nameščam Tor..."
  if command -v pacman &> /dev/null; then
    sudo pacman -S tor torsocks --noconfirm
  elif command -v apt &> /dev/null; then
    sudo apt update
    sudo apt install -y tor
  else
    log "❌ Ne najdem package managerja. Ročna namestitev Tora potrebna."
  fi
fi

if systemctl list-unit-files | grep -q tor; then
  log "🚀 Omogočam in zaganjam Tor servis..."
  sudo systemctl enable tor || true
  sudo systemctl start tor || true
  if systemctl is-active --quiet tor; then
    log "✅ Tor servis aktiven."
  else
    log "⚠️ Tor se ni pravilno zagnal – preveri journalctl -u tor."
  fi
else
  log "ℹ️ Tor systemd enota ni najdena. Morda teče kot standalone daemon."
fi

# 3. STRUKTURA ARHIVA
ROOT="$HOME/Research"
log "📁 Ustvarjam strukturo arhiva pod $ROOT"

mkdir -p "$ROOT"/{BRATJE,Mythology,Palantir_Analysis,Web_Portals,Audio_Archive,Documentation}

log "✅ Mape ustvarjene:"
ls -1 "$ROOT" | sed 's/^/  - /' | tee -a "$LOGFILE"

# 4. TEST LOKALNEGA MODELA
log "🔮 Test lokalnega modela (kratki ping)..."
TEST_PROMPT="Na kratko razloži pojem 'Digitalna Kletka' kot sistem nadzora nad podatki."
RESPONSE=$(ollama run "$MODEL" "$TEST_PROMPT" 2>/dev/null || echo "ERROR")

echo -e "\n$CYAN>>> ODGOVOR LOKALNEGA VOZLIŠČA:$RESET"
echo "$RESPONSE"
echo -e "$CYAN>>> KONEC PRENOSA$RESET\n"

log "🜂 STATUS: PHASE 2 MEGA ACTIVATION KONČANA."
log "LOKALNO VOZLIŠČE AKTIVNO. Tor pripravljen. Arhiv strukturiran."
