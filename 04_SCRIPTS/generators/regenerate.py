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