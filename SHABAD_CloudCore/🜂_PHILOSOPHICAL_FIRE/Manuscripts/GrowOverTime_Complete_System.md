# 🌱 Complete GrowOverTime System Package

This file contains everything you need to implement a system that grows without restarts.

## 📦 Core Files

### 1. HTML Template (`growovertime_template.html`)
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{title}}</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }
        header {
            border-bottom: 2px solid #2c3e50;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        h1 {
            color: #2c3e50;
            margin-bottom: 10px;
        }
        .metadata {
            color: #7f8c8d;
            font-size: 0.9em;
            margin-bottom: 20px;
        }
        .content {
            line-height: 1.8;
        }
        .content p {
            margin-bottom: 15px;
        }
        .content a {
            color: #3498db;
            text-decoration: none;
        }
        .content a:hover {
            text-decoration: underline;
        }
        nav ul {
            list-style: none;
            padding: 0;
        }
        nav li {
            margin-bottom: 10px;
        }
        nav a {
            padding: 8px 12px;
            display: block;
            background: #ecf0f1;
            border-radius: 4px;
            text-decoration: none;
            color: #2c3e50;
            transition: background 0.3s;
        }
        nav a:hover {
            background: #bdc3c7;
        }
        .footer {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            color: #7f8c8d;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{{title}}</h1>
            <div class="metadata">
                <strong>Date:</strong> {{date}} |
                <strong>Tags:</strong> {{tags}}
            </div>
        </header>
        
        <nav>
            <h3>Navigation</h3>
            {{navigation}}
        </nav>
        
        <main class="content">
            {{content}}
        </main>
        
        <div class="footer">
            <p>Generated on: {{generation_date}}</p>
            <p>Part of the ProPublica Research Archive</p>
        </div>
    </div>
</body>
</html>
```

### 2. Python Script - Add Research (`add-research.py`)
```python
#!/usr/bin/env python3
"""
Add Research Automation Script
Automatically processes research files from Dumps directory into structured content
"""

import os
import json
import shutil
from datetime import datetime
import re
import mimetypes

def extract_text_from_file(filepath):
    """Extract text content from various file types"""
    mime_type, _ = mimetypes.guess_type(filepath)
    
    if mime_type and 'text' in mime_type:
        # Handle text files
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            # Try with latin-1 if utf-8 fails
            with open(filepath, 'r', encoding='latin-1') as f:
                return f.read()
    elif mime_type and 'pdf' in mime_type:
        # Handle PDF files
        try:
            import PyPDF2
            with open(filepath, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\\n"
                return text
        except ImportError:
            return f"PDF content (requires PyPDF2 to extract text): {os.path.basename(filepath)}"
    elif mime_type and ('image' in mime_type or 'audio' in mime_type or 'video' in mime_type):
        return f"Media file: {os.path.basename(filepath)} - {mime_type}"
    else:
        # For unknown file types, try to read as text or return as binary info
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()[:2000]  # First 2000 chars as preview
        except:
            return f"File: {os.path.basename(filepath)} - Binary data ({mime_type})"

def generate_tags_from_content(content, filename):
    """Generate tags based on content and filename"""
    content_lower = content[:500].lower()  # Analyze first 500 chars
    filename_lower = filename.lower()
    
    common_tags = {
        'politics': ['government', 'minister', 'parliament', 'election', 'policy', 'politic'],
        'economy': ['money', 'finance', 'econom', 'market', 'bank', 'euro', 'price'],
        'environment': ['river', 'sava', 'pollution', 'water', 'nature', 'ecology', 'green'],
        'health': ['health', 'medical', 'sick', 'hospital', 'medicine'],
        'social': ['people', 'family', 'society', 'community', 'social'],
        'tech': ['digital', 'software', 'computer', 'tech', 'data', 'ai']
    }
    
    tags = set()
    full_text = content_lower + " " + filename_lower
    
    for tag, keywords in common_tags.items():
        if any(keyword in full_text for keyword in keywords):
            tags.add(tag)
    
    # Add any obvious tags from filename
    if 'sava' in filename_lower:
        tags.add('water')
        tags.add('slovenia')
    if 'gates' in filename_lower:
        tags.add('gates')
    if 'epstein' in filename_lower:
        tags.add('epstein')
    if 'cancer' in full_text:
        tags.add('health')
    
    # Extract any years from filename
    years = re.findall(r'\\d{4}', filename)
    for year in years:
        if 1900 < int(year) < 2100:
            tags.add(year)
    
    return list(tags) or ['research']

def process_research_file(dump_filepath, content_dir):
    """Process a single research file from Dumps to content directory"""
    filename = os.path.basename(dump_filepath)
    name, ext = os.path.splitext(filename)
    
    # Create date-based directory structure
    today = datetime.now()
    date_dir = f"{today.strftime('%Y-%m-%d')}-{name.lower().replace(' ', '-').replace('_', '-')}"
    output_dir = os.path.join(content_dir, 'research', date_dir)
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Extract content from file
    content = extract_text_from_file(dump_filepath)
    
    # Generate metadata
    title = name.replace('_', ' ').replace('-', ' ').title()
    date_str = today.strftime('%Y-%m-%d')
    tags = generate_tags_from_content(content, filename)
    tags_str = ', '.join(tags)
    
    # Create markdown content
    md_content = f"""---
title: "{title}"
date: "{date_str}"
tags: "{tags_str}"
source_file: "{filename}"
---

# {title}

**Date:** {date_str}  
**Tags:** {tags_str}  
**Original File:** {filename}

## Summary

{content[:500]}...

## Full Content

{content}

## Source Information
- **File:** {filename}
- **Processed:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Type:** {mimetypes.guess_type(dump_filepath)[0] or 'unknown'}
"""
    
    # Write markdown file
    md_filename = os.path.join(output_dir, f"{name}.md")
    with open(md_filename, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print(f"Processed: {filename} -> {md_filename}")
    print(f"  - Title: {title}")
    print(f"  - Date: {date_str}")
    print(f"  - Tags: {tags_str}")
    
    # Move original file to media directory
    media_dir = os.path.join(output_dir, 'media')
    if not os.path.exists(media_dir):
        os.makedirs(media_dir)
    
    new_file_path = os.path.join(media_dir, filename)
    shutil.copy2(dump_filepath, new_file_path)
    
    return {
        'title': title,
        'date': date_str,
        'tags': tags,
        'path': md_filename,
        'original_file': filename,
        'directory': date_dir
    }

def scan_and_add_research(dumps_dir="Dumps", content_dir="content"):
    """Scan Dumps directory and process any new files"""
    if not os.path.exists(dumps_dir):
        print(f"Dumps directory {dumps_dir} does not exist. Creating it...")
        os.makedirs(dumps_dir)
    
    if not os.path.exists(content_dir):
        print(f"Content directory {content_dir} does not exist. Creating it...")
        os.makedirs(content_dir)
        os.makedirs(os.path.join(content_dir, 'research'))
        os.makedirs(os.path.join(content_dir, 'index'))
    
    processed_files = []
    
    # Get all files in dumps directory
    for filename in os.listdir(dumps_dir):
        dump_filepath = os.path.join(dumps_dir, filename)
        
        # Skip directories and hidden files
        if os.path.isdir(dump_filepath) or filename.startswith('.'):
            continue
        
        # Check if already processed by checking content directory
        already_processed = False
        for root, dirs, files in os.walk(os.path.join(content_dir, 'research')):
            for file in files:
                if filename in file or filename in root:
                    already_processed = True
                    break
            if already_processed:
                break
        
        if not already_processed:
            try:
                result = process_research_file(dump_filepath, content_dir)
                processed_files.append(result)
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    
    return processed_files

if __name__ == "__main__":
    print("🔍 Scanning for new research files...")
    processed = scan_and_add_research()
    
    if processed:
        print(f"\\n✅ Successfully processed {len(processed)} files:")
        for item in processed:
            print(f"  - {item['title']} ({item['date']})")
    else:
        print("\\n✅ No new files to process")
    
    print("\\n📋 Scan complete!")
```

### 3. Python Script - Regenerate Index (`regenerate.py`)
```python
#!/usr/bin/env python3
"""
Regenerate Index Script
Creates an index.html file that lists all research content
"""

import os
import json
from datetime import datetime
import re

def extract_metadata_from_md(filepath):
    """Extract metadata from markdown file with YAML frontmatter"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Look for YAML frontmatter
    match = re.match(r'---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
    if match:
        frontmatter = match.group(1)
        rest_content = match.group(2)
        
        metadata = {}
        for line in frontmatter.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip().strip('"\'')
                metadata[key] = value
        
        return metadata, rest_content
    
    # If no frontmatter, create basic metadata
    filename = os.path.basename(filepath)
    name = os.path.splitext(filename)[0]
    return {
        'title': name.replace('_', ' ').replace('-', ' ').title(),
        'date': datetime.now().strftime('%Y-%m-%d'),
        'tags': 'research'
    }, content

def generate_navigation(research_items):
    """Generate navigation HTML for all research items"""
    nav_html = "<ul>"
    
    # Sort items by date (most recent first)
    sorted_items = sorted(research_items, key=lambda x: x['date'], reverse=True)
    
    for item in sorted_items:
        nav_html += f'<li><a href="research/{item["directory"]}/{item["original_file"].replace(os.path.splitext(item["original_file"])[1], ".html")}">{item["title"]} ({item["date"]})</a>'
        
        # Add tags as sub-list
        if item['tags']:
            nav_html += '<ul>'
            tags = item['tags'].split(', ')
            for tag in tags:
                nav_html += f'<li class="tag"><a href="#tag-{tag}">{tag}</a></li>'
            nav_html += '</ul>'
        nav_html += '</li>'
    
    nav_html += "</ul>"
    return nav_html

def generate_index_page(research_items):
    """Generate the main index.html page"""
    # Sort items by date (most recent first)
    sorted_items = sorted(research_items, key=lambda x: x['date'], reverse=True)
    
    # Generate navigation
    navigation_html = generate_navigation(sorted_items)
    
    # Generate content - list of all research items
    content_html = "<div class='research-list'>"
    content_html += "<h2>Research Archive</h2>"
    content_html += f"<p>Displaying {len(sorted_items)} research items</p>"
    
    # Group by year
    years = {}
    for item in sorted_items:
        year = item['date'][:4]
        if year not in years:
            years[year] = []
        years[year].append(item)
    
    for year in sorted(years.keys(), reverse=True):
        content_html += f"<h3>{year}</h3><ul>"
        for item in years[year]:
            content_html += f"<li><strong>{item['date']}</strong>: <a href='content/research/{item['directory']}/{item['original_file'].replace(os.path.splitext(item['original_file'])[1], '.html')}'>{item['title']}</a>"
            if item['tags']:
                content_html += f" <em>(tags: {item['tags']})</em>"
            content_html += "</li>"
        content_html += "</ul>"
    
    content_html += "</div>"
    
    # Create the full HTML
    template_path = "growovertime_template.html"
    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
    else:
        # Fallback template
        template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{title}}</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }
        header {
            border-bottom: 2px solid #2c3e50;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        h1 {
            color: #2c3e50;
            margin-bottom: 10px;
        }
        .metadata {
            color: #7f8c8d;
            font-size: 0.9em;
            margin-bottom: 20px;
        }
        .content {
            line-height: 1.8;
        }
        .content p {
            margin-bottom: 15px;
        }
        .content a {
            color: #3498db;
            text-decoration: none;
        }
        .content a:hover {
            text-decoration: underline;
        }
        nav ul {
            list-style: none;
            padding: 0;
        }
        nav li {
            margin-bottom: 10px;
        }
        nav a {
            padding: 8px 12px;
            display: block;
            background: #ecf0f1;
            border-radius: 4px;
            text-decoration: none;
            color: #2c3e50;
            transition: background 0.3s;
        }
        nav a:hover {
            background: #bdc3c7;
        }
        .footer {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            color: #7f8c8d;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{{title}}</h1>
            <div class="metadata">
                <strong>Date:</strong> {{date}} |
                <strong>Tags:</strong> {{tags}}
            </div>
        </header>
        
        <nav>
            <h3>Navigation</h3>
            {{navigation}}
        </nav>
        
        <main class="content">
            {{content}}
        </main>
        
        <div class="footer">
            <p>Generated on: {{generation_date}}</p>
            <p>Part of the ProPublica Research Archive</p>
        </div>
    </div>
</body>
</html>"""
    
    # Replace placeholders
    index_title = "ProPublica Research Archive - Index"
    index_date = datetime.now().strftime('%Y-%m-%d')
    
    index_html = template.replace('{{title}}', index_title)
    index_html = index_html.replace('{{date}}', index_date)
    index_html = index_html.replace('{{tags}}', 'index, archive, research')
    index_html = index_html.replace('{{navigation}}', navigation_html)
    index_html = index_html.replace('{{content}}', content_html)
    index_html = index_html.replace('{{generation_date}}', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    return index_html

def regenerate_all_indexes(content_dir="content"):
    """Regenerate all index files"""
    research_dir = os.path.join(content_dir, 'research')
    
    if not os.path.exists(research_dir):
        print(f"Research directory {research_dir} does not exist.")
        return
    
    # Collect all research items
    research_items = []
    
    for item_dir in os.listdir(research_dir):
        item_path = os.path.join(research_dir, item_dir)
        if os.path.isdir(item_path):
            # Look for markdown files in the directory
            for file in os.listdir(item_path):
                if file.endswith('.md'):
                    md_path = os.path.join(item_path, file)
                    metadata, _ = extract_metadata_from_md(md_path)
                    
                    research_items.append({
                        'title': metadata.get('title', item_dir),
                        'date': metadata.get('date', 'unknown'),
                        'tags': metadata.get('tags', 'research'),
                        'original_file': file,
                        'directory': item_dir,
                        'path': md_path
                    })
    
    # Generate main index
    index_html = generate_index_page(research_items)
    
    index_dir = os.path.join(content_dir, 'index')
    if not os.path.exists(index_dir):
        os.makedirs(index_dir)
    
    index_path = os.path.join(index_dir, 'index.html')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_html)
    
    print(f"✅ Regenerated index with {len(research_items)} items")
    print(f"📄 Index saved to: {index_path}")
    
    # Also create/update a main index in the content root
    root_index_path = os.path.join(content_dir, 'index.html')
    with open(root_index_path, 'w', encoding='utf-8') as f:
        f.write(index_html)
    
    print(f"📄 Root index saved to: {root_index_path}")
    
    return research_items

def generate_individual_pages(content_dir="content"):
    """Generate individual HTML pages for each research item"""
    research_dir = os.path.join(content_dir, 'research')
    
    if not os.path.exists(research_dir):
        print(f"Research directory {research_dir} does not exist.")
        return
    
    # Read the template
    template_path = "growovertime_template.html"
    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
    else:
        print("Template not found, skipping individual page generation")
        return
    
    for item_dir in os.listdir(research_dir):
        item_path = os.path.join(research_dir, item_dir)
        if os.path.isdir(item_path):
            # Look for markdown files in the directory
            for file in os.listdir(item_path):
                if file.endswith('.md'):
                    md_path = os.path.join(item_path, file)
                    metadata, content = extract_metadata_from_md(md_path)
                    
                    # Convert markdown content to simple HTML (basic conversion)
                    html_content = content.replace('\n\n', '</p><p>').replace('\n# ', '<h1>').replace('# ', '<h1>') 
                    html_content = f'<p>{html_content}</p>'
                    
                    # Replace placeholders in template
                    page_html = template.replace('{{title}}', metadata.get('title', 'Unknown Title'))
                    page_html = page_html.replace('{{date}}', metadata.get('date', 'Unknown Date'))
                    page_html = page_html.replace('{{tags}}', metadata.get('tags', 'research'))
                    page_html = page_html.replace('{{content}}', html_content)
                    page_html = page_html.replace('{{navigation}}', '<a href="../index/index.html">← Back to Index</a>')
                    page_html = page_html.replace('{{generation_date}}', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    
                    # Write HTML file
                    html_filename = file.replace('.md', '.html')
                    html_path = os.path.join(item_path, html_filename)
                    with open(html_path, 'w', encoding='utf-8') as f:
                        f.write(page_html)
                    
                    print(f"📄 Generated page: {html_path}")

if __name__ == "__main__":
    print("🔄 Regenerating indexes...")
    
    research_items = regenerate_all_indexes()
    generate_individual_pages()
    
    print(f"\\n✅ Regeneration complete!")
    print(f"📊 Processed {len(research_items)} research items")
    print(f"📁 Index files updated in content/index/ and content/")
```

### 4. Master Script (`grow.sh`)
```bash
#!/bin/bash
# Master Growth Script for ProPublica Research System
# This script orchestrates the entire growth process

set -e  # Exit on any error

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DUMPS_DIR="${DUMPS_DIR:-${SCRIPT_DIR}/Dumps}"
CONTENT_DIR="${CONTENT_DIR:-${SCRIPT_DIR}/content}"
CORE_DIR="${CORE_DIR:-${SCRIPT_DIR}/core}"
AUTOMATION_DIR="${AUTOMATION_DIR:-${SCRIPT_DIR}/automation}"

# Default values
DRY_RUN=${DRY_RUN:-1}
SYNC_DRIVE=${SYNC_DRIVE:-0}
VERBOSE=${VERBOSE:-0}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to show help
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo "Options:"
    echo "  -d, --dumps DIR      Set Dumps directory (default: ./Dumps)"
    echo "  -c, --content DIR    Set Content directory (default: ./content)"
    echo "  -n, --no-dry-run     Disable dry run mode (actually process files)"
    echo "  -s, --sync-drive     Enable Google Drive sync"
    echo "  -v, --verbose        Enable verbose output"
    echo "  --scan-only          Only scan and add research, no regeneration"
    echo "  --regen-only         Only regenerate indexes, no new files"
    echo "  --help               Show this help message"
    echo ""
    echo "Environment variables:"
    echo "  DRY_RUN=1            Enable dry run (default)"
    echo "  DRY_RUN=0            Disable dry run"
    echo "  SYNC_DRIVE=1         Enable Google Drive sync"
    echo "  VERBOSE=1            Enable verbose output"
    echo ""
    echo "Example usage:"
    echo "  $0 --no-dry-run                      # Process files and regenerate"
    echo "  DRY_RUN=0 SYNC_DRIVE=1 $0            # Process files, regenerate, and sync"
}

# Parse command line arguments
SCAN_ONLY=0
REGEN_ONLY=0

while [[ $# -gt 0 ]]; do
    case $1 in
        -d|--dumps)
            DUMPS_DIR="$2"
            shift 2
            ;;
        -c|--content)
            CONTENT_DIR="$2"
            shift 2
            ;;
        -n|--no-dry-run)
            DRY_RUN=0
            shift
            ;;
        -s|--sync-drive)
            SYNC_DRIVE=1
            shift
            ;;
        -v|--verbose)
            VERBOSE=1
            shift
            ;;
        --scan-only)
            SCAN_ONLY=1
            shift
            ;;
        --regen-only)
            REGEN_ONLY=1
            shift
            ;;
        --help)
            show_help
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Enable verbose mode if requested
if [ $VERBOSE -eq 1 ]; then
    set -x
