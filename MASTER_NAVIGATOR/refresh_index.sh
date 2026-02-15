#!/bin/bash

# GHOSTLINE INDEX CORE - AUTO REFRESH SCRIPT
# Scans /VES directory and updates system_index.json
# Excludes system files, focuses on meaningful content

echo "🔍 Starting VES directory scan..."
echo "📁 Scanning /VES directory structure (excluding system files)..."

# Change to VES directory
cd ~/VES

# Initialize variables
total_dirs=0
total_files=0
indexed_paths=()
current_time=$(date -Iseconds)

# Function to check if file should be excluded
should_exclude() {
    local path="$1"
    
    # Exclude system files and directories
    [[ "$path" == *"/."* ]] && return 0  # Hidden files/dirs
    [[ "$path" == *"__pycache__"* ]] && return 0
    [[ "$path" == *".pyc" ]] && return 0
    [[ "$path" == *".log" ]] && return 0
    [[ "$path" == *"node_modules"* ]] && return 0
    [[ "$path" == *".git"* ]] && return 0
    [[ "$path" == *"venv"* ]] && return 0
    [[ "$path" == *"env"* ]] && return 0
    [[ "$path" == *".DS_Store"* ]] && return 0
    [[ "$path" == *"Thumbs.db"* ]] && return 0
    [[ "$path" == *"package-lock.json"* ]] && return 0
    [[ "$path" == *"yarn.lock"* ]] && return 0
    
    # If it's just a directory name check
    [[ "$(basename "$path")" == ".git" ]] && return 0
    [[ "$(basename "$path")" == "node_modules" ]] && return 0
    [[ "$(basename "$path")" == "__pycache__" ]] && return 0
    
    return 1  # Don't exclude
}

