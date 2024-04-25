from aiogram import types
import datetime
import config as config
import backend.timetable as timetable
from aiogram.enums import ParseMode
import backend.dirty_backend.date as date
import backend.dirty_backend.db.new_user as user


async def send_schedule(message: types.Message):
    role = user.get_role(message.chat.id)
    week = await date.get_week(datetime.datetime.now())
    if week:
        if role == "student":
            await timetable.send_timetable(message, week=config.dict_ru_week[week], day=await date.day_today())
        elif role == "teacher":
            await timetable.send_timetable_teacher(message, week=config.dict_ru_week[week], day=await date.day_today())
    else:
        await message.answer("Кажется, идут каникулы :)")
        

async def send_tomorrow_schedule(message: types.Message):
    role = user.get_role(message.chat.id)
    week = await date.get_next_week(datetime.datetime.now())
    if week:
        if role == "student":
            await timetable.send_timetable(message, week=config.dict_ru_week[week], day=await date.day_tomorrow())
        elif role == "teacher":
            await timetable.send_timetable_teacher(message, week=config.dict_ru_week[week], day=await date.day_tomorrow())
    else:
        await message.answer("Кажется, идут каникулы :)")


async def get_week(message: types.Message):
    week = await date.get_week(datetime.datetime.now(), flag=True)
    await message.answer("Текущая неделя - <b><em>{}</em></b>".format(config.dict_full_weeks[week]),
                         parse_mode=ParseMode.HTML)


async def schedule_time(message: types.Message):
    text = """<b>Расписание звонков</b> ⏰:

0️⃣ — <b><em>08.00 - 08.25</em></b>
1️⃣ — <b><em>08.30 - 09.10</em></b>
2️⃣ — <b><em>09.20 - 10.00</em></b>
3️⃣ — <b><em>10.20 - 11.00</em></b>
4️⃣ — <b><em>11.10 - 11.50</em></b>
5️⃣ — <b><em>12.00 - 12.40</em></b>
6️⃣ — <b><em>13.00 - 13.40</em></b>
7️⃣ — <b><em>14.00 - 14.40</em></b>
8️⃣ — <b><em>14.50 - 15.30</em></b>
    """

    await message.answer(text, parse_mode=ParseMode.HTML)