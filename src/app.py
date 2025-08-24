import logging
from telegram.ext import ApplicationBuilder, CommandHandler

from .config import load_settings

from .db.repository import Repository

from .handlers.v1.hello.view import hello_handler
from .handlers.v1.echo.view import echo_handler

from .handlers.v1 import commands as cmd

from .scheduler.refresher import Refresher

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    settings = load_settings()

    repo = Repository(settings.database_url)
    cmd.set_repository(repo)

    app = ApplicationBuilder().token(settings.telegram_token).build()

    # register handlers
    app.add_handler(CommandHandler("start", cmd.start))
    app.add_handler(CommandHandler("add_mail", cmd.add_mail))
    app.add_handler(CommandHandler("info", cmd.info))
    app.add_handler(CommandHandler("mark_used", cmd.mark_used))
    app.add_handler(CommandHandler("delete_mail", cmd.delete_mail))
    app.add_handler(CommandHandler("find_free", cmd.find_free))

    app.add_handler(handler=hello_handler(), group=0)
    app.add_handler(handler=echo_handler(), group=0)

    # setup refresher
    refresher = Refresher(repo)

    # start refresher when launching app:
    refresher.start()

    # attach to app for graceful shutdown if wanted
    app.bot_data["repo"] = repo
    app.bot_data["refresher"] = refresher

    app.run_polling()

if __name__ == '__main__':
    main()