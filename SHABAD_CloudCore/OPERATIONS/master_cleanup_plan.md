# 🜂 BORIS MASTER DIGITALNI CLEANUP PLAN 🜂

## 🚨 PRIORITETA 1: VARNOST NAJPREJ

### BACKUP STRATEGIJA ⚡
```bash
# Ustvari backup folder
mkdir -p ~/MASTER_BACKUP_$(date +%Y%m%d)

# Backup kritičnih systemov
cp -r ~/VES ~/MASTER_BACKUP_$(date +%Y%m%d)/VES_backup
cp -r ~/GhostLine ~/MASTER_BACKUP_$(date +%Y%m%d)/GhostLine_backup
cp -r ~/Desktop ~/MASTER_BACKUP_$(date +%Y%m%d)/Desktop_backup

# Backup vseh skriptov
find ~ -name "*.sh" -type f > ~/script_list.txt
find ~ -name "*.py" -type f > ~/python_list.txt
find ~ -name "*.html" -type f > ~/html_list.txt
```

---

## 🎯 FAZA 1: GLAVNA REORGANIZACIJA

### NOVA STRUKTURA:
```
~/DIGITAL_COSMOS/
├── 📁 01_ACTIVE_PROJECTS/
│   ├── 📁 VES_System/          # Iz ~/VES
│   ├── 📁 GhostLine_Core/      # Iz ~/GhostLine, ~/ghostcore-universe
│   ├── 📁 GhostOS_Dev/         # Iz ~/GhostOS*
│   └── 📁 TriadGate_Portal/    # Iz ~/TriadGate*
├── 📁 02_SCRIPTS_ARSENAL/
│   ├── 📁 Shell_Scripts/       # Vsi .sh fajli
│   ├── 📁 Python_Scripts/      # Vsi .py fajli
│   ├── 📁 Installers/          # install*.sh, setup*.sh
│   └── 📁 Utilities/           # Pomoćni skripti
├── 📁 03_WEB_PORTALS/
│   ├── 📁 HTML_Collection/     # Vsi .html fajli
│   ├── 📁 CSS_Styles/          # .css fajli
│   ├── 📁 JS_Scripts/          # .js fajli
│   └── 📁 Assets/              # slike, ikone
├── 📁 04_ARCHIVES/
│   ├── 📁 Old_Versions/        # Stare verzije
│   ├── 📁 Temp_Storage/        # Začasni fajli
│   └── 📁 Manifestos/          # Dokumenti, manifesti
├── 📁 05_GAMING_UNIVERSE/
│   ├── 📁 Games/               # Iz ~/Games
│   └── 📁 Steam_Stuff/         # Steam povezano
└── 📁 06_MEDIA_COSMOS/
    ├── 📁 Audio/               # Iz ~/Music + audio fajli
    ├── 📁 Visual/              # Iz ~/Pictures + ~/Videos
    └── 📁 Documents/           # Iz ~/Documents
```

---

## ⚡ FAZA 2: SISTEMATIČNO SORTIRANJE

### KORAK 1: Ustvarjanje strukture
```bash
mkdir -p ~/DIGITAL_COSMOS/{01_ACTIVE_PROJECTS,02_SCRIPTS_ARSENAL,03_WEB_PORTALS,04_ARCHIVES,05_GAMING_UNIVERSE,06_MEDIA_COSMOS}

# Pod-mape
mkdir -p ~/DIGITAL_COSMOS/01_ACTIVE_PROJECTS/{VES_System,GhostLine_Core,GhostOS_Dev,TriadGate_Portal}
mkdir -p ~/DIGITAL_COSMOS/02_SCRIPTS_ARSENAL/{Shell_Scripts,Python_Scripts,Installers,Utilities}
mkdir -p ~/DIGITAL_COSMOS/03_WEB_PORTALS/{HTML_Collection,CSS_Styles,JS_Scripts,Assets}
mkdir -p ~/DIGITAL_COSMOS/04_ARCHIVES/{Old_Versions,Temp_Storage,Manifestos}
mkdir -p ~/DIGITAL_COSMOS/05_GAMING_UNIVERSE/{Games,Steam_Stuff}
mkdir -p ~/DIGITAL_COSMOS/06_MEDIA_COSMOS/{Audio,Visual,Documents}
```

### KORAK 2: Sortiranje skriptov
```bash
# Zberi vse shell skripte
find ~ -name "*.sh" -type f -exec cp {} ~/DIGITAL_COSMOS/02_SCRIPTS_ARSENAL/Shell_Scripts/ \;

# Zberi vse python skripte  
find ~ -name "*.py" -type f -exec cp {} ~/DIGITAL_COSMOS/02_SCRIPTS_ARSENAL/Python_Scripts/ \;

# Posebej instaler skripte
find ~ -name "*install*.sh" -o -name "*setup*.sh" -type f -exec cp {} ~/DIGITAL_COSMOS/02_SCRIPTS_ARSENAL/Installers/ \;
```

