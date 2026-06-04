import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import load_config
from bot.handlers.start import router as start_router
from bot.handlers.check import router as checkup_router



async def main() -> None:
    logging.basicConfig(level=logging.INFO)

    config = load_config()

    bot = Bot(
        token=config.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher()
    dp.include_router(start_router)
    dp.include_router(checkup_router)


    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())