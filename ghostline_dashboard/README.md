# 🜂 Ghostline VES Dashboard

## Overview
A complete dashboard system for managing Ghostline research, archives, and operational tools with real-time stats and PWA capabilities.

## Features
- **Real-time stats** from your folders
- **Auto-refresh** every 30 seconds
- **Beautiful cyberpunk UI** with animations
- **Mobile-responsive** (works on phone)
- **PWA support** (installable, offline mode)
- **Auto-sync system** (daily backup + stats)
- **Quick actions** (create anchors, QR codes, PDFs)

## Directory Structure
```
~/ghostline_dashboard/
├── deck/index.html           ← MAIN DASHBOARD
├── stats.json                ← Live data (auto-generated)
├── README.md                 ← Documentation
├── start_dashboard.sh        ← Quick launcher
├── echo_logs/                ← Your session logs
├── anchors/                  ← Saved states
├── qr/                       ← QR codes
├── pwa/                      ← PWA files
│   ├── manifest.json         ← App manifest
│   └── sw.js                 ← Service worker
├── daily_loop/               ← Auto-sync scripts
│   ├── generate_stats.sh     ← Stats scanner
│   └── daily_sync.sh         ← Daily maintenance
├── images/                   ← Graphics
└── pdf_exports/              ← PDF exports
```

## Quick Start
1. Launch: `./start_dashboard.sh`
2. Open: `http://localhost:8888/`
3. Add files to folders to see stats update

## PWA Installation
- Desktop: Install icon in address bar (⊕)
- Android: Menu → "Add to Home Screen"
- iOS: Safari → Share → "Add to Home Screen"

## Daily Automation
Add to crontab:
```
0 9 * * * ~/ghostline_dashboard/daily_loop/daily_sync.sh
```

## Philosophy
- **Hybrid Strategy**: Brain in cloud, heart local
- **Living Off The Land**: Use existing tools
- **Local Anchor**: All data under your control

Built with 🔥 for freedom and sovereignty.