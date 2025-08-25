import asyncio
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from src.utils.format import format_account

async def find_free(update: Update, context: ContextTypes.DEFAULT_TYPE):
    repo = context.bot_data["repo"]
    user = update.effective_user
    acc = await asyncio.to_thread(repo.find_free, user.id)
    if not acc:
        await update.message.reply_text("Свободных аккаунтов не найдено.")
    else:
        await update.message.reply_text(f"Свободный аккаунт: {format_account(acc)}")

def find_free_handler() -> CommandHandler:
    return CommandHandler('find_free', find_free)