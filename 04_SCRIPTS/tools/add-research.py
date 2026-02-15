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