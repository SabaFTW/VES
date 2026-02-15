# 🚀 GET STARTED: GrowOverTime System

Welcome to your new self-growing research system! This will solve your "restart" problem by letting your ProPublica system grow continuously.

## 📋 What You Just Got

### Core Files:
1. **`growovertime_template.html`** - Universal web page template
2. **`add-research.py`** - Auto-processes new research files  
3. **`regenerate.py`** - Builds indexes automatically
4. **`grow.sh`** - Master script to run everything
5. **This file** - Getting started guide

## 🛠️ Setup (2 minutes)

```bash
# 1. Make the script executable
chmod +x grow.sh

# 2. Create your dumps directory if you don't have one
mkdir -p Dumps

# 3. Create the content structure
mkdir -p content/research
mkdir -p content/index
```

## 🔄 Daily Usage (30 seconds)

```bash
# Drop new research file in Dumps/
cp my-new-research.pdf Dumps/

# Grow your system
./grow.sh --no-dry-run
```

That's it! Your system will:
- Process the new file automatically
- Extract metadata
- Create proper documentation
- Update all indexes
- Never delete anything

## 🧪 Try It Now

1. Create a test file in Dumps/: `echo "Test research content" > Dumps/test-research.txt`
2. Run: `./grow.sh --no-dry-run`
3. Check the `content/` directory - you'll see your new research processed!

## 🔁 Advanced Usage

```bash
# Dry run first (always safe to try):
./grow.sh  # Just shows what would happen

# Only scan for new files (no regeneration):
./grow.sh --scan-only --no-dry-run

# Only regenerate indexes (no new files):
./grow.sh --regen-only --no-dry-run

# With Google Drive sync:
SYNC_DRIVE=1 ./grow.sh --no-dry-run
```

## 🚫 No More Restarts!

Your system now grows like a living organism:
- Add files to `Dumps/` 
- Run `./grow.sh --no-dry-run`
- Check `content/index/index.html` in browser
- System grows. Never restarts.

## 🆘 Help

- `./grow.sh --help` - Full command options
- New files go in `Dumps/` directory
- Processed content appears in `content/`
- All indexes auto-update

---

You're done! Your ProPublica system now grows in real time. 🌱