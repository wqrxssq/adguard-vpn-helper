import asyncio
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

async def mark_used(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Usage: /mark_used email
    """
    repo = context.bot_data["repo"]
    user = update.effective_user
    args = context.args
    if len(args) < 1:
        await update.message.reply_text("Использование: /mark_used email")
        return
    email = args[0]
    ok = await asyncio.to_thread(repo.mark_used, user.id, email)
    if ok:
        await update.message.reply_text(f"Аккаунт {email} помечен как использованный.")
    else:
        await update.message.reply_text(f"Аккаунт {email} не найден.")

def mark_used_handler() -> CommandHandler:
    return CommandHandler('mark_used', mark_used)