import os
import json
import re

# --- Configuration ---
BASE_DIR = "/home/saba/"
TARGET_HTML_FILES = [
    "GHOSTCORE_NEXUS_ULTIMATE.html",
    "Sabad_Constellation_Home.html"
]
SCAN_DIRS = [
    ".", # Scan the base directory itself for top-level files
    "DROP",
    "SYSTEM_OF_ASHES_FORENSIC_KIT",
    "GHOST_OS",
    "Desktop/ShobadOS",
    "Desktop/ProPublica",
    "VES_CORE",
    "AGENTS",
    "MEMORY",
    "VES/modules",
    "VES/portals",
    "VES/RESEARCH",
    "VES/scripts",
    "VES/SHABAD_CloudCore",
    "VES/SYSTEM",
    "VES/TROJAN_HORSE",
    "VES/Vault",
    "VES/htmls snippets"
]

# Exclude patterns for directory components (e.g., /venv/, /node_modules/)
EXCLUDE_DIR_COMPONENTS = [
    "venv", ".venv", "__pycache__", ".git", "node_modules",
    "site-packages", "archive", "test", "backup", "temp", "tmp",
    "dist", "build", "outputs", ".gemini", "logs", "htmls snippets/done" # More specific exclusions
]

# Exclude patterns for full relative file paths (e.g., containing specific words or formats)
EXCLUDE_FILE_PATTERNS = [
    ".log", ".bak", ".old", ".orig", ".pyc", ".DS_Store", "package-lock.json",
    "thumbs.db", ".json.js", ".map" # Exclude common temp/meta files
]

# Only include files with these extensions
INCLUDE_FILE_EXTENSIONS = [
    ".html", ".htm", ".md", ".txt", ".py", ".sh", ".js", ".json", ".yaml", ".yml",
    ".pdf", ".doc", ".docx", ".odt", ".csv", ".xls", ".xlsx", ".png", ".jpg", ".jpeg", ".gif", ".svg"
]

# --- File Classification ---
FILE_TYPES = {
    (".html", ".htm"): "PORTAL",
    (".py", ".sh"): "SCRIPT",
    (".js",): "CODE_SNIPPET",
    (".json", ".yaml", ".yml"): "CONFIG",
    (".md", ".txt"): "CODEX",
    (".pdf", ".doc", ".docx", ".odt"): "DOCUMENT",
    (".csv", ".xls", ".xlsx"): "DATA",
    (".png", ".jpg", ".jpeg", ".gif", ".svg"): "IMAGE"
}

def classify_file(file_path):
    """Classifies file based on extension and path keywords, with specific project logic."""
    filename = os.path.basename(file_path).lower()
    file_extension = os.path.splitext(filename)[1].lower()

    # Priority classifications based on specific file names or paths
    if "ecosystem_map.md" in filename:
        return "SYSTEM_MAP"
    if "master_codex_manifest.md" in filename:
        return "MANIFEST"
    if "agent_registry.json" in filename or "memory/" in file_path.lower():
        return "MEMORY_FRAGMENT"
    if "ves_core/" in file_path.lower() and (file_extension == ".py" or file_extension == ".sh"):
        return "VES_TOOL"
    if "agents/" in file_path.lower():
        return "AGENT_DEFINITION"
    if "trojan_horse/" in file_path.lower():
        return "MISSION_DATA"
    if "propublica/" in file_path.lower():
        return "RESEARCH_ASSET"
    if "desktop/shobados/" in file_path.lower() and file_extension == ".html":
        return "DASHBOARD_ELEMENT"
    if "drop/" in file_path.lower():
        return "DROP_CONTENT"
    if "system/" in file_path.lower() and (file_extension == ".py" or file_extension == ".sh"):
        return "SYSTEM_SCRIPT"
    if "module" in file_path.lower() and (file_extension == ".py" or file_extension == ".js"):
        return "MODULE"


    for extensions, file_type in FILE_TYPES.items():
        if file_extension in extensions:
            return file_type
            
    return "UNKNOWN_ARTIFACT" # Fallback for files not explicitly classified

