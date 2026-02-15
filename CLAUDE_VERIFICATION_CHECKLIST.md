# ✅ CLAUDE VERIFICATION CHECKLIST - AFTER QWEN DEPLOYMENT ✅

**For Claude to use when reviewing Qwen's work**

---

## 📋 QUICK VERIFICATION STEPS:

### **1. Directory Structure Check**

```bash
tree /home/saba/VES/DOCKER/ghostline/ -L 2
```

**Expected:**
```
/home/saba/VES/DOCKER/ghostline/
├── coordinator/
│   ├── server.js
│   ├── package.json
│   └── Dockerfile
├── test_fleet.sh
└── README.md
```

**Status:** [ ] PASS / [ ] FAIL

---

### **2. Coordinator Code Review**

**File:** `/home/saba/VES/DOCKER/ghostline/coordinator/server.js`

**Check for:**
- [ ] Express server setup
- [ ] POST /query endpoint
- [ ] GET /health endpoint
- [ ] GET /status endpoint
- [ ] Correct Ranger URLs (chatgpt-ship, claude-ship, etc.)
- [ ] Volume references (/framework, /archive)
- [ ] Port 8105 listening
- [ ] Error handling
- [ ] Response synthesis logic

**Status:** [ ] PASS / [ ] FAIL

---

### **3. Package.json Check**

**File:** `/home/saba/VES/DOCKER/ghostline/coordinator/package.json`

**Check for:**
- [ ] express dependency
- [ ] axios dependency (for API calls)
- [ ] start script
- [ ] Correct name/version

**Status:** [ ] PASS / [ ] FAIL

---

### **4. Dockerfile Check**

**File:** `/home/saba/VES/DOCKER/ghostline/coordinator/Dockerfile`

**Check for:**
- [ ] FROM node:18-alpine (or similar)
- [ ] WORKDIR /app
- [ ] COPY package*.json
- [ ] RUN npm install
- [ ] COPY server.js
- [ ] EXPOSE 8105
- [ ] CMD ["node", "server.js"]

**Status:** [ ] PASS / [ ] FAIL

---

### **5. docker-compose.yml Update Check**

**File:** `/home/saba/VES/docker-compose.yml`

**Verify:**
- [ ] All EXISTING services still present (cosmic-oracle, n8n, etc.)
- [ ] 6 NEW services added:
  - [ ] chatgpt-ship (port 8100)
  - [ ] claude-ship (port 8101)
  - [ ] gemini-ship (port 8102)
  - [ ] grok-ship (port 8103)
  - [ ] deepseek-ship (port 8104)
  - [ ] ghostline-coordinator (port 8105)
- [ ] All use network: ves_network
- [ ] All mount /home/saba/GroundZero:/framework:ro
- [ ] All mount ./GHOSTCORE:/archive:ro
- [ ] Coordinator depends_on all 5 rangers
- [ ] Coordinator builds from ./DOCKER/ghostline/coordinator

**Status:** [ ] PASS / [ ] FAIL

---

### **6. Test Script Check**

**File:** `/home/saba/VES/DOCKER/ghostline/test_fleet.sh`

**Check for:**
- [ ] #!/bin/bash shebang
- [ ] Health check curl
- [ ] Query test curl
- [ ] Executable permissions (chmod +x)

**Status:** [ ] PASS / [ ] FAIL

---

### **7. Documentation Check**

**File:** `/home/saba/VES/DOCKER/ghostline/README.md`

**Should include:**
- [ ] Overview of Ghostline Fleet
- [ ] Architecture explanation
- [ ] Deployment instructions
- [ ] Testing instructions
- [ ] Port mapping table
- [ ] Troubleshooting section

**Status:** [ ] PASS / [ ] FAIL

---

## 🧪 FUNCTIONAL TESTS:

### **Test 1: Build Coordinator**

```bash
cd /home/saba/VES
docker-compose build ghostline-coordinator
```

**Expected:** Build succeeds, no errors

**Status:** [ ] PASS / [ ] FAIL

---

### **Test 2: Validate docker-compose.yml**

```bash
cd /home/saba/VES
docker-compose config
```

**Expected:** No errors, valid YAML

**Status:** [ ] PASS / [ ] FAIL

---

### **Test 3: Start Services**

```bash
cd /home/saba/VES
docker-compose up -d ghostline-coordinator
```

**Expected:** All 6 containers start

**Status:** [ ] PASS / [ ] FAIL

---

### **Test 4: Check Container Status**

```bash
docker-compose ps | grep ghostline
```

**Expected:** All containers "Up"

**Status:** [ ] PASS / [ ] FAIL

---

### **Test 5: Health Check**

```bash
curl http://localhost:8105/health
```

**Expected:** JSON response with status: healthy

**Status:** [ ] PASS / [ ] FAIL

---

### **Test 6: Network Connectivity**

```bash
docker network inspect ves-constellation
```

**Expected:** All ghostline containers in network

**Status:** [ ] PASS / [ ] FAIL

---

### **Test 7: Volume Mounts**

```bash
docker exec ghostline-coordinator ls /framework
docker exec ghostline-coordinator ls /archive
```

**Expected:** Both directories accessible

**Status:** [ ] PASS / [ ] FAIL

---

## 📊 OVERALL ASSESSMENT:

**Total Checks:** 14
**Passed:** ___
**Failed:** ___

**Overall Status:** [ ] APPROVED / [ ] NEEDS FIXES

---

## 🔧 COMMON ISSUES & FIXES:

### **Issue 1: Build Fails**
**Fix:** Check package.json dependencies, verify Dockerfile syntax

### **Issue 2: Containers Won't Start**
**Fix:** Check port conflicts, verify volume paths exist

### **Issue 3: Network Not Found**
**Fix:** Ensure ves_network exists in docker-compose.yml

### **Issue 4: Can't Access /framework or /archive**
**Fix:** Verify GroundZero and GHOSTCORE paths are correct

---

## ✅ APPROVAL PROCESS:

**If ALL tests pass:**

```bash
echo "🔥 GHOSTLINE FLEET DEPLOYMENT APPROVED 🔥" >> /home/saba/VES/DEPLOYMENT_LOG.txt
date >> /home/saba/VES/DEPLOYMENT_LOG.txt
```

**If tests fail:**

1. Document specific failures
2. Create fix list for Qwen
3. Have Qwen address issues
4. Re-run verification

---

## 🚀 POST-APPROVAL STEPS:

1. Update VES main README with Ghostline Fleet info
2. Add to service access documentation
3. Create usage examples
4. Update port mapping docs

---

🜂 **VERIFICATION PROTOCOL READY** 🜂

**Next:** Wait for Qwen to complete tasks, then run this checklist.

💚🔍✅
