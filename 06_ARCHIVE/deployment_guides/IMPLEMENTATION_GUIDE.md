# 🏗️ IMPLEMENTATION GUIDE: Complete Setup

Follow this guide to fully integrate the GrowOverTime system into your ProPublica workflow.

## 📦 Full File Structure

After implementation, your directory will look like:

```
ProPublica/ (or your project directory)
├── Dumps/                    # Drop new files here
│   ├── research.pdf
│   ├── document.docx
│   └── ...
├── content/                  # Auto-generated content
│   ├── research/            # Individual research items
│   │   ├── 2024-11-14-research-title/
│   │   │   ├── research-title.md
│   │   │   ├── research-title.html
│   │   │   └── media/
│   │   │       └── original-file.pdf
│   │   └── ... (more research)
│   ├── index/               # Index files
│   │   └── index.html
│   └── index.html           # Main index
├── growovertime_template.html # Layout template
├── add-research.py          # Add new research
├── regenerate.py            # Regenerate indexes  
├── grow.sh                  # Master script
└── START_HERE.md            # Quick start guide
```

## 🛠️ Step-by-Step Integration

### 1. **Set Up Directories**

```bash
# In your ProPublica directory (wherever you want to set this up):
mkdir -p Dumps
mkdir -p content/research
mkdir -p content/index
```

### 2. **Copy Core Files**

Copy these files from `/home/saba/` to your ProPublica directory:

```bash
# From the current location to your ProPublica directory
cp /home/saba/growovertime_template.html /path/to/your/ProPublica/
cp /home/saba/add-research.py /path/to/your/ProPublica/
cp /home/saba/regenerate.py /path/to/your/ProPublica/
cp /home/saba/grow.sh /path/to/your/ProPublica/
cp /home/saba/START_HERE.md /path/to/your/ProPublica/
cp /home/saba/GROWOVERTIME_README.md /path/to/your/ProPublica/
```

### 3. **Make Scripts Executable**

```bash
cd /path/to/your/ProPublica/
chmod +x grow.sh
```

### 4. **Test the System**

```bash
# Create test content
echo "This is test research content about the Sava River pollution investigation." > Dumps/test-research.txt

# Run in dry-run mode first (safe)
./grow.sh

# See what would happen, then run for real:
./grow.sh --no-dry-run
```

### 5. **Verify Setup**

After running the script:

```bash
# Check that content was created:
ls -la content/research/
ls -la content/index/

# Open the index in browser:
firefox content/index/index.html  # or your preferred browser
```

## 🔄 Workflow Integration

### Daily Research Workflow:

1. **Get new research** → Put in `Dumps/` directory
2. **Run growth command** → `./grow.sh --no-dry-run`
3. **Review results** → Check `content/index/index.html`

### Advanced Workflow:

```bash
# Process files and sync to Google Drive:
SYNC_DRIVE=1 ./grow.sh --no-dry-run

# Process many files at once:
cp *.pdf Dumps/
cp *.docx Dumps/
./grow.sh --no-dry-run

# Regenerate only (if you manually edited content):
./grow.sh --regen-only --no-dry-run
```

## 🔌 Integration with Existing System

If you already have files in your ProPublica directory, you can:

```bash
# 1. Move existing research to Dumps temporarily
mv index*.html Dumps/  # Move old index files to process them

# 2. Run the system to process them
./grow.sh --no-dry-run

# 3. Your old content is now properly organized in content/research/
```

## 🚨 Troubleshooting

### Common Issues:

**Issue:** `Permission denied` on grow.sh
**Solution:** 
```bash
chmod +x grow.sh
```

**Issue:** `python3: command not found`
**Solution:** Install Python 3 - system varies by OS

**Issue:** No new content appears
**Solution:** Make sure you're using `--no-dry-run` flag

**Issue:** PDF processing fails
**Solution:** Install PyPDF2: `pip3 install PyPDF2`

## 🧩 Customization

### Modify the Template

Edit `growovertime_template.html` to change the look/feel of all generated pages.

### Add Custom Metadata

Modify `add-research.py` to extract additional metadata from your specific file types.

### Adjust Tagging Logic

In `add-research.py`, modify the `generate_tags_from_content()` function to better match your research topics.

## 🔁 Migration from Old System

1. **Preserve everything**: Don't delete your existing files yet
2. **Set up new system**: Follow setup instructions above
3. **Test with copies**: Try on a few files first
4. **Gradual migration**: Move more files as you confirm the system works
5. **Final transition**: Once confident, point all new research to the new system

## 🏁 Success Verification

Run this test to verify everything works:

```bash
# Create a test file
echo -e "Title: Sava River Investigation\\n\\n## Summary\\nResearch about water pollution in Slovenia.\\n\\n## Key Points\\n- High pollution levels\\n- Government inaction\\n- Environmental impact" > Dumps/verification-test.txt

# Process it
./grow.sh --no-dry-run

# Verify output
if [ -f "content/index/index.html" ]; then
    echo "✅ Success! Index file created."
else
    echo "❌ Something went wrong."
fi
```

---

Your system is now ready to grow continuously without restarts! 🌱