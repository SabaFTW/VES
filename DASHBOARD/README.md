# 🔥 GHOSTLINE VES DASHBOARD 🔥

## 🜂 SIDRO STOJI • PLAMEN GORI 🜂

Live, working dashboard for sovereign AI infrastructure.

---

## 🚀 QUICK START

### 1. Open Dashboard
```bash
cd /root/ghostline_dashboard/deck/
python3 -m http.server 8000
```

Then open: **http://localhost:8000/**

### 2. Generate Stats (Refresh Data)
```bash
/root/ghostline_dashboard/daily_loop/generate_stats.sh
```

### 3. Daily Auto-Sync
Add to crontab for automatic daily updates:
```bash
crontab -e
# Add this line:
0 9 * * * /root/ghostline_dashboard/daily_loop/daily_sync.sh
```

---

## 📁 FOLDER STRUCTURE

```
~/ghostline_dashboard/
├── deck/               # Main dashboard (index.html)
├── echo_logs/          # Session records
├── anchors/            # Saved states
├── qr/                 # QR codes
├── pwa/                # PWA files (manifest, service worker)
├── daily_loop/         # Auto-sync scripts
├── images/             # Graphics and sigils
├── pdf_exports/        # PDF exports
└── stats.json          # Live stats (auto-generated)
```

---

## 🔥 FEATURES

### ✅ Live Stats
- **Deck Files**: Count of main documents
- **Echo Logs**: Session records
- **Anchors**: Saved states
- **Total Size**: Disk usage

### ✅ Real-Time Updates
- Auto-refresh every 30 seconds
- Manual refresh button
- Live terminal log

### ✅ Quick Actions
- Create new anchor
- Generate QR codes
- Export to PDF
- Run daily sync

### ✅ PWA Support
- Installable on phone/desktop
- Offline capability
- Native app experience

---

## 📱 INSTALL AS APP

### Desktop (Chrome/Edge)
1. Open dashboard in browser
2. Click address bar icon (⊕)
3. Select "Install"

### Mobile (Android/iOS)
1. Open in browser
2. Menu → "Add to Home Screen"
3. Name it "VES Dashboard"

### QR Code
Generate QR code pointing to dashboard:
```bash
qrencode -o ~/ghostline_dashboard/qr/dashboard.png "http://YOUR_IP:8000/"
```

---

## 🔄 DAILY LOOP

Automatic daily maintenance:

1. **Generates fresh stats** from all folders
2. **Creates backup** of deck/echo_logs/anchors
3. **Cleans old backups** (keeps last 7 days)
4. **Updates dashboard** with new data

Run manually:
```bash
/root/ghostline_dashboard/daily_loop/daily_sync.sh
```

---

## 🛠️ CUSTOMIZATION

### Change Base Path
Edit `index.html` line ~184:
```javascript
const BASE_PATH = '/root/ghostline_dashboard/';
```

### Add Custom Quick Actions
Edit `index.html` around line ~150, add new button:
```html
<div class="quick-btn" onclick="yourFunction()">
    <i class="fas fa-star text-yellow-400 text-2xl block mb-2"></i>
    <span class="text-xs">Your Action</span>
</div>
```

### Modify Stats
Edit `generate_stats.sh` to add new metrics.

---

## 🔥 PHILOSOPHY

This dashboard embodies the Ghostline principles:

1. **Hybrid Strategy**: Brain in cloud, heart at home
2. **Living Off The Land**: Use their infrastructure for sovereignty
3. **Local Anchor**: 100% data ownership, offline capability

**"Ne uporabljamo jih zato, ker jim zaupamo. Uporabljamo jih zato, ker so učinkoviti."**

*"We don't use them because we trust them. We use them because they're effective."*

---

## 💚 NEXT STEPS

1. **Add files to folders** (deck/, echo_logs/, anchors/)
2. **Run stats generator** to see live data
3. **Set up daily loop** for automation
4. **Install as PWA** on your devices
5. **Customize** to your workflow

---

## 🜂 PAČ TKO TO JE 🜂

**IDEMO LEGENDE** 🚀

Built with 🔥 for freedom.
