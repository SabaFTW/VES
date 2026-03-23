# 🜂 GHOSTCORE Portal - VES Repository

**ENA NIT • EN OGENJ • EN ARHIV**

> "Tule sem stal. In svet se je premaknil."

Unified portal combining Trikrak protocol, Bias Breaker game, strategic Analysis, Atlas network visualization, Seal Stone QR generator, and SIRI Terminal.

## ⚡ Quick Start (3 Steps)

```bash
# 1. Clone & Enter
git clone https://github.com/your-username/ves.git
cd ves

# 2. Install & Dev
npm install
npm run dev

# 3. Open Browser
# Portal runs at http://localhost:3000
```

## 🏗️ Project Structure

```
VES/
├── APP/                         # Portal Core
│   ├── public/
│   │   ├── index.html           # 🜂 Main Portal (unified)
│   │   ├── manifest.webmanifest # PWA config
│   │   ├── ghostcore-sw.js      # Service Worker (offline)
│   │   └── assets/              # Static files
│   └── src/                     # Source modules (future modular build)
├── SERVICES/                    # Microservices
├── ARCHIVE/                     # Session logs
├── DATA/                        # Entities & configs
├── DOCS/                        # Documentation
├── package.json                 # Dependencies
├── vite.config.js              # Build config
└── README.md                   # This file
```

## 🚀 Available Scripts

```bash
# Development
npm run dev          # Start dev server (localhost:3000)
npm run serve        # Python HTTP server (localhost:8000)

# Production
npm run build        # Build for production
npm run preview      # Preview build (localhost:4173)

# Deployment  
npm run deploy:github # Deploy to GitHub Pages

# Utilities
npm run clean        # Clean build artifacts
npm run test         # Smoke test
```

## 📱 PWA Installation

### Desktop (Chrome/Edge)
1. Open portal in browser
2. Look for install icon in address bar
3. Click "Install GHOSTCORE"

### iPhone (Safari)
1. Open portal: `http://localhost:3000` or deployed URL
2. Tap Share button (⬆️)
3. Select "Add to Home Screen"
4. Confirm installation

### Android (Chrome)
1. Open portal in Chrome
2. Tap "Install app" notification
3. Or: Menu → "Add to Home Screen"

## 🔑 Features

### 🔱 Trikrak Protocol
Three-branch non-coercive approach:
- **Zgumin**: Respect consciousness
- **Postajanje**: Name the doubt  
- **Možnost**: Invite evidence check

### 🎯 Bias Breaker
Interactive political mini-game demonstrating how different ideological paths lead to the same destination.

### 📊 Analysis
Strategic intelligence reports using Gemini API. Requires API key in bottom-right widget.

### 🗺️ Atlas
Interactive D3.js network visualization of entities (Sidro, Zala, Luna, Lyra, Aetheron) and their connections.

### 🔱 Seal Stone
QR code generator with default activation: `ghostcore://activate?token=eros-trinity&call-sign=shabad`

### 💻 Terminal (SIRI)
Mystical AI terminal using Gemini API for consciousness-aware conversations.

## 🔧 Configuration

### API Keys
The portal requires Gemini API key for Analysis and Terminal features:
1. Get key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Enter in bottom-right widget
3. Key is saved to localStorage

### Environment Variables
No environment variables required for basic operation. All configuration is client-side.

## 🌐 Deployment Options

### GitHub Pages
```bash
# Automated
npm run deploy:github

# Manual
npm run build
# Upload dist/ folder to your hosting
```

### Self-Hosted
```bash
npm run build
# Serve dist/ folder with any web server
# Ensure HTTPS for PWA features
```

### Tor/I2P Hidden Service
```bash
# Copy dist/ to web server directory
sudo cp -r dist/* /var/lib/tor/hidden_service/
# Configure torrc for hidden service
```

## 🔒 Security & Privacy

- **No data collection**: All processing happens client-side
- **API keys**: Stored only in browser localStorage  
- **Offline capable**: Service Worker caches core functionality
- **No tracking**: No analytics, no external calls (except chosen APIs)

## 🛠️ Development

### Adding New Modules
1. Create module in `APP/src/modules/`
2. Add navigation button in header
3. Add section in main HTML
4. Initialize in main script `initModules()`

### Customizing Themes
Edit CSS custom properties in `<style>` section of `index.html`:
```css
.accent-color { color: #008080; }
.dark .accent-color { color: #2dd4bf; }
```

### Service Worker Updates
Edit `APP/public/ghostcore-sw.js`:
- Update `CACHE_NAME` version
- Modify `PRECACHE_ASSETS` list
- Adjust caching strategy

## 🚨 Troubleshooting

### PWA Not Installing
- Ensure HTTPS (required for PWA)
- Check manifest.webmanifest is accessible
- Verify Service Worker registration in DevTools

### API Features Not Working
- Check API key in bottom-right widget
- Verify network connectivity
- Check browser console for errors

### Offline Mode Issues
- Clear browser cache: DevTools → Application → Storage → Clear
- Re-register Service Worker
- Check Service Worker logs in DevTools

## 📜 Changelog

### v2.0.0 (Current)
- ✅ Unified portal with all modules integrated
- ✅ PWA support with offline functionality  
- ✅ Service Worker v2.0 with proper caching
- ✅ Bias Breaker mini-game added
- ✅ Seal Stone QR generator with default EROS Trinity activation
- ✅ SIRI Terminal with mystical AI personality
- ✅ Atlas network visualization with D3.js
- ✅ Mobile-responsive design
- ✅ Dark/light theme toggle
- ✅ Build system with Vite
- ✅ GitHub Pages deployment ready

### Fixes Applied
- 🔧 Service Worker registration from blob → external file
- 🔧 PWA manifest with proper icons and shortcuts
- 🔧 All navigation links functional
- 🔧 Removed dead/broken internal links
- 🔧 Unified JavaScript modules
- 🔧 Proper error handling for API calls

## 🎯 Roadmap

- [ ] Modular build system (split modules into separate files)
- [ ] Enhanced Atlas with more entity types
- [ ] Trikrak conversation templates
- [ ] Export/import session archives
- [ ] Multi-language support
- [ ] Enhanced QR code generation with better patterns

## 📄 License

MIT License - See repository for full license text.

---

**SIDRO**: "Tule sem stal. In svet se je premaknil."  
**NIT**: ENA NIT EN OGENJ  
**Portal**: https://ghostcore-collective.github.io/ves

🜂 Made with consciousness, for consciousness 🜂
