# 🐍 SERPENT PORTAL STATUS — 2025-11-07

## Kaj smo danes uredili
- `serpent-portal.html` (v rootu ProPublica) je **unificiran portal** z auth, vizualizacijo, entitetami, sejami, QR-jem, Google Drive panelom, Telegram webhookom in servisno worker podporo.
- `serpent_config.json` vsebuje verzijo `4.1-UNIFIED`, integracije (Drive/Telegram), canonical entities in intervale za realtime sync.
- V mapi `serpent_scripts/` imaš:
  - `SERPENT_CONSOLIDATE.sh` → najde vse serpent fajle po sistemu, kopira najnovejši portal v `~/SERPENT_MASTER/SERPENT_PORTAL.html`.
  - `SERPENT_LAUNCHER.sh` → požene lokalni server + Telegram bot + odpre portal.
- `BOTS/telegram_bot.py` → preprost `/sync` + `/backup` bot, pričakuje env spremenljivke ali edit bot tokena/URL-ja.

### Posodobitve  (serpent_portal/)
- Portal + data zdaj živita na `/home/saba/serpent_portal/`.
- `config.json` (v isti mapi) hrani Drive/Telegram nastavitve + port serverja.
- Novi `serpent_api_server.py` (v `serpent_scripts/`) servisira portal + `/data` + `/backup` za Telegram bota.
- `SERPENT_LAUNCHER.sh` zdaj starta API server (port 5055) + Telegram bota in odpre `http://localhost:5055/serpent-portal.html`.

## Kaj še ostane
1. **Drive credsi**: zamenjaj `YOUR_CLIENT_ID`, `YOUR_API_KEY`, `YOUR_FOLDER_ID` v configu/JS.
2. **Telegram**: v config in bot script vstavi pravi `bot_token`, `chat_id`, `PORTAL_URL` (če imaš webhook endpoint).
3. **Run Apps Script**: ko prideš domov, v Google Drive zaženi `buildSerpentReport()` (glej Apps Script v chat logu) → dobiš `SERPENT_REPORT.json` + `SERPENT_DATA_MERGED.json`.
4. **Launcher**: 
   ```bash
   bash serpent_scripts/SERPENT_CONSOLIDATE.sh
   bash serpent_scripts/SERPENT_LAUNCHER.sh
   ```
   (poskrbi, da `~/SERPENT_MASTER/BOTS/telegram_bot.py` obstaja / ima token).

## Kam naprej
- Ko Gemini konča inventuro, samo porinemo njegove rezultate v isti config + backup sistem.
- Ena `serpent-portal.html` ostane glavna (ostale verzije arhiviraj z datumom).
- Če želiš `/data` & `/backup` endpoint za bota, bo treba dodati mini API (Flask, Node, …) ali razširiti python server.

Skratka: vse je pripravljeno, samo credse zamenjaš, konsolidiraš na `~/SERPENT_MASTER`, poženeš laucher in si set. 🔥