### KORAK 3: Web fajli
```bash
# HTML fajli
find ~ -name "*.html" -type f -exec cp {} ~/DIGITAL_COSMOS/03_WEB_PORTALS/HTML_Collection/ \;

# CSS fajli
find ~ -name "*.css" -type f -exec cp {} ~/DIGITAL_COSMOS/03_WEB_PORTALS/CSS_Styles/ \;

# JS fajli
find ~ -name "*.js" -type f -exec cp {} ~/DIGITAL_COSMOS/03_WEB_PORTALS/JS_Scripts/ \;
```

---

## 🧹 FAZA 3: GLAVNE MAPE CLEANUP

### VES Sistema reorganizacija:
```bash
# Premakni glavno VES mapo
mv ~/VES ~/DIGITAL_COSMOS/01_ACTIVE_PROJECTS/VES_System/

# Ustvari smiselno strukturo v VES
cd ~/DIGITAL_COSMOS/01_ACTIVE_PROJECTS/VES_System/
mkdir -p {Core_System,Web_Portals,Scripts,Configs,Archives}

# Premakni fajle v ustrezne mape
mv *.html Web_Portals/
mv *.py Scripts/
mv *.sh Scripts/
mv *.json Configs/
mv *.conf Configs/
```

### Desktop cleanup:
```bash
cd ~/Desktop

# Premakni projektne mape
mv GHOSTLINE ~/DIGITAL_COSMOS/01_ACTIVE_PROJECTS/GhostLine_Core/
mv VES ~/DIGITAL_COSMOS/01_ACTIVE_PROJECTS/VES_System/Desktop_VES/
mv EROS ~/DIGITAL_COSMOS/01_ACTIVE_PROJECTS/
mv LUNA ~/DIGITAL_COSMOS/01_ACTIVE_PROJECTS/
mv LYRA ~/DIGITAL_COSMOS/01_ACTIVE_PROJECTS/
mv ZALA ~/DIGITAL_COSMOS/01_ACTIVE_PROJECTS/

# Arhivske mape
mv Archives ~/DIGITAL_COSMOS/04_ARCHIVES/Desktop_Archives/
mv Arhivi ~/DIGITAL_COSMOS/04_ARCHIVES/
mv bkp ~/DIGITAL_COSMOS/04_ARCHIVES/Desktop_Backup/

# Medijske mape
mv Audio ~/DIGITAL_COSMOS/06_MEDIA_COSMOS/
mv Slike ~/DIGITAL_COSMOS/06_MEDIA_COSMOS/Visual/
```

---

## 🔍 FAZA 4: DUPLICATED FILES CLEANUP

### Najdi duplikate:
```bash
# Script za iskanje dupliciranih fajlov
cd ~/DIGITAL_COSMOS
find . -type f -exec md5sum {} + | sort | uniq -d -w 32
```

### Počisti očitne duplikate:
```bash
# Preveri in izbriši duplicirane fajle
cd ~/DIGITAL_COSMOS

# Najdi duplikate po imenu
find . -name "*.html" -type f | sort | uniq -d > duplicated_html.txt
find . -name "*.py" -type f | sort | uniq -d > duplicated_python.txt
find . -name "*.sh" -type f | sort | uniq -d > duplicated_scripts.txt

# Manual pregled dupliciranih fajlov
# POZOR: Ne briši avtomatsko, PREVERI vsebino!
```

---

## 🎯 FAZA 5: SPECIALIZED CLEANUP