def scan_and_filter_files(base_path, scan_dirs, exclude_dir_components, exclude_file_patterns, include_file_extensions):
    """
    Scans specified directories for relevant files,
    excluding paths/files matching patterns.
    Returns a list of dictionaries with 'name', 'path', 'type'.
    """
    found_files = []
    
    for scan_dir in scan_dirs:
        full_scan_path = os.path.join(base_path, scan_dir)
        if not os.path.exists(full_scan_path):
            print(f"Warning: Scan directory not found: {full_scan_path}")
            continue

        for root, dirs, files in os.walk(full_scan_path):
            # Convert current root to relative path for robust exclusion checks
            relative_root = os.path.relpath(root, base_path)

            # Filter out excluded directories and their contents if the current root path matches an exclude pattern
            # This prevents os.walk from entering excluded subtrees
            if any(component in relative_root.split(os.sep) for component in exclude_dir_components):
                 dirs[:] = [] # Don't traverse further into this excluded directory
                 continue
            
            # Filter the 'dirs' list itself for the current level
            dirs[:] = [d for d in dirs if not any(component in d for component in exclude_dir_components)]

            for file in files:
                full_file_path = os.path.join(root, file)
                relative_file_path = os.path.relpath(full_file_path, base_path)
                file_extension = os.path.splitext(file)[1].lower()
                
                # Exclude files based on extension, full path patterns, or specific file names
                if file_extension not in include_file_extensions:
                    continue
                if any(excl_pattern in relative_file_path for excl_pattern in exclude_file_patterns):
                    continue
                
                file_type = classify_file(relative_file_path)
                
                # Basic name cleaning: remove extension, replace separators with spaces, title case
                name_without_ext = os.path.splitext(file)[0]
                name = name_without_ext.replace('_', ' ').replace('-', ' ').title()

                found_files.append({
                    "name": name,
                    "path": f"./{relative_file_path}", # Relative path for HTML linking
                    "type": file_type
                })
    return found_files

def update_html_file_index(html_file_path, var_name, new_file_index_data):
    """
    Reads an HTML file, replaces its JavaScript array with the specified variable name,
    and writes the updated content back.
    """
    try:
        with open(html_file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Regex to find the target JavaScript array (e.g., 'const fileIndex = [...]' or 'const localFiles = [...]')
        pattern = rf"(const\s+{re.escape(var_name)}\s*=\s*\[[\s\S]*?\];)"
        match = re.search(pattern, content)

        if not match:
            print(f"Error: '{var_name}' array not found in {html_file_path}. Skipping update.")
            return False

        # Build the new fileIndex/localFiles string
        new_index_list_str = ",\n            ".join([json.dumps(item, ensure_ascii=False) for item in new_file_index_data])
        new_array_str = f"""const {var_name} = [
            {new_index_list_str}
        ];"""
        
        # Replace the old array with the new one
        updated_content = content[:match.start(1)] + new_array_str + content[match.end(1):]

        with open(html_file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print(f"Successfully updated '{var_name}' in {html_file_path}")
        return True

    except FileNotFoundError:
        print(f"Warning: HTML file not found: {html_file_path}. Skipping update.")
        return False
    except Exception as e:
        print(f"An error occurred while updating {html_file_path}: {e}")
        return False

def main():
    print("🚀 Starting GHOSTCORE Sync Protocol...")
    
    # Use refined exclusion lists
    nexus_files = scan_and_filter_files(
        BASE_DIR,
        SCAN_DIRS,
        EXCLUDE_DIR_COMPONENTS,
        EXCLUDE_FILE_PATTERNS,
        INCLUDE_FILE_EXTENSIONS
    )
    print(f"🔍 Found {len(nexus_files)} relevant files for indexing.")

    # List of (filename, variable_name) pairs to update
    files_to_update = [
        ("GHOSTCORE_NEXUS_ULTIMATE.html", "fileIndex"),
        ("Sabad_Constellation_Home.html", "localFiles")
    ]

    for filename, var_name in files_to_update:
        full_html_path = os.path.join(BASE_DIR, filename)
        update_html_file_index(full_html_path, var_name, nexus_files)

    print("✅ GHOSTCORE Sync Protocol finished.")

if __name__ == "__main__":
    main()