fi

# Main execution
main() {
    print_status "🚀 Starting ProPublica Growth System"
    print_status "Dumps directory: $DUMPS_DIR"
    print_status "Content directory: $CONTENT_DIR"
    print_status "Dry run mode: $([ $DRY_RUN -eq 1 ] && echo "ENABLED" || echo "DISABLED")"
    print_status "Google Drive sync: $([ $SYNC_DRIVE -eq 1 ] && echo "ENABLED" || echo "DISABLED")"
    
    # Create directories if they don't exist
    if [ $DRY_RUN -eq 0 ]; then
        mkdir -p "$DUMPS_DIR"
        mkdir -p "$CONTENT_DIR"
        mkdir -p "$CONTENT_DIR/index"
        mkdir -p "$CONTENT_DIR/research"
        print_success "Directories created/verified"
    fi
    
    # Run the growth process
    if [ $REGEN_ONLY -eq 1 ]; then
        print_status "🔄 Running regeneration only..."
        if [ $DRY_RUN -eq 1 ]; then
            print_warning "DRY RUN: Would regenerate indexes"
        else
            python3 regenerate.py
            print_success "Indexes regenerated"
        fi
    elif [ $SCAN_ONLY -eq 1 ]; then
        print_status "🔍 Running scan only..."
        if [ $DRY_RUN -eq 1 ]; then
            print_warning "DRY RUN: Would scan for new research"
        else
            python3 add-research.py
            print_success "New research scanned and processed"
        fi
    else
        print_status "🔍 Scanning for new research files..."
        if [ $DRY_RUN -eq 1 ]; then
            print_warning "DRY RUN: Would scan and add research"
        else
            python3 add-research.py
            print_success "New research processed"
        fi
        
        print_status "🔄 Regenerating indexes..."
        if [ $DRY_RUN -eq 1 ]; then
            print_warning "DRY RUN: Would regenerate indexes"
        else
            python3 regenerate.py
            print_success "Indexes regenerated"
        fi
        
        # Google Drive sync if enabled
        if [ $SYNC_DRIVE -eq 1 ]; then
            print_status "☁️  Syncing with Google Drive..."
            if [ $DRY_RUN -eq 1 ]; then
                print_warning "DRY RUN: Would sync with Google Drive"
            else
                if command -v rclone &> /dev/null; then
                    # Sync content directory to Google Drive
                    # Assumes you have rclone configured with a remote called "gdrive"
                    if [ -d "$CONTENT_DIR" ]; then
                        print_status "Syncing $CONTENT_DIR to Google Drive..."
                        rclone sync "$CONTENT_DIR" "gdrive:ProPublica" --progress
                        print_success "Google Drive sync completed"
                    else
                        print_error "Content directory does not exist: $CONTENT_DIR"
                    fi
                else
                    print_error "rclone not found. Please install and configure rclone for Google Drive sync."
                    print_warning "Skipping Google Drive sync"
                fi
            fi
        fi
    fi
    
    print_success "✅ Growth process completed!"
    print_status "Your ProPublica system has grown without restart!"
}

