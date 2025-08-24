from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

def hello_handler() -> CommandHandler:
    return CommandHandler('hello', hello)