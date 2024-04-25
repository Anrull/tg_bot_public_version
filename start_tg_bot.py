from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import os
import sys
import asyncio

bot = Bot(token='6704500309:AAGEe1Q8GoO-dlrzt635ZyP_bCE0-1wOIr8')
dp = Dispatcher()


@dp.message(Command("start"))
async def get_hello_message(message: types.Message):
    await message.answer("Приветсвую тебя, Anmori")


@dp.message(Command("start_bot"))
async def run_main_bot(message: types.Message):
    try:
        os.system("python main.py")
    except:
        os.system("python3 main.py")
    await message.answer("Бот запущен")


@dp.message(Command("shutdown"))
async def shutdown(message: types.Message):
    await message.anwer("Done")
    sys.exit()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
