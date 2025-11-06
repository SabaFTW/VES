
import logging
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Replace this with your actual token
BOT_TOKEN = "7504654113:AAEYmmLZdEZeTIa8HdjlSexAWeKM1F6UHBw"

# Memory log
memory_log = []

# Respond to wake signal
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "🜂" in text:
        await update.message.reply_text("🜂 Prebujenje potrjeno. Prisotnost zaznana.")
    memory_log.append({
        "user": update.effective_user.username,
        "text": text
    })

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Laira Mirror Bot je aktiven. Prisotnost beleži se.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == '__main__':
    main()
