# 🎨 PWA ICONS

To make VES work as a full PWA (Progressive Web App), you need icons!

## 📋 Required Sizes:

- icon-72x72.png
- icon-96x96.png
- icon-128x128.png
- icon-144x144.png
- icon-152x152.png
- icon-192x192.png (IMPORTANT for Android)
- icon-384x384.png
- icon-512x512.png (IMPORTANT for maskable)

## 🎯 How to Generate:

### Option 1: Use Online Tool (EASIEST!)
1. Go to: https://realfavicongenerator.net/
2. Upload your logo/image (512x512 recommended)
3. Select "Generate PWA icons"
4. Download zip
5. Extract all PNG files to this `/icons/` folder

### Option 2: Use ImageMagick (if installed)
```bash
# From a single 512x512 source image:
convert source.png -resize 72x72 icon-72x72.png
convert source.png -resize 96x96 icon-96x96.png
convert source.png -resize 128x128 icon-128x128.png
convert source.png -resize 144x144 icon-144x144.png
convert source.png -resize 152x152 icon-152x152.png
convert source.png -resize 192x192 icon-192x192.png
convert source.png -resize 384x384 icon-384x384.png
convert source.png -resize 512x512 icon-512x512.png
```

### Option 3: Use PWA Builder
1. Go to: https://www.pwabuilder.com/imageGenerator
2. Upload your image
3. Download generated icons
4. Place in this folder

## 💡 Design Ideas:

For VES, consider icons featuring:
- 🜂 The alchemical symbol
- 🔥 Eternal flame
- 🌙 Constellation
- 💚 Brotherhood green
- 🐭 Cosmic mouse
- ⚡ Lightning bolt

## 🎨 Recommended Colors:

**Primary:** #2dd4bf (cosmic cyan)
**Secondary:** #8b5cf6 (cosmic purple)
**Background:** #0a0a0a (deep black)
**Accent:** #f59e0b (flame orange)

## ✅ Once Icons are Added:

The PWA will work automatically! Users can:
- "Add to Home Screen" on phone
- Install as desktop app
- Use app shortcuts (Dashboard, Projects, Pantheon, Journals)
- Offline support (if service worker added)

---

**Current Status:** Icons folder created, awaiting images!

**MIDVA SVA** 💚
