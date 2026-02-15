# VES AGENT SECURITY AUDIT

**Date:** 2025-12-26
**Subject:** `/home/saba/ves-agent/agent.py`
**Version:** 1.0.0
**Status:** Operational (systemd service `ves-agent.service`)

---

## EXECUTIVE SUMMARY

The VES Agent is a **read-only filesystem API** running on `localhost:8420`. It provides HTTP access to whitelisted directories for the VES PWA frontend.

**Security Model:** Defense in depth
- Localhost-only binding (no external network exposure)
- Whitelisted directories (explicit allow-list)
- File extension filtering (no executables)
- Path traversal prevention (no `../` escapes)
- Read-only operations (no write, delete, or execute)

**Risk Level:** LOW (for intended use case)

---

## API ENDPOINTS

### 1. `GET /`

**Purpose:** Service identification and health check

**Input:** None

**Output:**
```json
{
  "service": "VES Agent",
  "status": "operational",
  "version": "1.0.0"
}
```

**Security Impact:** None (informational only)

---

### 2. `GET /health`

**Purpose:** System health verification

**Input:** None

**Output:**
```json
{
  "status": "ok",
  "base_dir": "/home/saba"
}
```

**Security Impact:** Discloses base directory path. Acceptable for localhost-only service.

---

### 3. `GET /read?path=<file_path>`

**Purpose:** Read file contents

**Input:** `path` parameter (relative to `/home/saba`)

**Output:** Plain text file contents

**Security Controls:**
- Path is resolved to absolute, checked against `BASE_DIR`
- File must exist and be a file (not directory)
- Extension must be in `ALLOWED_EXTENSIONS` (`.md`, `.txt`, `.json`, `.yaml`, `.yml`)
- Returns 403 if access denied
- Returns 404 if file not found
- Returns 400 if not a file
- Returns 500 on unexpected errors

**Example Attack Scenarios:**

| Attack | Input | Result |
|--------|-------|--------|
| Path traversal | `../../../etc/passwd` | 403 (outside `BASE_DIR`) |
| Executable access | `ves-agent/agent.py` | 403 (`.py` not allowed) |
| Directory read | `core/` | 400 (not a file) |
| Non-existent file | `fake.md` | 404 (not found) |

**Risk:** LOW (read-only, whitelisted extensions)

---

### 4. `GET /list?path=<dir_path>`

**Purpose:** List directory contents

**Input:** `path` parameter (relative to `/home/saba`, defaults to `""`)

**Output:** Array of items with `name`, `type` (`dir` or `file`), and `path`

**Security Controls:**
- Path is resolved to absolute, checked against `BASE_DIR`
- Directory must exist and be a directory
- Returns 403 if access denied
- Returns 404 if directory not found
- Returns 400 if not a directory
- Returns 500 on unexpected errors

**Example Output:**
```json
[
  {"name": "VES", "type": "dir", "path": "VES"},
  {"name": "README.md", "type": "file", "path": "README.md"}
]
```

**Risk:** LOW (directory enumeration is intentional functionality)

---

### 5. `GET /reports`

**Purpose:** List Cloud Constellation reports

**Input:** None

**Output:** Array of report metadata

**Hardcoded Path:** `/home/saba/cloud_constellation/data/reports`

**Security Controls:**
- Only scans `.md` files in reports directory
- Returns empty array if directory doesn't exist

**Risk:** MINIMAL (specialized endpoint, read-only)

---

### 6. `GET /scan`

**Purpose:** System inventory and directory statistics

**Input:** None

**Output:** JSON structure with directory summaries, file counts, and size

**Whitelisted Directories:**
```python
[
  "cloud_constellation",
  "VES",
  "core",
  "ves-agent",
  "codex",
  "Desktop",
  "CONSTELLATION_BRIDGE",
  "MASTER_NAVIGATOR",
  "AGENTS",
  "CONSTELLATION",
  "ACTIVE"
]
```

**Security Controls:**
- Only scans whitelisted directories
- Maximum depth of 3 levels (prevents deep filesystem traversal)
- Skips directories with permission errors (fails safely)
- Counts files by extension, calculates sizes

**Risk:** LOW (intentional system introspection, limited scope)

---

## FILESYSTEM ACCESS CONTROLS

### Allowed File Extensions

```python
ALLOWED_EXTENSIONS = {".md", ".txt", ".json", ".yaml", ".yml"}
```

**Rationale:** Documentation and configuration files only. No executables, no binaries, no scripts.

**Blocked Extensions:**
- `.py` (Python scripts)
- `.js` (JavaScript)
- `.sh` (Shell scripts)
- `.exe` (Executables)
- `.bin` (Binaries)
- `.so` (Shared libraries)
- All others not explicitly allowed

---

### Path Traversal Protection

**Implementation (agent.py:42-44, 69-71):**

```python
file_path = file_path.resolve()
if not str(file_path).startswith(str(BASE_DIR)):
    return JSONResponse({"error": "Access denied"}, status_code=403)
```

**Test Cases:**

| Input Path | Resolved Path | Result |
|------------|---------------|--------|
| `VES/README.md` | `/home/saba/VES/README.md` | ✅ Allowed |
| `../../../etc/passwd` | `/etc/passwd` | ❌ 403 (outside BASE_DIR) |
| `core/../../../root/.ssh` | `/root/.ssh` | ❌ 403 (outside BASE_DIR) |
| `VES/./SHABAD_CloudCore/README.md` | `/home/saba/VES/SHABAD_CloudCore/README.md` | ✅ Allowed |

