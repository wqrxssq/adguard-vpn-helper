import logging
from telegram.ext import ApplicationBuilder, CommandHandler

from .config import load_settings

from .db.repository import Repository

from .handlers.v1.start.view import start_handler
from .handlers.v1.echo.view import echo_handler
from .handlers.v1.add_mail.view import add_mail_handler
from .handlers.v1.delete_mail.view import delete_mail_handler
from .handlers.v1.find_free.view import find_free_handler
from .handlers.v1.info.view import info_handler
from .handlers.v1.mark_used.view import mark_used_handler

from .scheduler.refresher import Refresher

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    settings = load_settings()

    repo = Repository(settings.database_url)

    app = ApplicationBuilder().token(settings.telegram_token).build()
    app.add_handlers({
        0: [start_handler(), echo_handler(), add_mail_handler(), 
            delete_mail_handler(), find_free_handler(), 
            info_handler(), mark_used_handler()]
    })

    refresher = Refresher(repo)

    # start refresher when launching app:
    refresher.start()

    # attach to app for graceful shutdown if wanted
    app.bot_data["repo"] = repo
    app.bot_data["refresher"] = refresher

    app.run_polling()

if __name__ == '__main__':
    main()