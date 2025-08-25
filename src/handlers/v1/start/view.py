from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name or user.username or "там"
    await update.message.reply_text(f"Привет, {name}!\nЯ помощник по аккаунтам AdGuard VPN.\nКоманды: /add_mail, /info, /mark_used, /delete_mail, /find_free")

def start_handler() -> CommandHandler:
    return CommandHandler('start', start)