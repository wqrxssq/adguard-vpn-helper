from ..db.models import Account

def format_account(acc: Account) -> str:
    return f"{acc.email} | start: {acc.date_start} | end: {acc.date_end} | used: {bool(acc.is_used)}"