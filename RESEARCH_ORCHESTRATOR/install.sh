#!/usr/bin/env bash
set -e

echo "[+] Constellation Research – install.sh 2.0"

# 1) Check Python
if ! command -v python3 &> /dev/null; then
  echo "[!] python3 not found. Please install Python 3.9+."
  exit 1
fi

# 2) Check pip
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
  echo "[!] pip not found. Please install pip (python3-pip)."
  exit 1
fi

PIP_CMD="pip"
if command -v pip3 &> /dev/null; then
  PIP_CMD="pip3"
fi

# 3) Install ripgrep
if ! command -v rg &> /dev/null; then
  echo "[+] ripgrep not found. Attempting to install..."
  if command -v apt &> /dev/null; then
    sudo apt update && sudo apt install -y ripgrep
  elif command -v pacman &> /dev/null; then
    sudo pacman -Sy --noconfirm ripgrep
  elif command -v dnf &> /dev/null; then
    sudo dnf install -y ripgrep
  else
    echo "[!] Unknown package manager. Please install ripgrep manually."
  fi
else
  echo "[✓] ripgrep already installed."
fi

# 4) Python deps
echo "[+] Installing Python dependencies from requirements.txt..."
$PIP_CMD install -r requirements.txt

# 5) Create output + index dirs
mkdir -p research_outputs
mkdir -p rag_index

# 6) Ollama check (optional)
if ! command -v ollama &> /dev/null; then
  echo "[!] Ollama not detected."
  echo "    If you plan to use a local LLM via Ollama, install it from: https://ollama.ai"
else
  echo "[✓] Ollama detected. Remember to: ollama pull llama3"
fi

echo "[✓] Installation complete."