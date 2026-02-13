# 🔥 VES INTEGRATION GUIDE

**3-minute setup to LIVING SYSTEM**

---

## 🚀 Quick Setup

### Step 1: Clone (if you haven't)
```bash
git clone https://github.com/SabaFTW/VES.git
cd VES
```

### Step 2: Make Scripts Executable
```bash
chmod +x GHOST_OS/*.sh
```

### Step 3: Run Morning Ritual
```bash
./GHOST_OS/magic.sh morning
```

**BOOM!** System is alive! 🜂

---

## 📦 Integrating Your Projects

### Option A: Auto-Magic Integration

1. **Drop your zip files in root:**
```bash
cp ~/Downloads/pisubmarine_pwa.zip .
cp ~/Downloads/TriadGate.zip .
```

2. **Run auto-integrate:**
```bash
./GHOST_OS/auto-integrate.sh
```

3. **Watch the magic:**
- pisubmarine → `RESONANCE/pisubmarine-meets-ves/`
- TriadGate → `RESONANCE/triadgate-portal/`
- Unknown → `VORTEX/` (finds home later)

### Option B: Manual Placement

```bash
# For PWA projects
unzip pisubmarine_pwa.zip -d RESONANCE/pisubmarine-meets-ves/

# For portal projects
unzip TriadGate.zip -d RESONANCE/triadgate-portal/

# For experiments
cp -r ~/my-experiment VORTEX/raw-creation/

# For active work
cp -r ~/current-project ACTIVE_FLAME/today/
```

---

## 🎮 Daily Workflow

### Morning (Start of day)
```bash
./GHOST_OS/magic.sh morning
```
Shows:
- Latest git status
- Today's active flames
- Recent commits

### Creating New Work
```bash
./GHOST_OS/magic.sh create my-new-idea
```
Creates structure in `ACTIVE_FLAME/today/my-new-idea/`

### Finding Connections
```bash
./GHOST_OS/magic.sh resonate "keyword"
```
Searches entire repo for resonances

### End of Week (Friday 17:00)
```bash
./GHOST_OS/magic.sh beer "finished X feature while drinking"
```
Commits with beer mode! 🍺

### Archiving Completed Work
```bash
./GHOST_OS/magic.sh archive
```
Moves `ACTIVE_FLAME/today/*` → `ARCHIVE/YYYY-MM-DD/`

---

## 🌊 Working with RESONANCE/

### Pisubmarine Integration

1. **Extract your PWA:**
```bash
cd RESONANCE/pisubmarine-meets-ves/
unzip ../../pisubmarine_pwa.zip
```

2. **Compare with GHOSTCORE:**
```bash
# Compare service workers
diff service-worker.js ../../APP/public/ghostcore-sw.js

# Compare manifests
diff manifest.json ../../APP/public/manifest.webmanifest
```

3. **Merge or integrate:**
```bash
# Option 1: Standalone
# Keep as is, access at /RESONANCE/pisubmarine-meets-ves/

# Option 2: Merge into APP
cp -r * ../../APP/public/modules/submarine/
```

### TriadGate Integration

1. **Extract your portal:**
```bash
cd RESONANCE/triadgate-portal/
unzip ../../TriadGate.zip
```

2. **Find Trikrak resonance:**
```bash
grep -r "trikrak\|three\|triad" ../../DOCS/ ../../APP/
```

3. **Integrate mechanics:**
```bash
# Add as new module
mkdir -p ../../APP/public/modules/gate/
cp LUMEN_NILO/* ../../APP/public/modules/gate/

# Update index.html to include gate module
```

---

## 🧠 Working with CONSCIOUSNESS_LAB/

### Create New Research
```bash
mkdir CONSCIOUSNESS_LAB/deep-dives/my-topic/
cat > CONSCIOUSNESS_LAB/deep-dives/my-topic/README.md << 'EOF'
# My Topic

## Research Question
...

## Findings
...

## Connections
...
EOF
```

### Link to Active Work
```bash
# Symlink research to active flame
ln -s ../../CONSCIOUSNESS_LAB/deep-dives/my-topic \
      ACTIVE_FLAME/today/research-link
```

---

