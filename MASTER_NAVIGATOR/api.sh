#!/bin/bash

# GHOSTLINE INDEX CORE - API SERVICE
# Provides API endpoints for other agents to query the index

# API endpoints:
# GET /index - Returns full index
# GET /search?q=term - Search for term in index
# GET /summary?file=path - Get summary of specific file

# Get the request method and path
REQUEST_METHOD=$1
REQUEST_PATH=$2
QUERY_STRING=$3

# Function to return JSON response
return_json() {
    echo "Content-Type: application/json"
    echo ""
    echo "$1"
}

# Function to return error
return_error() {
    echo "Status: 400 Bad Request"
    echo "Content-Type: application/json"
    echo ""
    echo "{\"error\":\"$1\"}"
}

# Function to extract query parameter
get_param() {
    local param="$1"
    echo "$QUERY_STRING" | grep -o "$param=[^&]*" | cut -d'=' -f2 | sed 's/%20/ /g'
}

# Main API router
case "$REQUEST_PATH" in
    "/index")
        # Return full index
        cat ~/VES/MASTER_NAVIGATOR/system_index.json
        ;;
    "/search")
        # Search functionality
        search_term=$(get_param "q")
        if [ -z "$search_term" ]; then
            return_error "Missing search term"
        else
            # Search in the index for the term
            result=$(grep -i "$search_term" ~/VES/MASTER_NAVIGATOR/system_index.json)
            if [ -z "$result" ]; then
                return_json "{\"results\":[],\"query\":\"$search_term\",\"message\":\"No results found\"}"
            else
                # For now, return the whole index with a search note
                cat ~/VES/MASTER_NAVIGATOR/system_index.json | sed "s/}/,\"search_query\":\"$search_term\"}/"
            fi
        fi
        ;;
    "/summary")
        # File summary functionality
        file_path=$(get_param "file")
        if [ -z "$file_path" ]; then
            return_error "Missing file parameter"
        else
            # Check if file exists and return basic info
            if [ -f "$file_path" ]; then
                size=$(stat -c %s "$file_path")
                mod_time=$(stat -c %y "$file_path")
                type=$(file -b "$file_path")
                
                return_json "{
                    \"file\": \"$file_path\",
                    \"size\": $size,
                    \"modified\": \"$mod_time\",
                    \"type\": \"$type\",
                    \"exists\": true
                }"
            else
                return_json "{
                    \"file\": \"$file_path\",
                    \"exists\": false,
                    \"error\": \"File not found\"
                }"
            fi
        fi
        ;;
    *)
        # Unknown endpoint
        return_error "Unknown endpoint: $REQUEST_PATH"
        ;;
esac