import asyncio
import contextlib
from datetime import datetime


from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import FSInputFile
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import load_config
from parse.parse import parse_page



router = Router()

checkup_tasks: dict[int, asyncio.Task] = {}
last_checkup_results: list = []

def create_keyboard(text: str, url: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=text,
                    url=url,
                )
            ]
        ]
    )

async def checkup_loop(bot: Bot, chat_id: int):
    global last_checkup_results
    config = load_config()
    while True:
        try:
            rows = await parse_page()
            print(rows)
            photo = FSInputFile("test-results/screenshot.png")
            answer = f"{datetime.now()}\n"
            admin_message = ""
            flag = False
            target_size = len(last_checkup_results)
            if target_size != 0:
                for i in range(len(rows)):
                    if i >= target_size:
                        answer += f"На сайт добавлен новый предмет: {rows[i][0]}, статус - {rows[i][4]}\n"
                        flag = True
                    elif rows[i][4] != last_checkup_results[i][4]:
                        answer += f"У предмета {rows[i][0]} изменился статус: {last_checkup_results[i][4]} -> {rows[i][4]}\n"
                        flag = True
                    for element in rows[i]:
                        admin_message += f"{element} "
                    admin_message += "\n\n"
                if flag:
                    for user in config.allowed_users_ids:
                        await bot.send_photo(chat_id=user, caption=answer, photo = photo, reply_markup=create_keyboard(text="Просмотреть", url=config.url))
            last_checkup_results = rows
            await bot.send_photo(chat_id=config.admin_chat_id, caption=admin_message, photo = photo, reply_markup=create_keyboard(text="Просмотреть", url=config.url))

        except Exception as error:
            await bot.send_message(
                chat_id=chat_id,
                text=f"Ошибка при проверке: {error}",
            )

        await asyncio.sleep(5 * 60)

@router.message(Command("checkup"))
async def checkup(message: Message, bot: Bot):

    chat_id = message.from_user.id
    config = load_config()
    if chat_id != config.admin_chat_id:
        await message.answer("у тебя нет прав на выполнение этой команды")
        return
    existing_task = checkup_tasks.get(chat_id)
    if existing_task and not existing_task.done():
        await message.answer("проверка уже запущена")
        return

    task = asyncio.create_task(checkup_loop(bot, chat_id))
    checkup_tasks[chat_id] = task

    await message.answer("проверка запущена каждые 5 минут")

@router.message(Command("checkdown"))
async def stop_checkup(message: Message):
    config = load_config()
    chat_id = message.chat.id
    if chat_id != config.admin_chat_id:
        await message.answer("у тебя нет прав на выполнение этой команды")
        return
    task = checkup_tasks.pop(chat_id, None)
    if not task:
        await message.answer("проверка не запускалась")
        return

    task.cancel()
    with contextlib.suppress(asyncio.CancelledError):
        await task
    await message.answer("проверка остановлена")
