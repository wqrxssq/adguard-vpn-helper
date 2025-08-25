import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from telegram import User, Message, Update

from src.handlers.v1.start.view import start
from src.handlers.v1.echo.view import echo
from src.handlers.v1.add_mail.view import add_mail
from src.handlers.v1.delete_mail.view import delete_mail
from src.handlers.v1.find_free.view import find_free
from src.handlers.v1.info.view import info
from src.handlers.v1.mark_used.view import mark_used

@pytest.mark.asyncio
async def test_start_handler():
    mock_message = MagicMock(spec=Message)
    mock_message.reply_text = AsyncMock()
    mock_user = MagicMock(spec=User)
    mock_user.first_name = "Иван"
    mock_user.id = 10
    mock_update = MagicMock(spec=Update)
    mock_update.effective_user = mock_user
    mock_update.message = mock_message

    await start(mock_update, MagicMock())
    mock_message.reply_text.assert_awaited()

@pytest.mark.asyncio
async def test_add_mail_calls_repo():
    # dummy repo
    class DummyRepo:
        def add_account(self, user_id, email, days_left):
            self.called = (user_id, email, days_left)

    dummy = DummyRepo()

    # подготовка update/context
    mock_message = MagicMock()
    mock_message.reply_text = AsyncMock()

    mock_user = MagicMock()
    mock_user.id = 42

    mock_update = MagicMock()
    mock_update.effective_user = mock_user
    mock_update.message = mock_message

    ctx = MagicMock()
    ctx.bot_data = {"repo": dummy}   # <- вот сюда кладём repo
    ctx.args = ["t@e.com", "12"]

    await add_mail(mock_update, ctx)

    mock_message.reply_text.assert_awaited()
    assert getattr(dummy, "called") == (42, "t@e.com", 12)