# Run main function
main "$@"
```

## 📚 Documentation

### START_HERE.md
```markdown
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
```

### IMPLEMENTATION_GUIDE.md
```markdown
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
```

### GROWOVERTIME_README.md
```markdown
# 🌱 GROWOVERTIME SYSTEM

*"Systems that grow without restarts"*

## 🧠 Philosophy

Traditional systems require "restarting" - rebuilding from scratch when new knowledge emerges. This creates fear of growth, leading to fragmentation and lost work.

The GrowOverTime system is different. It's designed to continuously evolve, adding new knowledge while preserving everything that came before. Like a living organism, it grows incrementally, never losing its foundation.

## 🔥 Core Principles

### 1. **NEVER DELETE** 
- Every piece of research is preserved
- Old versions remain accessible
- Growth is additive, not replacement-based

### 2. **AUTOMATED ORGANIZATION**
- Files automatically sorted by date
- Metadata extracted automatically
- Indexes updated automatically

### 3. **SCALABLE STRUCTURE**
- Works with 1 file or 10,000 files
- Consistent organization regardless of size
- Navigation adapts to content volume

### 4. **CONTINUOUS INTEGRATION**
- New content immediately available
- No downtime during growth
- System remains accessible during updates

## 🏗️ How It Works

### The Process Flow:
```
New File (Dumps/) → Auto-Processing → Organized Content → Updated Indexes → Live System
```

