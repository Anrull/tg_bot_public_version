from aiogram import types
from aiogram.enums import ParseMode

from backend.dirty_backend.db.history.history import get_history
import asyncio


async def get_last_news(message: types.Message):
    print(1)
    olimps = await get_history()
    text = """<em><b>Последние добавленные олимпиады:</b></em>\n\n"""
    for elem in olimps:
        text = text + """<b>{}</b>, <em>{}</em>\n🦾 {}\n📚 {}\n🪜 {}\n👨‍🏫 {}\n\n\n""".format(
            elem["name"], elem["date"], elem["olimps"], elem["sub"], elem["stage"], elem["teacher"], elem["date"])

    await message.answer(text, parse_mode=ParseMode.HTML)
