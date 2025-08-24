import logging
from telegram.ext import ApplicationBuilder

from config import load_settings
from handlers.v1.hello.view import hello_handler
from handlers.v1.echo.view import echo_handler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    settings = load_settings()
    app = ApplicationBuilder().token(settings.telegram_token).build()

    app.add_handler(handler=hello_handler(), group=0)
    app.add_handler(handler=echo_handler(), group=0)

    app.run_polling()

if __name__ == '__main__':
    main()