from aiogram import types

help_message = """Это бот-расписание для БЛИ № 3
Команды для бота-расписания:
♦️ /schedule - узнать расписание
♦️ /days - расписание по дням
♦️ /tomorrow - узнать расписание на завтра
♦️ /week - узнать текущую идею
♦️ /time - узнать расписание звонков
Чтобы узнать расписание у любого класса в любой день требуется написать следующее: 6A н пн, где 6A - класс (англ), н - неделя (н/ч), пн - день

Команды для трекер-бота:
♦️ /add - добавить новую запись
♦️ /my_olimps - получить свои записи в трекере
♦️ /get_treker - получение всех данных (требуется пароль)

Общие:
♦️ /newsletter - уведомления"""


async def get_help(message: types.Message):
    await message.answer(help_message)
