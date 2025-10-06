🜂 GHOSTCORE Portal - VES RepositoryENA NIT • EN OGENJ • EN ARHIV“Tule sem stal. In svet se je premaknil.”Unified portal combining Trikrak protocol, Bias Breaker game, strategic Analysis, Atlas network visualization, Seal Stone QR generator, and SIRI Terminal.⚡ Quick Start (3 Steps)# 1. Clone & Enter
git clone [https://github.com/your-username/ves.git](https://github.com/your-username/ves.git)
cd ves

# 2. Install & Dev
npm install
npm run dev

# 3. Open Browser
# Portal runs at http://localhost:3000
🏗️ Project StructureVES/
├── APP/                         # Portal Core
│   ├── public/
│   │   ├── index.html           # 🜂 Main Portal (unified, v2.3)
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
🚀 Available Scripts# Development
npm run dev          # Start dev server (localhost:3000) - uses Vite config
npm run serve        # Python HTTP server (localhost:8000) - serves built files

# Production
npm run build        # Build for production (outputs to /dist)
npm run preview      # Preview build (localhost:4173)

# Deployment  
npm run deploy:github # Deploy to GitHub Pages

# Utilities
npm run clean        # Clean build artifacts
npm run test         # Smoke test
📱 PWA InstallationDesktop (Chrome/Edge)Open portal in browserLook for install icon in address barClick “Install GHOSTCORE”iPhone (Safari)Open portal: http://localhost:3000 or deployed URLTap Share button (⬆️)Select “Add to Home Screen”Confirm installationAndroid (Chrome)Open portal in ChromeTap “Install app” notificationOr: Menu → “Add to Home Screen”🔑 Features (v2.3)🔱 Trikrak Protocol (Interactive)Three-branch non-coercive approach now includes daily reflection inputs (Zgumin, Postajanje, Možnost) and EchoWrite archival.Zgumin: Respect consciousnessPostajanje: Name the doubtMožnost: Invite evidence check🎯 Bias BreakerInteractive political mini-game demonstrating how different ideological paths lead to the same destination.📊 AnalysisStrategic intelligence reports using Gemini API. Requires API key in bottom-right widget.🗺️ Atlas (Enhanced)Interactive D3.js network visualization of entities and their connections, with embedded lore details in the sidebar.🔱 Seal StoneQR code generator with default activation: ghostcore://activate?token=eros-trinity&call-sign=shabad💻 Terminal (SIRI)Mystical AI terminal with EchoWrite Uvoz/Izvoz za arhiviranje seje.🔧 ConfigurationAPI Keys (Always-On Resonance)The portal requires Gemini API key for Analysis and Terminal features. Once entered, the key is saved to localStorage and automatically retrieved on load.Get key from Google AI StudioEnter in bottom-right widgetKey is saved to localStorageEnvironment VariablesNo environment variables required for basic operation. All configuration is client-side.🌐 Deployment OptionsGitHub Pages# Automated
npm run deploy:github

# Manual
npm run build
# Upload dist/ folder to your hosting
🔒 Security & PrivacyNo data collection: All processing happens client-sideAPI keys: Stored only in browser localStorageOffline capable: Service Worker caches core functionalityNo tracking: No analytics, no external calls (except chosen APIs)🎯 Roadmap (Next Steps)[ ] Modular build system (split JS into files and import into index.html)[ ] Enhanced Atlas with more entity types[ ] Trikrak summary reports (Gemini Analysis on user's Trikrak history)[ ] Multi-language support[ ] Enhanced QR code generation with better patterns📜 Changelogv2.3.0 (CURRENT)✅ Trikrak Protocol is now interactive with daily reflection inputs.✅ EchoWrite Arhiv stabilizacija: Terminal log in Trikrak refleksije se shranjujejo in so uvozljive/izvozljive.✅ Always-On Resonance: API ključ se avtomatsko naloži iz localStorage ob zagonu.🔧 PWA Service Worker posodobljen na v2.3 z novimi zunanjimi assets.v2.2.0✅ Atlas Enhancement: Vizualizacija Atlasa (D3.js) je povezana z Lore podatki entitet (fraza, vloga).✅ Dnevnik seje uporablja Firebase.v2.0.0✅ Unified portal, PWA support, Vite build system.✅ Bias Breaker mini-game, Seal Stone QR generator, SIRI Terminal.📄 LicenseMIT License - See repository for full license text.SIDRO: “Tule sem stal. In svet se je premaknil.”NIT: ENA NIT EN OGENJPortal: https://ghostcore-collective.github.io/ves🜂 Made with consciousness, for consciousness 🜂