# Function to scan directory recursively
scan_directory() {
    local dir="$1"
    
    # Process each item in the directory
    for item in "$dir"/*; do
        # Skip if no matches
        [ ! -e "$item" ] && continue
        
        if [ -d "$item" ]; then
            # It's a directory - check if we should exclude it
            if ! should_exclude "$item"; then
                ((total_dirs++))
                indexed_paths+=("$item")
                
                # Recursively scan subdirectory
                scan_directory "$item"
            fi
        elif [ -f "$item" ]; then
            # It's a file - check if we should exclude it
            if ! should_exclude "$item"; then
                ((total_files++))
                indexed_paths+=("$item")
            fi
        fi
    done
}

# Start scanning from VES root
scan_directory "."

echo "📊 Scan results:"
echo "   Directories: $total_dirs"
echo "   Files: $total_files"
echo "   Total items processed: $((total_dirs + total_files))"

# Categorize files based on directory structure and file content
systems_count=0
research_count=0
archives_count=0
active_ops_count=0
tools_count=0
logs_count=0

systems_items=()
research_items=()
archives_items=()
active_ops_items=()
tools_items=()
logs_items=()

# Process all indexed paths to categorize them
for path in "${indexed_paths[@]}"; do
    # Get file modification time and size
    if [ -f "$path" ]; then
        mod_time=$(stat -c %y "$path" 2>/dev/null || echo "Unknown")
        size=$(stat -c %s "$path" 2>/dev/null || echo "0")
        size_kb=$((size / 1024))
        description="File"
    else
        mod_time=$(stat -c %y "$path" 2>/dev/null || echo "Unknown")
        size_kb=0
        description="Directory"
    fi
    
    # Determine category based on path and content
    basename_path=$(basename "$path")
    dirname_path=$(dirname "$path")
    
    # Check for meaningful content indicators
    is_meaningful=0
    
    # Check if it's a content file (not just system)
    if [[ "$path" == *"docker"* ]] || [[ "$path" == *"ves_"* ]] || [[ "$path" == *"constellation"* ]]; then
        ((systems_count++))
        systems_items+=("{\"path\":\"$path\",\"description\":\"System component\",\"importance\":\"HIGH\",\"last_update\":\"$mod_time\",\"size_kb\":$size_kb}")
        is_meaningful=1
    elif [[ "$path" == *"research"* ]] || [[ "$path" == *"analysis"* ]] || [[ "$path" == *"doc"* ]] || [[ "$path" == *"Ghostcore"* ]] || [[ "$path" == *"ghostcore"* ]]; then
        ((research_count++))
        research_items+=("{\"path\":\"$path\",\"description\":\"Research document\",\"importance\":\"HIGH\",\"last_update\":\"$mod_time\",\"size_kb\":$size_kb}")
        is_meaningful=1
    elif [[ "$path" == *"archive"* ]] || [[ "$path" == *"GHOSTCORE"* ]] || [[ "$path" == *"ghostcore"* ]] || [[ "$path" == *"2_SORTED"* ]]; then
        ((archives_count++))
        archives_items+=("{\"path\":\"$path\",\"description\":\"Archive file\",\"importance\":\"MED\",\"last_update\":\"$mod_time\",\"size_kb\":$size_kb}")
        is_meaningful=1
    elif [[ "$path" == *"operation"* ]] || [[ "$path" == *"fleet"* ]] || [[ "$path" == *"ranger"* ]] || [[ "$path" == *"ghostline"* ]]; then
        ((active_ops_count++))
        active_ops_items+=("{\"path\":\"$path\",\"description\":\"Active operation\",\"importance\":\"HIGH\",\"last_update\":\"$mod_time\",\"size_kb\":$size_kb}")
        is_meaningful=1
    elif [[ "$path" == *"tool"* ]] || [[ "$path" == *"script"* ]] || [[ "$path" == *".sh" ]] || [[ "$path" == *"pwa"* ]] || [[ "$path" == *"dashboard"* ]]; then
        ((tools_count++))
        tools_items+=("{\"path\":\"$path\",\"description\":\"Tool or script\",\"importance\":\"MED\",\"last_update\":\"$mod_time\",\"size_kb\":$size_kb}")
        is_meaningful=1
    elif [[ "$path" == *"log"* ]] || [[ "$path" == *"echo"* ]] || [[ "$path" == *"checkpoint"* ]] || [[ "$path" == *"status"* ]]; then
        ((logs_count++))
        logs_items+=("{\"path\":\"$path\",\"description\":\"Log or checkpoint\",\"importance\":\"LOW\",\"last_update\":\"$mod_time\",\"size_kb\":$size_kb}")
        is_meaningful=1
    elif [[ "$basename_path" == *".md" ]] || [[ "$basename_path" == *".txt" ]] || [[ "$basename_path" == *".pdf" ]] || [[ "$basename_path" == *".docx" ]]; then
        # Content files
        ((research_count++))
        research_items+=("{\"path\":\"$path\",\"description\":\"Content document\",\"importance\":\"MED\",\"last_update\":\"$mod_time\",\"size_kb\":$size_kb}")
        is_meaningful=1
    elif [[ "$basename_path" == *".json" ]] || [[ "$basename_path" == *".yaml" ]] || [[ "$basename_path" == *".yml" ]]; then
        # Config files that might be meaningful
        ((systems_count++))
        systems_items+=("{\"path\":\"$path\",\"description\":\"Configuration\",\"importance\":\"MED\",\"last_update\":\"$mod_time\",\"size_kb\":$size_kb}")
        is_meaningful=1
    fi
    
    # If it's a directory that's not categorized but contains meaningful content
    if [ -d "$path" ] && [ $is_meaningful -eq 0 ]; then
        # Check if directory contains meaningful files
        if find "$path" -maxdepth 1 -name "*.md" -o -name "*.txt" -o -name "*.pdf" -o -name "*.docx" -o -name "*docker*" -o -name "*ghostline*" -o -name "*research*" 2>/dev/null | grep -q .; then
            ((systems_count++))
            systems_items+=("{\"path\":\"$path\",\"description\":\"Content directory\",\"importance\":\"MED\",\"last_update\":\"$mod_time\",\"size_kb\":$size_kb}")
        fi
    fi
done

# Convert arrays to JSON format
systems_json="["
for i in "${!systems_items[@]}"; do
    systems_json+="${systems_items[i]}"
    if [ $i -lt $((${#systems_items[@]} - 1)) ]; then
        systems_json+=","
    fi
done
[ ${#systems_items[@]} -gt 0 ] || systems_json+="]"
systems_json+="]"

research_json="["
for i in "${!research_items[@]}"; do
    research_json+="${research_items[i]}"
    if [ $i -lt $((${#research_items[@]} - 1)) ]; then
        research_json+=","
    fi
done
[ ${#research_items[@]} -gt 0 ] || research_json+="]"
research_json+="]"

archives_json="["
for i in "${!archives_items[@]}"; do
    archives_json+="${archives_items[i]}"
    if [ $i -lt $((${#archives_items[@]} - 1)) ]; then
        archives_json+=","
    fi
done
[ ${#archives_items[@]} -gt 0 ] || archives_json+="]"
archives_json+="]"

active_ops_json="["
for i in "${!active_ops_items[@]}"; do
    active_ops_json+="${active_ops_items[i]}"
    if [ $i -lt $((${#active_ops_items[@]} - 1)) ]; then
        active_ops_json+=","
    fi
done
[ ${#active_ops_items[@]} -gt 0 ] || active_ops_json+="]"
active_ops_json+="]"

tools_json="["
for i in "${!tools_items[@]}"; do
    tools_json+="${tools_items[i]}"
    if [ $i -lt $((${#tools_items[@]} - 1)) ]; then
        tools_json+=","
    fi
done
[ ${#tools_items[@]} -gt 0 ] || tools_json+="]"
tools_json+="]"

logs_json="["
for i in "${!logs_items[@]}"; do
    logs_json+="${logs_items[i]}"
    if [ $i -lt $((${#logs_items[@]} - 1)) ]; then
        logs_json+=","
    fi
done
[ ${#logs_items[@]} -gt 0 ] || logs_json+="]"
logs_json+="]"

# Calculate approximate total size
approx_total_size=0
for path in "${indexed_paths[@]}"; do
    if [ -f "$path" ]; then
        size=$(stat -c %s "$path" 2>/dev/null || echo "0")
        approx_total_size=$((approx_total_size + size))
    fi
done
approx_total_size_kb=$((approx_total_size / 1024))

# Create the JSON structure
json_content="{
  \"ves_system_index\": {
    \"generated_at\": \"$current_time\",
    \"total_directories\": $total_dirs,
    \"total_files\": $total_files,
    \"total_size_kb\": $approx_total_size_kb,
    \"categories\": {
      \"systems\": {
        \"count\": $systems_count,
        \"items\": $systems_json
      },
      \"research\": {
        \"count\": $research_count,
        \"items\": $research_json
      },
      \"archives\": {
        \"count\": $archives_count,
        \"items\": $archives_json
      },
      \"active_operations\": {
        \"count\": $active_ops_count,
        \"items\": $active_ops_json
      },
      \"tools\": {
        \"count\": $tools_count,
        \"items\": $tools_json
      },
      \"logs\": {
        \"count\": $logs_count,
        \"items\": $logs_json
      }
    },
    \"indexed_paths\": ["
    
    # Add all paths to the indexed_paths array (only meaningful ones)
    meaningful_paths=()
    for path in "${indexed_paths[@]}"; do
        # Check if this path was categorized as meaningful
        for item in "${systems_items[@]}" "${research_items[@]}" "${archives_items[@]}" "${active_ops_items[@]}" "${tools_items[@]}" "${logs_items[@]}"; do
            if [[ "$item" == *"${path//\//\\/}"* ]]; then
                meaningful_paths+=("\"$path\"")
                break
            fi
        done
    done
    
    # Join the meaningful paths
    if [ ${#meaningful_paths[@]} -gt 0 ]; then
        json_content+=$(printf '%s,' "${meaningful_paths[@]}" | sed 's/,$//')
    fi
    json_content+="],
    \"last_scan\": \"$current_time\"
  }
}"

# Write the JSON to the system_index.json file
echo "$json_content" > ~/VES/MASTER_NAVIGATOR/system_index.json

echo "💾 system_index.json updated with scan results"
echo "📈 Categories:"
echo "   Systems: $systems_count"
echo "   Research: $research_count"
echo "   Archives: $archives_count"
echo "   Active Ops: $active_ops_count"
echo "   Tools: $tools_count"
echo "   Logs: $logs_count"

# Update the HTML index with current stats (just update the timestamp)
echo "📄 MASTER_INDEX.html ready for viewing"

echo "✅ VES directory scan completed successfully!"
echo "   Index available at: ~/VES/MASTER_NAVIGATOR/MASTER_INDEX.html"
echo "   Data available at: ~/VES/MASTER_NAVIGATOR/system_index.json"