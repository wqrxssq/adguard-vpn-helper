import asyncio
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from ....utils.format import format_account

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    repo = context.bot_data["repo"]
    user = update.effective_user
    accounts = await asyncio.to_thread(repo.list_accounts, user.id)
    if not accounts:
        await update.message.reply_text("У вас пока нет аккаунтов.")
        return
    lines = [ format_account(a) for a in accounts ]
    await update.message.reply_text("\n".join(lines))

def info_handler() -> CommandHandler:
    return CommandHandler('info', info)