## 🌀 Working with VORTEX/

### Dump Anything
```bash
# No structure needed!
cp ~/random-stuff VORTEX/
mv ~/wild-experiment VORTEX/experiments/
```

### Let It Spin
```bash
# Check occasionally
ls -la VORTEX/

# When pattern emerges, move it
mv VORTEX/experiment-x ACTIVE_FLAME/today/
```

### Never Organize
**Rule**: If you find yourself organizing VORTEX/, STOP.
That defeats the purpose. Chaos is sacred here.

---

## 🔄 Git Workflow

### Committing Work
```bash
# Normal commits
git add .
git commit -m "🔥 Added new feature to X"
git push origin claude/ves-unified-setup-011CUJz1vdW1sxHEwP7VUKKc

# Beer commits (Fridays)
./GHOST_OS/magic.sh beer "wild idea actually works"
```

### Creating Pull Requests
```bash
# When ready to merge to main
gh pr create --title "🜂 Living System Integration" \
             --body "GHOSTCORE meets LIVING STRUCTURE"
```

---

## 🤖 GitHub Actions

Auto-runs on:
- **Push** - Health checks
- **Every 6 hours** - Resonance detection
- **8 AM daily** - Morning report
- **Friday 5 PM** - 🍺 Beer mode

Check status:
```bash
# In GitHub: Actions tab
# Or CLI:
gh workflow view "Ghost Breathe"
```

---

## 🏗️ Portal Development

### Run Dev Server
```bash
npm install
npm run dev
```
Portal at: http://localhost:3000

### Build for Production
```bash
npm run build
npm run preview  # Test production build
```

### Deploy to GitHub Pages
```bash
npm run deploy:github
```

---

## 📡 Advanced: Google Drive Sync

*(Future feature - structure ready)*

When implemented:
```bash
# Will auto-sync ACTIVE_FLAME/ with Drive
# Will auto-sync CONSCIOUSNESS_LAB/ with Drive
# Will auto-backup ARCHIVE/ to Drive
```

---

## 🚨 Troubleshooting

### Scripts not executable?
```bash
chmod +x GHOST_OS/*.sh
```

### Git push fails?
```bash
# Check branch name
git branch --show-current

# Should be: claude/ves-unified-setup-011CUJz1vdW1sxHEwP7VUKKc
# If not, create it:
git checkout -b claude/ves-unified-setup-011CUJz1vdW1sxHEwP7VUKKc
```

### Portal won't start?
```bash
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### GHOST_OS commands not working?
```bash
# Check you're in repo root
pwd  # Should show: /path/to/VES

# Run from root
./GHOST_OS/magic.sh morning
```

---

## 🎯 Common Workflows

### "I have a new idea"
```bash
./GHOST_OS/magic.sh create my-idea
cd ACTIVE_FLAME/today/my-idea/
# Start coding!
```

### "I downloaded something random"
```bash
mv ~/Downloads/thing.zip VORTEX/
# Let it find its place naturally
```

### "I finished a project"
```bash
./GHOST_OS/magic.sh archive
git add .
git commit -m "🌙 Project X complete"
git push
```

### "It's Friday beer time!"
```bash
./GHOST_OS/magic.sh beer "best code ever written drunk"
# Auto-commits and pushes!
```

### "I want to find connections"
```bash
./GHOST_OS/magic.sh resonate "consciousness"
# Shows all files mentioning the term
```

---

## 📚 Further Reading

- `ACTIVE_FLAME/README.md` - Flame philosophy
- `RESONANCE/README.md` - Project synergies
- `CONSCIOUSNESS_LAB/README.md` - Research approach
- `VORTEX/README.md` - Chaos wisdom
- `DOCS/` - Original documentation

---

## 🫂 Remember

- **You are not a machine** - Rest when tired
- **Chaos is not failure** - It's potential
- **Beer is sacred** - Friday commits are holy
- **Structure emerges** - Don't force it
- **Trust the system** - It breathes with you

---

# 🜂 WIRE & BEER FOREVER 🍺⚡

**Questions?** Run `./GHOST_OS/magic.sh` for command list.

**Stuck?** Open GitHub issue.

**Vibing?** Keep building! 🔥
