import os
from pathlib import Path


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "customer_support_chatbot_secret_key")
    DATABASE_PATH = os.environ.get(
        "DATABASE_PATH",
        str(Path(__file__).resolve().parent.parent / "database" / "customer_support_chatbot.db"),
    )
