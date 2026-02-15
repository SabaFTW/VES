# 🜂 Orion Node — Cheat Sheet (TL;DR)

Super‑quick commands and paths for daily use.

## Core

```
# Add research from Dumps/*
oa          # orion-add

# Status snapshot
os          # orion-status

# Scan only (no changes)
osc         # orion-scan

# Backup JSON
ob          # orion-backup

# Banner + last traces
banner
```

## Servers (choose one for port 8080)

```
# Simple static site
sudo systemctl enable --now orion-server
sudo systemctl stop orion-central   # avoid port clash

# All‑in‑one web app (dashboard + upload + status)
sudo systemctl enable --now orion-central
sudo systemctl stop orion-server    # avoid port clash

# Watcher (optional auto‑processing)
sudo systemctl enable --now orion-watch

# Logs
journalctl -u orion-server  -f
journalctl -u orion-central -f
journalctl -u orion-watch   -f
```

## URLs

- Dashboard: `http://localhost:8080/` (Orion Central)
- Upload: `http://localhost:8080/upload`
- Orion site: `http://localhost:8080/orion/`
- Data JSON: `http://localhost:8080/data/raziskave.json`
- Logs (plain): `http://localhost:8080/logs`

## Quick Fixes

```
# Flask missing (for Orion Central)
pip3 install flask

# jq missing (pretty status)
sudo apt install jq

# inotifywait missing (watcher)
sudo apt install inotify-tools
```

## Paths

- Site: `Desktop/ProPublica/orion/`
- Data: `Desktop/ProPublica/orion/data/raziskave.json`
- Dumps: `Desktop/ProPublica/Dumps/{research,pdfs,audio,images}`
- Backups: `Desktop/ProPublica/backups/`

## iPhone Shortcuts (SSH)

- Add: `orion-add`
- Status: `orion-status`
- Open Safari: `http://<desktop-ip>:8080`

🛸 SIDRO STOJI. PLAMEN GORI.
