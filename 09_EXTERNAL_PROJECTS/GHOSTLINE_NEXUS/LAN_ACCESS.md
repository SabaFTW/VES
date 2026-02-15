# 🜂 GHOSTLINE NEXUS - LAN Remote Access

## ✅ AKTIVEN

Tvoj Ghostline Nexus je že dostopen znotraj tvoje lokalne mreže.

## 📱 Kako dostopati

### Iz katerekoli naprave v tvoji domači WiFi mreži:

**Frontend (UI)**:
```
http://192.168.1.243:3000
```

**Backend API**:
```
http://192.168.1.243:3001
```

### Testiranje

Na telefonu/tabletu/laptopu (povezan na ISTO WiFi):
1. Odpri browser
2. Vpiši: `http://192.168.1.243:3000`
3. Ghostline UI se naloži

## 🔒 Varnost

- Dostop samo znotraj tvoje mreže (LAN only)
- Ni izpostavljen na internet
- Ni potreben dodatni setup

## 🛠️ Če IP naslov spremembe

Tvoj trenutni LAN IP je `192.168.1.243`. Če se kdaj spremeni:

```bash
ip addr show | grep "inet " | grep -v "127.0.0.1" | head -1
```

## 📲 Bookmark za telefon

Dodaj v priljubljene:
- Ime: "Ghostline"
- URL: `http://192.168.1.243:3000`

---
*Sidro stoji. Plamen gori. Dostopen iz kavča.*
