# VES AGENT SCOPE DOCUMENT

**Service:** VES Local Agent (`ves-agent.service`)
**File:** `/home/saba/ves-agent/agent.py`
**Binding:** `127.0.0.1:8420`
**Purpose:** Filesystem API gateway for VES PWA

---

## WHITELISTED DIRECTORIES

The agent provides access ONLY to these directories within `/home/saba`:

```
/home/saba/cloud_constellation
/home/saba/VES
/home/saba/core
/home/saba/ves-agent
/home/saba/codex
/home/saba/Desktop
/home/saba/CONSTELLATION_BRIDGE
/home/saba/MASTER_NAVIGATOR
/home/saba/AGENTS
/home/saba/CONSTELLATION
/home/saba/ACTIVE
```

**Total:** 11 directories

**Constraint:** All paths must resolve to subdirectories of `/home/saba`. Path traversal attempts (`../`) are blocked.

---

## ALLOWED FILE EXTENSIONS

The agent serves ONLY files with these extensions:

```
.md      (Markdown)
.txt     (Plain text)
.json    (JSON data)
.yaml    (YAML configuration)
.yml     (YAML configuration)
```

**Total:** 5 extensions

**All other extensions are denied.**

---

## EXPLICIT DENIALS

### ❌ Write Operations

- NO file creation
- NO file modification
- NO content upload
- NO data insertion

**Reason:** Read-only architecture.

---

### ❌ Delete Operations

- NO file deletion
- NO directory removal
- NO truncation
- NO purging

**Reason:** Agent has no delete functionality.

---

### ❌ Execute Operations

- NO shell commands
- NO script execution
- NO subprocess spawning
- NO code running

**Reason:** Agent is not a shell. It reads files, it does not run them.

---

### ❌ Shell Access

- NO SSH
- NO terminal emulation
- NO command line
- NO interactive shell

**Reason:** Agent is an HTTP API, not a remote access tool.

---

### ❌ Network Access

- NO outbound HTTP requests
- NO external API calls
- NO URL fetching
- NO external connections

**Reason:** Agent has no network client capabilities.

---

### ❌ System Modification

- NO configuration changes
- NO service management
- NO package installation
- NO system updates

**Reason:** Agent is confined to read-only filesystem operations.

---

### ❌ Executable File Access

**Blocked Extensions:**
- `.py` (Python scripts)
- `.js` (JavaScript)
- `.sh` (Shell scripts)
- `.exe` (Executables)
- `.bin` (Binaries)
- `.so` (Shared libraries)
- Any extension not in allowed list

**Reason:** Extension whitelist prevents execution risk.

---

## ACCESS CONTROL SUMMARY

| Operation | Allowed | Scope |
|-----------|---------|-------|
| Read files | ✅ Yes | Whitelisted dirs + extensions |
| List directories | ✅ Yes | Whitelisted dirs only |
| Scan system | ✅ Yes | Whitelisted dirs, max depth 3 |
| Write files | ❌ No | Not implemented |
| Delete files | ❌ No | Not implemented |
| Execute code | ❌ No | Not implemented |
| Shell access | ❌ No | Not implemented |
| Network access | ❌ No | No client code |

---

## EXAMPLE USE CASES

### ✅ Allowed Operations

```bash
# Read a markdown file
GET /read?path=VES/SHABAD_CloudCore/README.md

# List directory contents
GET /list?path=ACTIVE

# Get system inventory
GET /scan

# Read JSON configuration
GET /read?path=codex/config.json
```

### ❌ Denied Operations

```bash
# Try to read Python source
GET /read?path=ves-agent/agent.py
→ 403 Forbidden (extension not allowed)

# Try path traversal
GET /read?path=../../../etc/passwd
→ 403 Forbidden (outside BASE_DIR)

# Try to write (endpoint doesn't exist)
POST /write
→ 404 Not Found

# Try to execute (endpoint doesn't exist)
POST /exec?cmd=ls
→ 404 Not Found
```

---

## OPERATIONAL BOUNDARIES

### Where the Agent Can Reach

```
/home/saba/
├── cloud_constellation/     ✅ Yes
├── VES/                     ✅ Yes
├── core/                    ✅ Yes
├── ves-agent/               ✅ Yes (but only .md, .txt, .json, .yaml, .yml)
├── codex/                   ✅ Yes
├── Desktop/                 ✅ Yes
├── CONSTELLATION_BRIDGE/    ✅ Yes
├── MASTER_NAVIGATOR/        ✅ Yes
├── AGENTS/                  ✅ Yes
├── CONSTELLATION/           ✅ Yes
├── ACTIVE/                  ✅ Yes
└── [other directories]      ❌ No
```

### Where the Agent Cannot Reach

```
/root/          ❌ Outside BASE_DIR
/etc/           ❌ Outside BASE_DIR
/var/           ❌ Outside BASE_DIR
/tmp/           ❌ Outside BASE_DIR
/home/other/    ❌ Outside BASE_DIR
```

---

## REVISION HISTORY

| Date | Change | Reason |
|------|--------|--------|
| 2025-11-XX | Added initial 6 directories | System foundation |
| 2025-12-26 | Added 5 new directories (CONSTELLATION_BRIDGE, MASTER_NAVIGATOR, AGENTS, CONSTELLATION, ACTIVE) | Directory integration |

**Current Version:** 1.1 (11 whitelisted directories)

---

## COMPLIANCE STATEMENT

This agent operates within strict boundaries:

1. **Read-only** - Cannot modify filesystem
2. **Localhost-only** - Not accessible from network
3. **Whitelist-based** - Explicit allow-list, implicit deny
4. **Extension-filtered** - No executable access
5. **Path-safe** - Traversal protection

**These boundaries are enforced by code, not configuration.**

Changes to scope require modifying `/home/saba/ves-agent/agent.py` and restarting the service.

---

## CONTACT

For scope expansion requests, contact system administrator.

**DO NOT:**
- Add write operations
- Enable execute operations
- Expose to external network
- Disable path traversal protection
- Allow all file extensions

**These changes would violate the security model.**
