import os
from dataclasses import dataclass

@dataclass
class Settings:
    telegram_token: str
    database_url: str

def load_settings() -> Settings:
    token = os.environ.get("TOKEN")
    if not token:
        raise RuntimeError("TOKEN is not set in environment")
    db = os.environ.get("DATABASE_URL", "sqlite:///./data.db")
    return Settings(telegram_token=token, database_url=db)
