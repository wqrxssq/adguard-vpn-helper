import os
from dataclasses import dataclass

@dataclass
class Settings:
    telegram_token: str

def load_settings() -> Settings:
    token = os.environ.get("TOKEN")
    if not token:
        raise RuntimeError("TOKEN is not set in environment")
    return Settings(telegram_token=token)