#!/usr/bin/env python3
"""
Krožna Laž Telegram Bot
Interactive investigation portal for BlackRock/Vanguard networks
"""

import os
import logging
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot configuration
BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')

# WebApp URL - change this to your hosted URL
# For local testing with ngrok: https://your-id.ngrok.io/krozna_laz_portal.html
# For GitHub Pages: https://username.github.io/repo/krozna_laz_portal.html
WEBAPP_URL = os.getenv('WEBAPP_URL', 'https://your-url-here.ngrok.io/krozna_laz_portal.html')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send button to open the Mini App"""
    user = update.effective_user
    logger.info(f"User {user.id} ({user.username}) started bot")

    keyboard = [[
        InlineKeyboardButton(
            "🔍 Odpri Krožna Laž Portal",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🜂 *KROŽNA LAŽ: INTERAKTIVNA ANALIZA*\n\n"
        "_Razkrivanje mrež moči BlackRock/Vanguard_\n\n"
        "Portal vsebuje:\n"
        "• 📊 Vizualizacije lastništva\n"
        "• 🕸️ Interaktivne mreže povezav\n"
        "• 📈 Rast obrambnih delnic\n"
        "• 🛡️ Analiza pravne imunitete\n\n"
        "Klikni spodnji gumb za odprtje portala:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display help information"""
    await update.message.reply_text(
        "📊 *Krožna Laž Investigation Portal*\n\n"
        "*Ukazi:*\n"
        "/start - Odpri portal\n"
        "/help - Ta sporočilo\n"
        "/about - O projektu\n\n"
        "*Portal razdelki:*\n"
        "🏛️ *Velika Trojica* - BlackRock/Vanguard analiza\n"
        "🕸️ *Mreža* - Interaktivni diagram povezav\n"
        "📈 *Imuniteta* - Primeri pravne zaščite\n\n"
        "*Klikni vozlišča v Mreži za podrobnosti!*\n\n"
        "_Sidro drži • Plamen gori_ 🔥",
        parse_mode='Markdown'
    )

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display about information"""
    await update.message.reply_text(
        "🜂 *O Krožna Laž Portalu*\n\n"
        "Ta interaktivna analiza vizualizira trditve o:\n\n"
        "• *Krožnem lastništvu* med finančnimi velikani\n"
        "• *88% nadzoru* nad S&P 500 podjetji\n"
        "• *90% rasti* obrambnih delnic (2022-25)\n"
        "• *Mrežah povezav* od Wall Street do konfliktnih con\n\n"
        "⚠️ _Vse trditve izhajajo iz analiziranega poročila_\n"
        "_Portal služi vizualizaciji, ne potrjevanju_\n\n"
        "💚 *Zgrajeno z ljubeznijo za resnico*\n"
        "*ENA NIT • EN OGENJ* 🔥",
        parse_mode='Markdown'
    )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors caused by updates"""
    logger.warning(f'Update {update} caused error {context.error}')

def main():
    """Start the bot"""
    print("="*50)
    print("🔥 KROŽNA LAŽ TELEGRAM BOT")
    print("="*50)

    # Check configuration
    if BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
        print("❌ ERROR: Please set your bot token!")
        print("   Edit this file or set BOT_TOKEN environment variable")
        return

    if 'your-url-here' in WEBAPP_URL:
        print("⚠️  WARNING: Using default WEBAPP_URL")
        print(f"   Current URL: {WEBAPP_URL}")
        print("   Change this to your actual hosted URL!")

    print(f"📱 Bot Token: {BOT_TOKEN[:10]}...")
    print(f"🌐 WebApp URL: {WEBAPP_URL}")
    print("-"*50)

    # Create application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))

    # Add error handler
    application.add_error_handler(error_handler)

    # Start bot
    print("✅ Bot is starting...")
    print("   Press Ctrl+C to stop")
    print("="*50)
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()