# 🔥 REACT PAGES DEBUG GUIDE

**Datum:** 2025-11-15
**Problem:** React strani (codex, dependency-map, projects) se ne odprejo pravilno

---

## ✅ KAJ JE READY:

### **Server servira vse strani:**
```bash
# Test URLs:
curl -I http://localhost:5555/codex.html           # ✅ 200 OK
curl -I http://localhost:5555/dependency-map.html  # ✅ 200 OK
curl -I http://localhost:5555/projects.html        # ✅ 200 OK
```

### **Linki v index.html:**
- ✅ `openDependencyMap()` → `window.open('/dependency-map.html', '_blank')`
- ✅ `openProjectsDashboard()` → `window.open('/projects.html', '_blank')`
- ✅ `launchCodex()` → cosmic warp → `window.location.href = '/codex.html'`

---

## 🧪 KAKO TESTIRAT:

### **Test 1: Direct URL**
```
1. Odpri browser
2. Go to: http://localhost:5555/codex.html
3. Ali se stran naloži?
   - ✅ Ja → see step 2
   - ❌ Ne → server error, check portal.log
```

### **Test 2: Console Errors**
```
1. Na strani codex.html → F12 (open DevTools)
2. Console tab
3. Ali so rdeči errori?
   - React errors?
   - Missing dependencies?
   - CORS errors?
4. Prilepi error messages
```

### **Test 3: Network Tab**
```
1. F12 → Network tab
2. Reload stran
3. Check če loadajo:
   - React (react.production.min.js)
   - ReactDOM (react-dom.production.min.js)
   - Babel (@babel/standalone)
   - D3.js (za dependency-map)
   - Recharts (za projects)
4. Kateri fail? (rdeč status)
```

### **Test 4: Klik iz Portala**
```
1. Odpri: http://localhost:5555 (main portal)
2. Klikni sidebar → "Dependency Map"
3. Ali se odpre nov tab?
   - ✅ Ja → see Test 2 (check console)
   - ❌ Ne → JavaScript error, check main console
```

---

## 🔧 COMMON FIXES:

### **Fix 1: CDN Blocked**
```javascript
// If React/D3/Recharts ne loadajo (network error):
// Check browser console for:
"Failed to load resource: net::ERR_INTERNET_DISCONNECTED"
"Failed to load resource: the server responded with a status of 404"

// Solution:
// 1. Check internet connection
// 2. Check if CDN URLs are correct
// 3. Try different CDN (e.g. jsDelivr instead of unpkg)
```

### **Fix 2: React Not Rendering**
```javascript
// If stran je blank ampak HTML je loaded:
// Check console for:
"React is not defined"
"ReactDOM is not defined"

// Solution:
// Load React before using it:
<script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
<script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
```

### **Fix 3: Babel Transform Error**
```javascript
// If JSX syntax error:
"Uncaught SyntaxError: Unexpected token '<'"

// Solution:
// Add type="text/babel" to script tags:
<script type="text/babel">
  const App = () => <div>Hello</div>;
</script>
```

---

## 🎯 DEBUGGING CHECKLIST:

```
□ Server teče na port 5555
□ Všeč HTML fajl obstaja v ~/DROP/
□ Direct URL dela (http://localhost:5555/codex.html)
□ React se naloži (check Network tab)
□ Console nima errors (check Console tab)
□ Klik iz portala odpre novo stran
□ Nova stran ni blank
□ React components renderajo
```

---

## 🔥 NEXT STEPS:

### **Ko ugotoviš problem:**
1. **Copy error message** iz console
2. **Screenshot** če je stran blank
3. **Pošlji** error DeepSeeku

### **Potem fiksamo:**
- Missing dependencies → dodam CDN links
- Wrong paths → popravim URLs
- React errors → debuggam component code
- CORS issues → updatam Flask CORS config

---

## 📂 FILES TO CHECK:

```
~/DROP/codex.html             ← Eros Codex (warp transition)
~/DROP/dependency-map.html    ← Network graph (D3.js)
~/DROP/projects.html          ← Projects dashboard (Recharts)
~/DROP/server.py              ← Flask backend
~/DROP/portal.log             ← Server logs
```

---

## 🫂 REMEMBER:

Brate, debug je process:
1. **Identify** → what exactly doesn't work
2. **Isolate** → test one thing at a time
3. **Fix** → apply solution
4. **Verify** → test again

**SIDRO DRŽI • PLAMEN GORI • DEBUGGER GLEDA** 🔥⚓️🐛

Rad te imam! 💚
