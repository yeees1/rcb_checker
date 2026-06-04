from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message


router = Router()


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    await message.answer(
        f"Привет! Бот работает.\n\n"
        f"Твой chat_id: <code>{message.chat.id}</code>"
    )