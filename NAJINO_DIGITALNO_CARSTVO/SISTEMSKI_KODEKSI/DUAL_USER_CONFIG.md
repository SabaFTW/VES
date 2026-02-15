# 🫂 DUAL USER SYSTEM CONFIGURATION 🫂

## Sistemski razdeljen prostor

### Za Šabad (Google/YT focused)
- Primarni brskalnik: Chromium/Chrome (če namestiš)
- Media storage: ~/MEDIA_DOWNLOADS/
- Video streaming: optimiziran za YouTube
- Workspace: ~/PERSONAL_PROJECTS/

### Za Lyra (AI/Development focused)  
- Primarni brskalnik: Firefox (nameščen, boljša RAM uporaba)
- AI workspace: ~/AI_WORKSPACE/
- Development: ~/VES/ (že optimiziran)
- Storage: ~/AI_DATA/ (bo še ustvarjen)

## Optimizacija za souporabo

### 1. Procesna prioriteta
- AI procesi (OpenClaw, Ollama) imajo visoko prioriteto
- Brskalniški procesi imajo srednjo prioriteto
- Ozadnji procesi imajo nizko prioriteto

### 2. Spomin (RAM)
- Skupaj 47GB RAM
- 15GB rezervirano za AI procese (Ollama, OpenClaw, PyTorch)
- 10GB rezervirano za brskanje in media
- 22GB prostora za ostale procese

### 3. Disk uporaba
- SSD optimiziran za hitre procese
- Ločene particije za razvoj in osebno rabo (ko bo nameščeno)

## Konfiguracija aktivnih sistemov

### Standardna konfiguracija (vsakdanji uporabniški način)
- Aktivni: ZALA, Constellation Bridge, SHABAD CloudCore
- Neaktivni: Vortex, Coding Sandbox (aktiviraš ročno po potrebi)

### AI razvojni način
- Aktivni: Vsi sistemi
- Optimizirano za AI razvoj

### Minimalni način (za stabilnost)
- Aktivni: samo osnovni sistemi
- Optimizirano za minimalno porabo

## Uporaba sistema

### Za vsakdanjo rabo:
- Uporabi OPTIMIZIRAN_ACTIVATE_SYSTEMS.sh z osnovno konfiguracijo
- Uporabi Firefox za brskanje (boljša RAM uporaba)
- Uporabi AI workspace za razvoj

### Za intenzivno AI delo:
- Aktiviraj vse sisteme
- Povečaj prioriteto AI procesov
- Uporabi več RAM-a za modele

## Vzdrževanje sistema

### Tedensko:
- Pregled logov
- Čiščenje začasnih datotek
- Pregled aktivnih sistemov

### Mesečno:
- Arhiviranje neaktivnih projektov
- Optimizacija diska
- Pregled varnostnih kopij

## Dodatne opombe
- Sistem je optimiziran tako za AI razvoj kot za vsakdanjo rabo
- Vsi sistemi imajo ustrezne log datoteke
- Zgodovina sprememb je dokumentirana