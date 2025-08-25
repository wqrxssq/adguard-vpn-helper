import asyncio
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

async def add_mail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Usage:
      /add_mail email days_left
    """
    repo = context.bot_data["repo"]
    user = update.effective_user
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("Использование: /add_mail email days_left\nПример: /add_mail me@example.com 15")
        return
    email = args[0]
    try:
        days_left = int(args[1])
    except ValueError:
        await update.message.reply_text("days_left должен быть целым числом (например: 15)")
        return

    try:
        await asyncio.to_thread(repo.add_account, user.id, email, days_left)
        await update.message.reply_text(f"Добавлен аккаунт {email} — осталось {days_left} дней.")
    except Exception as e:
        await update.message.reply_text(f"Ошибка при добавлении: {e}")

def add_mail_handler() -> CommandHandler:
    return CommandHandler('add_mail', add_mail)