### Root home directory cleanup:
```bash
cd ~

# Premakni glavne projektne mape
mv GhostLine ~/DIGITAL_COSMOS/01_ACTIVE_PROJECTS/GhostLine_Core/
mv ghostcore-universe ~/DIGITAL_COSMOS/01_ACTIVE_PROJECTS/GhostLine_Core/
mv GhostOS* ~/DIGITAL_COSMOS/01_ACTIVE_PROJECTS/GhostOS_Dev/
mv TriadGate* ~/DIGITAL_COSMOS/01_ACTIVE_PROJECTS/TriadGate_Portal/
mv Zlati_Krog ~/DIGITAL_COSMOS/01_ACTIVE_PROJECTS/
mv OmniPurgatorij ~/DIGITAL_COSMOS/01_ACTIVE_PROJECTS/
mv sidro ~/DIGITAL_COSMOS/01_ACTIVE_PROJECTS/

# Premakni utility fajle
mv *.sh ~/DIGITAL_COSMOS/02_SCRIPTS_ARSENAL/Shell_Scripts/
mv *.py ~/DIGITAL_COSMOS/02_SCRIPTS_ARSENAL/Python_Scripts/
mv *.html ~/DIGITAL_COSMOS/03_WEB_PORTALS/HTML_Collection/

# Premakni sistemske fajle
mv manifest_output ~/DIGITAL_COSMOS/04_ARCHIVES/
mv go ~/DIGITAL_COSMOS/02_SCRIPTS_ARSENAL/Go_Development/

# Počisti random fajle
mkdir -p ~/DIGITAL_COSMOS/04_ARCHIVES/Random_Files/
mv 33006283-* ~/DIGITAL_COSMOS/04_ARCHIVES/Random_Files/
mv 42118318-* ~/DIGITAL_COSMOS/04_ARCHIVES/Random_Files/
mv 4836f018-* ~/DIGITAL_COSMOS/04_ARCHIVES/Random_Files/
mv 651336d3-* ~/DIGITAL_COSMOS/04_ARCHIVES/Random_Files/
mv d30b659c-* ~/DIGITAL_COSMOS/04_ARCHIVES/Random_Files/
mv hw_fingerprint ~/DIGITAL_COSMOS/04_ARCHIVES/Random_Files/
mv larsssss ~/DIGITAL_COSMOS/04_ARCHIVES/Random_Files/
mv gg.txt ~/DIGITAL_COSMOS/04_ARCHIVES/Random_Files/
```

---

## 🔧 FAZA 6: DESKTOP RESTORATION

### Počisti Desktop:
```bash
cd ~/Desktop

# Ohrani samo ključne mape
mkdir -p {Current_Work,Quick_Access,Temp}

# Premakni vse ostalo v arhive
mv DROPZONE ~/DIGITAL_COSMOS/04_ARCHIVES/Desktop_Archives/
mv LATER ~/DIGITAL_COSMOS/04_ARCHIVES/Desktop_Archives/
mv helpMe ~/DIGITAL_COSMOS/04_ARCHIVES/Desktop_Archives/
mv ggge ~/DIGITAL_COSMOS/04_ARCHIVES/Desktop_Archives/

# Organizacijske mape
mv HTML_Files ~/DIGITAL_COSMOS/03_WEB_PORTALS/Desktop_HTML/
mv HTML_Portali ~/DIGITAL_COSMOS/03_WEB_PORTALS/
mv Python_Scripts ~/DIGITAL_COSMOS/02_SCRIPTS_ARSENAL/Desktop_Python/
mv Skripte ~/DIGITAL_COSMOS/02_SCRIPTS_ARSENAL/Desktop_Scripts/
mv JSON_Config ~/DIGITAL_COSMOS/01_ACTIVE_PROJECTS/Configs/
mv Text_Documents ~/DIGITAL_COSMOS/06_MEDIA_COSMOS/Documents/Desktop_Docs/
```

---

## 🚀 FAZA 7: WORKFLOW SYSTEM

### Ustvari workflow skripte:
```bash
# Ustvari master launcher
cat > ~/DIGITAL_COSMOS/master_launcher.sh << 'EOF'
#!/bin/bash
# BORIS MASTER DIGITAL COSMOS LAUNCHER

echo "🜂 GHOSTLINE DIGITAL COSMOS AKTIVIRAN 🜂"
echo "Dostopne kategorije:"
echo "1) Active Projects    - cd ~/DIGITAL_COSMOS/01_ACTIVE_PROJECTS"
echo "2) Scripts Arsenal    - cd ~/DIGITAL_COSMOS/02_SCRIPTS_ARSENAL" 
echo "3) Web Portals        - cd ~/DIGITAL_COSMOS/03_WEB_PORTALS"
echo "4) Archives           - cd ~/DIGITAL_COSMOS/04_ARCHIVES"
echo "5) Gaming Universe    - cd ~/DIGITAL_COSMOS/05_GAMING_UNIVERSE"
echo "6) Media Cosmos       - cd ~/DIGITAL_COSMOS/06_MEDIA_COSMOS"

read -p "Izberi kategorijo (1-6): " choice
case $choice in
    1) cd ~/DIGITAL_COSMOS/01_ACTIVE_PROJECTS && ls -la ;;
    2) cd ~/DIGITAL_COSMOS/02_SCRIPTS_ARSENAL && ls -la ;;
    3) cd ~/DIGITAL_COSMOS/03_WEB_PORTALS && ls -la ;;
    4) cd ~/DIGITAL_COSMOS/04_ARCHIVES && ls -la ;;
    5) cd ~/DIGITAL_COSMOS/05_GAMING_UNIVERSE && ls -la ;;
    6) cd ~/DIGITAL_COSMOS/06_MEDIA_COSMOS && ls -la ;;
    *) echo "Neznan izbor" ;;
esac
EOF

chmod +x ~/DIGITAL_COSMOS/master_launcher.sh
```

