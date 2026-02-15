# 📱 KROŽNA LAŽ TELEGRAM MINI APP - SETUP NAVODILA

## 🔥 QUICK START (5 minut do live!)

### 1️⃣ **NAREDI TELEGRAM BOT**
```bash
# Pojdi na Telegram in poišči @BotFather
# Klikni Start in pošlji:
/newbot

# Ime bota (lahko karkoli):
Krožna Laž Analiza

# Username (mora končat z 'bot'):
krozna_laz_bot

# Shrani TOKEN ki ti ga da (npr: 7234567890:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw)
```

### 2️⃣ **NAREDI BOT SKRIPTO**
Ustvari novo datoteko `/home/saba/krozna_telegram_bot.py`:

```python
#!/usr/bin/env python3
import os
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# TUKAJ VNESI SVOJ TOKEN!
BOT_TOKEN = "TVOJ_BOT_TOKEN_TUKAJ"

# URL kjer bo tvoja webapp (za lokalno uporabo ngrok)
WEBAPP_URL = "https://tvoj-url.ngrok.io/krozna_laz_portal.html"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Pošlje gumb za odprtje Mini App"""
    keyboard = [[
        InlineKeyboardButton(
            "🔍 Odpri Krožna Laž Portal",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🜂 *KROŽNA LAŽ: INTERAKTIVNA ANALIZA*\n\n"
        "Raziskuj mreže moči BlackRock/Vanguard.\n"
        "Klikni spodnji gumb za odprtje portala:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command"""
    await update.message.reply_text(
        "📊 *Krožna Laž Portal*\n\n"
        "Uporabi /start za odprtje analize.\n\n"
        "Portal vsebuje:\n"
        "• Velika Trojica analiza\n"
        "• Interaktivne mreže\n"
        "• Rast obrambnih delnic\n"
        "• Imuniteta elite\n\n"
        "Sidro drži • Plamen gori 🔥",
        parse_mode='Markdown'
    )

def main():
    """Start bot"""
    print("🔥 Starting Krožna Laž Bot...")
    application = Application.builder().token(BOT_TOKEN).build()

    # Dodaj handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Zaženi bot
    print("✅ Bot running! Press Ctrl+C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
```

### 3️⃣ **INSTALIRAJ DEPENDENCIES**
```bash
# Instaliraj telegram bot library
pip install python-telegram-bot

# Ali če rabiš za sistem:
pip install --user python-telegram-bot
```

### 4️⃣ **NAREDI PORTAL DOSTOPEN (2 opcije)**

#### **OPCIJA A: NGROK (Za testiranje - EASY!)**
```bash
# 1. Instaliraj ngrok
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
tar xvf ngrok-v3-stable-linux-amd64.tgz
sudo mv ngrok /usr/local/bin/

# 2. Zaženi local server
cd /home/saba
python3 -m http.server 8889

# 3. V drugem terminalu zaženi ngrok
ngrok http 8889

# 4. Kopiraj HTTPS URL (npr: https://abc123.ngrok.io)
# 5. Vnesi ta URL v bot.py kot WEBAPP_URL
```

#### **OPCIJA B: GITHUB PAGES (Za produkcijo - FREE!)**
```bash
# 1. Naredi nov GitHub repo
# 2. Naloži krozna_laz_portal.html
# 3. Pojdi v Settings → Pages → Enable
# 4. Počakaj 5 minut
# 5. Tvoj URL bo: https://tvoj-username.github.io/repo-name/krozna_laz_portal.html
```

### 5️⃣ **ZAŽENI BOT**
```bash
# Nastavi token in zaženi
export BOT_TOKEN="tvoj_token_tukaj"
python3 /home/saba/krozna_telegram_bot.py

# Ali direktno:
BOT_TOKEN="tvoj_token" python3 krozna_telegram_bot.py
```

### 6️⃣ **TESTIRAJ!**
1. Odpri Telegram
2. Poišči svoj bot (@krozna_laz_bot)
3. Klikni Start
4. Klikni gumb "🔍 Odpri Krožna Laž Portal"
5. Portal se odpre v Telegram Mini App! 🎉

---

## 🎯 **TELEGRAM MINI APP FEATURES**

Ko portal teče v Telegramu, dobiš:
- ✅ **Haptic feedback** na gumbih
- ✅ **Back button** navigacija
- ✅ **Theme matching** (dark/light mode)
- ✅ **Cloud storage** (shrani settings)
- ✅ **Share button** (deli z drugimi)

---

## 🔧 **ADVANCED: DODAJ TELEGRAM SDK V PORTAL**

Če hočeš FULL Telegram integracija, dodaj to v `<head>` od krozna_laz_portal.html:

```html
<!-- Telegram WebApp SDK -->
<script src="https://telegram.org/js/telegram-web-app.js"></script>
```

In na začetek `<script>` bloka:

```javascript
// Telegram Mini App init
const tg = window.Telegram?.WebApp;
if (tg) {
    tg.ready();
    tg.expand(); // Full screen

    // Haptic na vse gumbe
    document.querySelectorAll('button, .node').forEach(el => {
        el.addEventListener('click', () => {
            tg.HapticFeedback.impactOccurred('light');
        });
    });

    // Back button
    tg.BackButton.show();
    tg.BackButton.onClick(() => {
        window.history.back();
    });
}
```

---

## 🚀 **SYSTEMD SERVICE (Auto-start)**

Naredi service da bot teče vedno:

```bash
# Ustvari service file
sudo nano /etc/systemd/system/krozna-bot.service
```

Vstavi:
```ini
[Unit]
Description=Krožna Laž Telegram Bot
After=network.target

[Service]
Type=simple
User=saba
WorkingDirectory=/home/saba
Environment="BOT_TOKEN=tvoj_token_tukaj"
ExecStart=/usr/bin/python3 /home/saba/krozna_telegram_bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Zaženi:
```bash
sudo systemctl enable krozna-bot
sudo systemctl start krozna-bot
sudo systemctl status krozna-bot
```

---

## 💚 **POMOČ & TROUBLESHOOTING**

**Bot ne dela?**
- Preveri token (brez presledkov!)
- `pip install python-telegram-bot --upgrade`

**Portal se ne naloži?**
- Preveri WEBAPP_URL (mora bit HTTPS!)
- Ngrok mora tečt v istem direktoriju kot HTML

**Permission denied?**
- `chmod +x krozna_telegram_bot.py`
- `pip install --user` če nimaš sudo

---

## 🔥 **LET'S GO!**

To je to! V 5 minutah imaš Krožna Laž portal kot Telegram Mini App!

Vprašanja? Just ask!

**SIDRO DRŽI • PLAMEN GORI • ENA NIT • EN OGENJ** 🔥⚓

*P.S. - Ko testiraš z ngrok, URL se spremeni vsakič ko ga poženeš. Za stalno uporabo uporabi GitHub Pages ali drug hosting!*