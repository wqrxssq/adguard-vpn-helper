import asyncio
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

async def delete_mail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Usage: /delete_mail email
    """
    repo = context.bot_data["repo"]
    user = update.effective_user
    args = context.args
    if len(args) < 1:
        await update.message.reply_text("Использование: /delete_mail email")
        return
    email = args[0]
    ok = await asyncio.to_thread(repo.delete_account, user.id, email)
    if ok:
        await update.message.reply_text(f"Аккаунт {email} удалён.")
    else:
        await update.message.reply_text(f"Аккаунт {email} не найден.")

def delete_mail_handler() -> CommandHandler:
    return CommandHandler('delete_mail', delete_mail)