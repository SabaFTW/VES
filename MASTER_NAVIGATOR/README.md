# GHOSTLINE INDEX CORE - MASTER NAVIGATOR

## Overview
The Ghostline Index Core is an intelligent indexing system that transforms the /VES directory into a living knowledge system. It provides structured access to all components of the VES ecosystem through both human-readable UI and machine-readable APIs.

## Components

### 1. System Index (JSON)
- **Location**: `/VES/MASTER_NAVIGATOR/system_index.json`
- **Purpose**: Backend-usable JSON intelligence
- **Content**: Structured knowledge model of the entire VES system
- **Fields**: path, category, description, importance, last_update, linked_context

### 2. Master Index (HTML)
- **Location**: `/VES/MASTER_NAVIGATOR/MASTER_INDEX.html`
- **Purpose**: Human-usable HTML UI index
- **Features**: 
  - System Status
  - Active Operations
  - Protocols
  - Research Vault
  - Agents
  - Archives
  - Tools
  - Logs & Checkpoints

### 3. Auto Refresh Script
- **Location**: `/VES/MASTER_NAVIGATOR/refresh_index.sh`
- **Purpose**: Scans VES directory and updates system_index.json
- **Execution**: Daily or manual trigger
- **Features**: Excludes system files, focuses on meaningful content

### 4. API Service
- **Location**: `/VES/MASTER_NAVIGATOR/api.sh`
- **Purpose**: Backend API for other agents to query
- **Endpoints**:
  - `GET /index` - Returns full index
  - `GET /search?q=term` - Search for term in index
  - `GET /summary?file=path` - Get summary of specific file

## Usage

### Manual Refresh
```bash
~/VES/MASTER_NAVIGATOR/refresh_index.sh
```

### View Index
Open in browser:
```
~/VES/MASTER_NAVIGATOR/MASTER_INDEX.html
```

### API Usage
```bash
# Get full index
~/VES/MASTER_NAVIGATOR/api.sh GET /index

# Search for term
~/VES/MASTER_NAVIGATOR/api.sh GET /search "q=search_term"

# Get file summary
~/VES/MASTER_NAVIGATOR/api.sh GET /summary "file=path/to/file"
```

## Categories

The system automatically categorizes content into:
- **Systems**: Core infrastructure components
- **Research**: Research documents and analysis
- **Archives**: Historical data and archives
- **Active Operations**: Current operational components
- **Tools**: Scripts and tools
- **Logs**: Logs and checkpoints

## Philosophy

- **Filesystem = Source of Truth**
- **Folder = Concept Domain**
- **Document = State / Instance**
- **Archives = History**
- **Active Projects = Live Operations**
- **Systems = Core infrastructure**
- **Research = Knowledge & narrative intelligence**

## Automation

To set up daily refresh, add to crontab:
```bash
# Daily at 6 AM
0 6 * * * ~/VES/MASTER_NAVIGATOR/refresh_index.sh
```

## Security

- All operations are read-only
- No external network access required
- Local file system only
- No sensitive data exposed

Built with 🔥 for freedom and sovereignty.