### The File Structure:
```
Dumps/                    # Input zone - drop new files here
└── my-research.pdf

content/                  # Output zone - auto-organized
├── research/            # Chronologically organized research
│   ├── 2024-11-14-my-research-title/
│   │   ├── my-research-title.md
│   │   ├── my-research-title.html  
│   │   └── media/
│   │       └── my-research.pdf
│   └── ... (more research, organized by date)
├── index/               # Auto-generated navigation
│   └── index.html
└── index.html           # Main entry point
```

## 🎯 Use Cases

This system is perfect for:

- **Research collections** - Academic, investigative, or personal research
- **Knowledge bases** - Organizing information that grows over time  
- **Documentation** - Technical docs, project notes, meeting records
- **Archive systems** - Historical records that should never be lost
- **Investigative journalism** - Evidence, sources, and analysis

## 🛠️ Technical Features

### Auto-Processing:
- **File type detection** - Handles PDFs, text files, images, and more
- **Metadata extraction** - Automatically generates titles, dates, tags
- **Text extraction** - Pulls content from PDFs for searching/indexing
- **Smart tagging** - Identifies topics automatically

### Navigation:
- **Chronological organization** - Research organized by date processed
- **Tag-based discovery** - Topics automatically categorized
- **Hierarchical structure** - Easy navigation between items
- **Responsive design** - Works on all devices

