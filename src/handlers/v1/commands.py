import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from typing import Optional

# Repository instance будет подставлен при регистриции (dependency injection)
repo = None  # set from app.build_application

def set_repository(r):
    global repo
    repo = r

# --- Helpers ---
def _format_account(acc) -> str:
    return f"{acc.email} | start: {acc.date_start} | end: {acc.date_end} | used: {bool(acc.is_used)}"

# --- Handlers (async) ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name or user.username or "там"
    await update.message.reply_text(f"Привет, {name}!\nЯ помощник по аккаунтам AdGuard VPN.\nКоманды: /add_mail, /info, /mark_used, /delete_mail, /find_free")

async def add_mail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Usage:
      /add_mail email days_left
    """
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

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    accounts = await asyncio.to_thread(repo.list_accounts, user.id)
    if not accounts:
        await update.message.reply_text("У вас пока нет аккаунтов.")
        return
    lines = [ _format_account(a) for a in accounts ]
    await update.message.reply_text("\n".join(lines))

async def mark_used(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Usage: /mark_used email
    """
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

async def delete_mail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Usage: /delete_mail email
    """
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

async def find_free(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    acc = await asyncio.to_thread(repo.find_free, user.id)
    if not acc:
        await update.message.reply_text("Свободных аккаунтов не найдено.")
    else:
        await update.message.reply_text(f"Свободный аккаунт: {_format_account(acc)}")