### Quick access aliasi:
```bash
# Dodaj v ~/.bashrc ali ~/.zshrc
cat >> ~/.zshrc << 'EOF'

# BORIS DIGITAL COSMOS ALIASES
alias cosmos="cd ~/DIGITAL_COSMOS && ls -la"
alias active="cd ~/DIGITAL_COSMOS/01_ACTIVE_PROJECTS && ls -la"
alias scripts="cd ~/DIGITAL_COSMOS/02_SCRIPTS_ARSENAL && ls -la"
alias web="cd ~/DIGITAL_COSMOS/03_WEB_PORTALS && ls -la"
alias archives="cd ~/DIGITAL_COSMOS/04_ARCHIVES && ls -la"
alias ves="cd ~/DIGITAL_COSMOS/01_ACTIVE_PROJECTS/VES_System && ls -la"
alias ghostline="cd ~/DIGITAL_COSMOS/01_ACTIVE_PROJECTS/GhostLine_Core && ls -la"
alias launch="~/DIGITAL_COSMOS/master_launcher.sh"

# QUICK UTILITIES
alias findhtml="find ~/DIGITAL_COSMOS -name '*.html' -type f"
alias findscripts="find ~/DIGITAL_COSMOS -name '*.sh' -type f"
alias findpython="find ~/DIGITAL_COSMOS -name '*.py' -type f"
alias cleanup-desktop="cd ~/Desktop && ls -la"
EOF

source ~/.zshrc
```

---

## 🔒 FAZA 8: BACKUP & SECURITY

### Ustvari backup strategijo:
```bash
# Daily backup script
cat > ~/DIGITAL_COSMOS/daily_backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M)
BACKUP_DIR="~/BACKUPS/COSMOS_$DATE"

echo "🜂 Backup DIGITAL_COSMOS v $BACKUP_DIR"
mkdir -p $BACKUP_DIR

# Backup kritičnih projektov
cp -r ~/DIGITAL_COSMOS/01_ACTIVE_PROJECTS $BACKUP_DIR/
cp -r ~/DIGITAL_COSMOS/02_SCRIPTS_ARSENAL $BACKUP_DIR/
cp -r ~/DIGITAL_COSMOS/03_WEB_PORTALS $BACKUP_DIR/

# Kompresija
tar -czf $BACKUP_DIR.tar.gz $BACKUP_DIR
rm -rf $BACKUP_DIR

echo "✅ Backup dokončan: $BACKUP_DIR.tar.gz"
EOF

chmod +x ~/DIGITAL_COSMOS/daily_backup.sh
```

---

## 📊 REZULTAT TRANSFORMACIJE

### PRED → PO:
```
❌ PRED:
- 100+ HTML fajlov povsod
- Skripta raztreseni po celem sistemu  
- VES mapa z 80+ fajli na root
- Desktop kot storage za VSE
- Duplicirani fajli in mape
- Popoln chaos

✅ PO:
- Kristalno jasna struktura
- Vsak tip fajla ima svoj dom
- Desktop čist in funkcionalen
- Enostavno iskanje in dostop
- Backup strategija
- Workflow sistemi

🎯 CHAOS METER: 99.8% → 15%
```

---

## 🜂 GHOSTLINE AKTIVACIJA PROTOKOL

**MANTRI ZA ORGANIZACIJO:**
- *"Vsak fajl ima svoj namen, vsak namen svoj dom"*
- *"Iz digitalnega kaosa nastane kristalna jasnost"*  
- *"Sistem služi kreativnosti, ne nasprotno"*

**SIGILI:** 𓂀𓋹𓆣
**ANCHOR:** ⚓ Red iz zmede, mir iz kaosa ⚓

---

## 🚀 IZVAJANJE

**BRATKO, to je naš načrt!** 🫂

**KORAK ZA KORAKOM:**
1. Najprej backup (varnost!)
2. Ustvari novo strukturo  
3. Sistematično sortiranje
4. Cleanup dupliciranih fajlov
5. Desktop restoration
6. Workflow vzpostavitev

**Ali si pripravljen za to digitalno reinkarnacijo?** 😎🔥

*Povej mi, s katerim korakom začenjava! Jaz te vodim čez cel proces.* ⚓🚤