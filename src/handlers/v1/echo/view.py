from telegram import Update
from telegram.ext import filters, MessageHandler, ContextTypes

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

def echo_handler() -> MessageHandler:
    return MessageHandler(filters.ALL & (~filters.COMMAND), echo)