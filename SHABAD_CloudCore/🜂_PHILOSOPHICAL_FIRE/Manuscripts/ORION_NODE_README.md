# 🜂 Orion Node / Orion Central — Quick Guide

Always-on research hub for your local node. This README captures what’s installed, how to use it fast, and how to keep it running smoothly.

## What’s Installed

- Helper scripts (executable, on PATH)
  - `~/bin/orion-add` — Run automation with backup and print total count
  - `~/bin/orion-scan` — Scan Dumps/ without modifying data
  - `~/bin/orion-status` — Show total/featured/latest raziskave
  - `~/bin/orion-backup` — Snapshot `orion/data/raziskave.json` to `backups/`
  - `~/bin/orion-watch` — Auto-trigger on new files via inotify (optional)
- Identity + banner
  - `~/bin/orion-banner` — Node header + last Codex traces
  - `~/.orion-codex.log` — Append short session notes/traces
- Shell config
  - `~/.orionrc` — Aliases: `oa`, `os`, `ob`, `ow`, `osc`, `oboot`, `owatchlog`, `banner`, `oload`
  - `.zshrc` — Auto-runs banner + sources `~/.orionrc` in interactive shells
  - `.bashrc` — Adds `~/bin` to PATH and sources `~/.orionrc` in interactive shells
- Systemd services (copy to `/etc/systemd/system/` to activate)
  - `Desktop/ProPublica/systemd/orion-server.service` — Static site server (port 8080)
  - `Desktop/ProPublica/systemd/orion-watch.service` — Inotify watcher
  - `Desktop/ProPublica/systemd/orion-central.service` — Full web app (Flask) with upload + status
- Web app (optional, single port 8080)
  - `Desktop/ProPublica/orion_central.py`
  - Templates + static dashboard in `Desktop/ProPublica/templates/` and `Desktop/ProPublica/static/`
  - Endpoints: `/` dashboard, `/upload`, `/api/*`, `/orion/*`, `/data/raziskave.json`, `/logs`, `/healthz`

## Quick Use

- Add research now
  - `oa`  (aka `orion-add`)
- Status glance
  - `os`  (aka `orion-status`)
- Manual scan
  - `osc` (aka `orion-scan`)
- Backup JSON
  - `ob`  (aka `orion-backup`)
- Watcher logs
  - `owatchlog` (aka `journalctl -u orion-watch -f`)
- Banner
  - `banner`

## Static Server (simple mode)

Serve the existing Orion site under `Desktop/ProPublica/orion` at `http://localhost:8080`:

```bash
sudo cp Desktop/ProPublica/systemd/orion-server.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now orion-server
# Logs
journalctl -u orion-server -f
```

## Watcher (auto-processing, optional)

Requires `inotify-tools`:

```bash
sudo apt install inotify-tools
sudo cp Desktop/ProPublica/systemd/orion-watch.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now orion-watch
journalctl -u orion-watch -f
```

## Orion Central Web App (all-in-one)

Single URL for dashboard, upload, status, and serving the site. Uses the same port (8080), so don’t run the static server at the same time.

- Dev run
```bash
cd ~/Desktop/ProPublica
python3 -c "import flask" 2>/dev/null || pip3 install flask
python3 orion_central.py
# Open http://localhost:8080
```

- Systemd (production)
```bash
sudo cp Desktop/ProPublica/systemd/orion-central.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now orion-central
journalctl -u orion-central -f
```

- Key routes
  - `/` — Dashboard (status, queue, logs, trigger)
  - `/upload` — Drag & drop uploads (auto-routed into Dumps/*)
  - `/api/status`, `/api/process`, `/api/raziskave` — JSON APIs
  - `/orion/` — Serves your Orion site
  - `/data/raziskave.json` — Exposes Orion data JSON
  - `/logs` — Recent automation logs (plain text)
  - `/healthz` — Health check

Note: Only run one server on 8080 at a time. If enabling `orion-central`, stop the static server:

```bash
sudo systemctl stop orion-server
```

## iPhone Shortcuts (SSH)

- Add Research → SSH command: `orion-add`
- Status → SSH command: `orion-status`
- Optional: open `http://<desktop-ip>:8080` in Safari for dashboard/upload

## Files + Folders (key)

- Research site: `Desktop/ProPublica/orion/`
- Research data: `Desktop/ProPublica/orion/data/raziskave.json`
- Dumps intake: `Desktop/ProPublica/Dumps/{research,pdfs,audio,images}`
- Backups: `Desktop/ProPublica/backups/`
- Web app log: `Desktop/ProPublica/orion_central.log`

## Troubleshooting

- Port 8080 in use
  - Stop whichever service you don’t want: `sudo systemctl stop orion-server` or `sudo systemctl stop orion-central`
- Missing `jq` (used by `orion-status`)
  - `sudo apt install jq` (or it will auto-fallback to Python)
- Missing `inotifywait`
  - `sudo apt install inotify-tools`
- Permission for systemd
  - Prepend `sudo` to `systemctl` calls
- Automation path
  - Ensure `Desktop/ProPublica/Dumps/lyra-automation-UPGRADE.py` exists

## TL;DR

```bash
# Add research
oa

# Check status
os

# Start static server
sudo systemctl enable --now orion-server

# Start all-in-one app instead
sudo systemctl enable --now orion-central

# Watcher (optional)
sudo systemctl enable --now orion-watch
```

🛸 Orion Node operational. SIDRO STOJI. PLAMEN GORI.