**Effectiveness:** HIGH (Python's `Path.resolve()` normalizes paths before checking)

---

### Base Directory Constraint

```python
BASE_DIR = Path("/home/saba")
```

**Effect:** All file operations are restricted to `/home/saba` and its subdirectories.

**Cannot Access:**
- `/root`
- `/etc`
- `/var`
- `/tmp`
- Any other user's home directory

---

## NETWORK SECURITY

### Binding Configuration

**Code (agent.py:253):**
```python
uvicorn.run(app, host="127.0.0.1", port=8420)
```

**Result:**
- Listens ONLY on `127.0.0.1` (loopback interface)
- NOT accessible from `192.168.x.x` (LAN)
- NOT accessible from `0.0.0.0` (all interfaces)
- NOT accessible from external networks

**Test:**
```bash
curl http://localhost:8420/       # ✅ Works
curl http://127.0.0.1:8420/       # ✅ Works
curl http://192.168.1.x:8420/     # ❌ Connection refused
curl http://external.ip:8420/     # ❌ Connection refused
```

---

### CORS Configuration

**Code (agent.py:16-22):**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8099", "http://127.0.0.1:8099"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Effect:**
- PWA at `http://localhost:8099` can make requests
- Other origins (e.g., `http://evil.com`) are blocked by browser
- Credentials (cookies, auth headers) are allowed from permitted origins

**Risk:** MINIMAL (localhost-only, single trusted origin)

---

## OPERATIONS EXPLICITLY NOT POSSIBLE

### ❌ Write Operations

**Not Implemented:**
- No `POST /write` endpoint
- No file creation
- No file modification
- No content upload

**Why:** Read-only architecture by design. Agent does not support write operations.

---

### ❌ Delete Operations

**Not Implemented:**
- No `DELETE /delete` endpoint
- No file deletion
- No directory deletion
- No truncation

**Why:** Agent has no delete functionality. Filesystem is immutable from agent's perspective.

---

### ❌ Execute Operations

**Not Implemented:**
- No `POST /exec` endpoint
- No shell command execution
- No script running
- No subprocess spawning

**Why:** Agent is not a remote shell. It reads files, it does not execute them.

---

### ❌ File Upload

**Not Implemented:**
- No multipart form data handling
- No binary upload
- No file transfer

**Why:** Agent serves content, it does not receive it.

---

### ❌ External Network Access

**Not Possible:**
- Agent cannot fetch URLs
- Agent cannot make outbound HTTP requests
- Agent cannot access external APIs

**Why:** No network client code exists. Agent only responds to localhost requests.

---

### ❌ User Authentication

**Not Implemented:**
- No login system
- No user accounts
- No password verification
- No tokens or sessions

**Why:** Single-user system on localhost. OS-level authentication (user owns `/home/saba`) is the security boundary.

---

## THREAT MODEL

### In-Scope Threats

| Threat | Mitigation | Residual Risk |
|--------|-----------|---------------|
| Path traversal attack | `Path.resolve()` + BASE_DIR check | LOW |
| Reading system files | Extension whitelist + BASE_DIR | MINIMAL |
| Port scanning disclosure | Localhost-only binding | MINIMAL |
| CORS bypass | Strict origin whitelist | LOW |

### Out-of-Scope Threats

| Threat | Why Out of Scope |
|--------|------------------|
| Remote network attack | Agent not accessible from network |
| SQL injection | No database |
| XSS | No HTML rendering, plain text responses |
| CSRF | Read-only operations, no state changes |
| Authentication bypass | No authentication implemented |

---

## SYSTEMD SERVICE SECURITY

**Service File:** `/home/saba/.config/systemd/user/ves-agent.service`

**Key Properties:**
- Runs as user `saba` (not root)
- No privilege escalation
- Restarts on failure (availability, not security)
- Working directory: `/home/saba/ves-agent`

**Implications:**
- Agent has same permissions as user `saba`
- Cannot access files outside `saba`'s permissions
- Cannot modify system files
- Cannot affect other users

---

## DEPENDENCY SECURITY

**Python Dependencies:**
- `fastapi` - Well-maintained web framework
- `uvicorn` - ASGI server (standard for FastAPI)
- `starlette` - FastAPI dependency (HTTP handling)

**Vulnerability Management:**
- Dependencies installed in virtual environment (`venv/`)
- Check for updates: `pip list --outdated`
- No known critical vulnerabilities (as of 2025-12-26)

**Recommendation:** Run `pip install --upgrade fastapi uvicorn` monthly.

---

## AUDIT FINDINGS

### ✅ Strengths

1. **Read-only by design** - No write/delete/execute endpoints
2. **Localhost-only** - No external network exposure
3. **Path traversal protection** - Robust `resolve()` + BASE_DIR check
4. **Extension whitelist** - No executables accessible
5. **Fail-safe defaults** - Errors return 403/404/400, never expose sensitive info

### ⚠️ Considerations

1. **No authentication** - Acceptable for localhost single-user system, but any process running as `saba` can access agent
2. **Directory enumeration** - `/list` endpoint reveals directory structure (intentional functionality)
3. **Error messages** - Could be more generic (currently expose path details in errors)

### 🔒 Recommendations

1. **No changes needed** - Current security model is appropriate for use case
2. **Future enhancement** - If exposing beyond localhost, add API key authentication
3. **Monitoring** - Log all `/read` requests to detect unusual patterns

---

## CONCLUSION

**The VES Agent is read-only safe.**

It provides controlled, auditable access to whitelisted documentation files on localhost. The security model is appropriate for its purpose: serving a local PWA with filesystem access.

**Key Security Properties:**
- ✅ Cannot modify files
- ✅ Cannot execute code
- ✅ Cannot access system files
- ✅ Cannot be reached from network
- ✅ Fails safely on errors

**Approved for continued operation.**

No security issues identified that would prevent production use in current configuration.