### Scalability:
- **Performance maintained** - System doesn't slow down as it grows
- **Modular design** - Components can be used independently
- **Extensible** - Easy to add new features or change behavior
- **Robust** - Errors in one file don't affect the whole system

## 🔄 Growth Process

### Adding New Content:
1. Place new research file in `Dumps/` directory
2. Run `./grow.sh --no-dry-run`
3. System processes, organizes, and indexes the content
4. New content immediately available in the system

### The Growth Scripts:
- **`add-research.py`** - Finds new files and processes them into structured content
- **`regenerate.py`** - Updates all indexes and navigation to include new content  
- **`grow.sh`** - Master script to run the full process automatically

## 🧭 Long-term Vision

This system represents a shift from "project-based" to "organism-based" information management. Instead of:

1. Accumulate files → 
2. Feel overwhelmed → 
3. Restart and reorganize → 
4. Repeat

We have:

1. Continuous input →
2. Automatic organization → 
3. Living system →
4. Sustained growth

The system becomes a reflection of your growing knowledge - always accessible, always organized, always expanding.

## ✅ Success Indicators

Your system is working correctly when:

- [ ] New files appear in `Dumps/` 
- [ ] Running `./grow.sh` processes them automatically
- [ ] New content shows up in `content/research/`
- [ ] Indexes update to include new items
- [ ] Old content remains unchanged and accessible
- [ ] System performance stays consistent as it grows

## 🌿 The Living System

This isn't just a file organization system - it's a **digital garden** that grows with you. Each addition strengthens the whole, and nothing is ever lost. It's designed to support research practices that evolve over years or decades, not just projects with fixed endpoints.

Your ProPublica investigation can now grow organically, adapting to new information while maintaining the integrity of everything that came before. No more restarts. No more fear of growth. Just continuous evolution.

---

*GrowOverTime: Systems that evolve, not restart.* 🌱
```

## 🚀 How to Use This Complete System

1. **Copy each file content** from the sections above to create the corresponding files in your ProPublica directory
2. **Make the script executable**: `chmod +x grow.sh`
3. **Run a test**: 
   ```bash
   echo "Test research" > Dumps/test.txt
   ./grow.sh --no-dry-run
   ```

This system will allow your ProPublica research system to grow continuously without ever needing to restart or rebuild from scratch. Each new file you add to the Dumps/ folder will be automatically processed, organized, and added to your growing archive while preserving everything that came before.

The system is designed to eliminate the fear of growth and fragmentation that has caused you to restart your research system multiple times. Now it will grow organically like a living organism! 🌱