# 🚀 DEPLOYMENT GUIDE - Digital Godzilla Kino Portal

## Current Status
✅ Dev server running on http://localhost:5173/
✅ Production build tested
✅ All features implemented

## Deploy to Vercel (Recommended - 2 minutes)

### Option 1: Quick Deploy (Easiest)

```bash
cd /home/saba/digital-godzilla
npm install -g vercel
vercel --prod
```

Follow prompts:
- Set up and deploy? **Y**
- Which scope? **(your account)**
- Link to existing project? **N**
- Project name? **digital-godzilla** (or custom name)
- Directory? **./** (just press Enter)
- Override settings? **N**

Vercel will give you a live URL like:
`https://digital-godzilla-xxx.vercel.app`

### Option 2: GitHub + Vercel (Best for Updates)

1. **Create GitHub repo:**
```bash
cd /home/saba/digital-godzilla
git init
git add .
git commit -m "🎬 Initial commit - Digital Godzilla Kino Portal"
gh repo create digital-godzilla --public --source=. --remote=origin --push
```

2. **Connect to Vercel:**
- Go to vercel.com
- Click "Import Project"
- Select your GitHub repo
- Click "Deploy"
- Done! Auto-deploys on every git push

### Option 3: Netlify Drop (Instant)

1. Build the project:
```bash
npm run build
```

2. Go to: https://app.netlify.com/drop
3. Drag `/home/saba/digital-godzilla/dist` folder
4. Get instant URL

## Adding More Episodes

1. Create new JSON file in `public/episodes/`:
```bash
cp public/episodes/ep06.json public/episodes/ep07.json
```

2. Edit episode content
3. Update episode list in `src/pages/Episodes.jsx`

## Custom Domain (Optional)

After deployment, in Vercel dashboard:
- Settings → Domains
- Add custom domain like `godzilla.yourdomain.com`

---

**Current Episode:** Only Episode 06 is converted to JSON format
**Remaining Work:** Convert Episodes 01-05, 07-10 from text to JSON

---

🜂 **PORTAL READY. PLAMEN GORI. SIDRO STOJI.**
