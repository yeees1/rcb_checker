import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Config:
    bot_token: str
    admin_chat_id: int
    rc_name: str
    rc_surname: str
    rc_patronymic: str
    rc_id: int
    url: str
    allowed_users_ids: list[int]

def load_config() -> Config:
    bot_token = os.getenv("BOT_TOKEN")
    try:
        admin_chat_id = int(os.getenv("ADMIN_CHAT_ID"))
    except ValueError:
        raise ValueError("ADMIN_CHAT_ID must be an integer.")
    rc_name = os.getenv("RC_NAME")
    rc_surname = os.getenv("RC_SURNAME")
    rc_patronymic = os.getenv("RC_PATRONYMIC")
    try:
        rc_id = int(os.getenv("RC_ID"))
    except ValueError:
        raise ValueError("RC_ID must be an integer.")
    url = os.getenv("URL")
    try:
        allowed_users_ids = list(map(int, os.getenv("ALLOWED_USERS_IDS").split(','))) if os.getenv("ALLOWED_USERS_IDS") else None
    except ValueError:
        raise ValueError("ALLOWED_USERS_IDS must be a comma-separated list of integers.")
    if not allowed_users_ids:
        raise ValueError("ALLOWED_USERS_IDS is not set in the environment variables.")
    if not bot_token:
        raise ValueError("BOT_TOKEN is not set in the environment variables.")
    if not admin_chat_id:
        raise ValueError("ADMIN_CHAT_ID is not set in the environment variables.")
    if not rc_name:
        raise ValueError("RC_NAME is not set in the environment variables.")
    if not rc_surname:
        raise ValueError("RC_SURNAME is not set in the environment variables.")
    if not rc_patronymic:
        raise ValueError("RC_PATRONYMIC is not set in the environment variables.")
    if not id:
        raise ValueError("RC_ID is not set in the environment variables.")
    if not url:
        raise ValueError("URL is not set in the environment variables.")
    return Config(
        bot_token=bot_token,
        admin_chat_id=admin_chat_id,
        rc_name=rc_name,
        rc_surname=rc_surname,
        rc_patronymic=rc_patronymic,
        rc_id = rc_id,
        url=url,
        allowed_users_ids=allowed_users_ids,
    )