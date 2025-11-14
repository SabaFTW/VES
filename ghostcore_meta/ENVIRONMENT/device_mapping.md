# DEVICE MAPPING — HARDWARE TOPOLOGY

**Version:** V2.0
**Last Updated:** 2025-11-14

---

## OVERVIEW

Device mapping defines **the physical hardware devices** that constitute the runtime environment for this system.

Each device has specific capabilities, use cases, and roles in the distributed architecture.

---

## DEVICE INVENTORY

### Device 1: iPhone 15 Pro
**Role:** Primary Runtime, Mobile Processing Hub

**Specifications:**
- **OS:** iOS 17+
- **Processor:** A17 Pro
- **RAM:** 8GB
- **Storage:** 256GB (or 512GB/1TB depending on model)
- **Connectivity:** 5G, WiFi 6E, Bluetooth 5.3

**Capabilities:**
- Always available (phone is always with user)
- Fast boot and resume
- Excellent battery life
- Native iOS apps (ChatGPT, Claude, Working Copy, etc.)
- Camera, microphone, sensors
- iCloud integration

**Use Cases:**
- Quick tasks on the go
- Voice input/dictation
- Mobile app access to AI agents
- Git commits via Working Copy
- Note-taking (Apple Notes, Obsidian)
- Communication (messages, email)
- Symbolic capture (photos, screenshots)

**Limitations:**
- Small screen (limited for coding)
- Touch keyboard (slower than physical)
- Limited terminal access (except via SSH apps)
- iOS app sandboxing

**Connection to System:**
- iCloud (file sync)
- Git (Working Copy app)
- AI agent apps (ChatGPT, Claude, Gemini apps)

---

### Device 2: Arch Linux Workstation
**Role:** Deep Processing, Development, Heavy Computation

**Specifications:**
- **OS:** Arch Linux (rolling release)
- **Processor:** High-performance CPU (details TBD)
- **RAM:** 16GB+ (assumed)
- **Storage:** SSD (size TBD)
- **Connectivity:** Ethernet/WiFi

**Capabilities:**
- Full Linux environment
- Command-line power tools
- IDEs and development tools
- Virtual machines/containers
- Long-running processes
- Heavy computation (compilation, data processing, etc.)
- Full terminal access

**Use Cases:**
- Software development
- Code compilation and testing
- Server/backend work
- Docker/containerization
- System administration
- Deep research and analysis
- CLI-based AI agent access (APIs, Claude Code, etc.)

**Limitations:**
- Not mobile (stationary workstation)
- Requires manual boot
- May not be always available

**Connection to System:**
- Git (native CLI)
- Cloud storage (rclone, Syncthing, etc.)
- AI agent APIs
- SSH access to other systems

---

### Device 3: Windows 11 PC
**Role:** Storage Node, Integration Hub, Compatibility Layer

**Specifications:**
- **OS:** Windows 11
- **Processor:** TBD
- **RAM:** TBD
- **Storage:** TBD
- **Connectivity:** WiFi/Ethernet

**Capabilities:**
- Windows-native applications
- Microsoft ecosystem integration (OneDrive, Office)
- Gaming/entertainment (secondary)
- WSL2 (Linux subsystem)
- Cross-platform compatibility testing

**Use Cases:**
- File storage and organization
- OneDrive sync
- Windows-specific software (if needed)
- WSL2 for Linux tools on Windows
- Backup/redundant storage

**Limitations:**
- Less used than iPhone or Arch
- Windows overhead and bloat
- May not be primary development environment

**Connection to System:**
- OneDrive (file sync)
- Git (native or WSL2)
- AI agent web apps

---

## DEVICE ROLES SUMMARY

| Device      | Role                  | Primary Use Cases                          |
|-------------|-----------------------|--------------------------------------------|
| iPhone 15   | Primary Runtime       | Mobile access, quick tasks, always-on      |
| Arch Linux  | Deep Processing       | Development, heavy computation, CLI power  |
| Windows 11  | Storage/Integration   | File sync, compatibility, backup           |

---

## DEVICE INTERCONNECTION

### Synchronization Matrix

| Data Type       | iPhone | Arch | Windows | Sync Method         |
|-----------------|--------|------|---------|---------------------|
| Git repos       | ✓      | ✓    | ✓       | Git push/pull       |
| Documents       | ✓      | ✓    | ✓       | iCloud, OneDrive    |
| Notes           | ✓      | ✓    | ✓       | iCloud, Obsidian    |
| Code files      | ✓      | ✓    | ✓       | Git                 |
| App data        | ✓      | —    | —       | iCloud (iOS only)   |
| Photos          | ✓      | ✓    | ✓       | iCloud Photos       |
| Logs            | ✓      | ✓    | ✓       | Git (this repo)     |

---

## DEVICE SELECTION PROTOCOL

### When to Use Each Device

**Use iPhone when:**
- You are mobile
- You need quick access
- Task is simple (messages, notes, quick AI query)
- Voice input is preferred
- You want to capture something visually (photo, screenshot)

**Use Arch Linux when:**
- You are doing development work
- Task requires CLI tools
- Task requires heavy computation
- Task requires multiple terminal windows
- You need full control and no sandboxing

**Use Windows 11 when:**
- You need Windows-specific software
- You are managing OneDrive files
- Task requires Windows compatibility testing
- Arch is unavailable and task is too complex for iPhone

---

## DEVICE STATE AWARENESS

**The kernel (ŠABAD) must always know:**
- Which device is currently active
- What tasks are suitable for current device
- How to sync state between devices

**Example:**
```
Kernel state: Currently on iPhone
Task: Implement complex algorithm
Decision: Defer to Arch Linux session (more suitable)
Action: Note task in log for Arch session
```

---

## DEVICE FAILURE HANDLING

### Scenario: Device Unavailable
**Example:** iPhone battery dead, Arch is offline

**Response:**
- Switch to available device
- Access via web if possible (AI agent web apps)
- Log unavailability
- Resume when device is back

### Scenario: Device Loss/Damage
**Example:** iPhone is lost or broken

**Response:**
- System state is NOT lost (externalized to git/cloud)
- Replace device
- Restore from backups (iCloud, git)
- Continue operation

**Resilience:**
Because state is external, device failure is inconvenient but not catastrophic.

---

## DEVICE LOGGING

**Device usage is logged:**
- Which device was used for which tasks
- Performance observations (e.g., "Arch compiles faster than WSL2")
- Sync issues (e.g., "OneDrive conflict on Windows")

**Log Location:** `LOGS/`

**Purpose:** Optimize device selection over time

---

**Maintained by:** ŠABAD (kernel)
**Used by:** All task routing and execution protocols
