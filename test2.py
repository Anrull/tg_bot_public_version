import asyncio
import backend.dirty_backend.db.new_user as user
from aiogram import Bot
import sys
import asyncio
import os
import config
import logging
import datetime
from backend.send_logs import send_logs
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import backend.dirty_backend.date as date
import backend.dirty_backend.make_zip as make_zip
import backend.timetable as timetable
from aiogram.types import FSInputFile

print("program running")

logging.basicConfig(level=logging.INFO, filename="logs/py_log.log", filemode="a")

logging.debug("program running")


def delete_files():
    # Функция, которая удаляет все файлы в папке
    for file in os.listdir("images"):
        os.remove(os.path.join("images", file))

    logging.debug("files deleted")
    print("files deleted")
    

delete_files()


scheduler = AsyncIOScheduler()
bot = Bot(token=config.TOKEN)


async def send_logs_everyweek(id):
    try:
        await send_logs(id)
    except Exception as e:
        logging.debug(f"Чат с айди {id} не найден: {e}")


async def lesson_schedule(id):
    try:
        await bot.send_message(id, "У вас сегодня занятие с 6B")
    except:
        logging.debug(f"Чат с айди {id} не найден: {e}")


async def send_tomorrow_schedule(user_id: int):
    if int(user.get_info_about_person(user_id).newsletter):
        try:
            role = user.get_role(user_id)
            week = await date.get_week(datetime.datetime.now())
            if week:
                if role == "student":
                    await timetable.send_timetable_schedule(user_id, num=len(os.listdir("images")) + 1,
                                                            week=config.dict_ru_week[week], day=await date.day_tomorrow())
                elif role == "teacher":
                    await timetable.send_timetable_teacher_schedule(user_id, num=len(os.listdir("images")) + 1, week=config.dict_ru_week[week], day=await date.day_tomorrow())
                logging.debug(f"message has been sent: {user_id}")
        except Exception as e:
            logging.debug(f"Чат с айди {user_id} не найден: {e}")
    
    await asyncio.sleep(1)


async def process_user(user_id):
    await send_tomorrow_schedule(user_id)
    print(user_id)


async def process_admin_files(admin_id):
    await send_logs_everyweek(admin_id)


async def foo():
    tasks = [process_user(int(user_id.user_id)) for user_id in user.get_all()]
    await asyncio.gather(*tasks)


async def foo2():
    tasks = [process_admin_files(admin_id) for admin_id in [1705933876]]
    await asyncio.gather(*tasks)


async def foo3():
    tasks = [lesson_schedule(teacher_id) for teacher_id in [601560717]]
    await asyncio.gather(*tasks)


# scheduler.add_job(foo, 'cron', day_of_week=0, hour=11, minute=33)
for i in range(3):
    scheduler.add_job(foo, 'cron', day_of_week=i, hour=14, minute=0)
scheduler.add_job(foo, 'cron', day_of_week=4, hour=12, minute=0)
scheduler.add_job(foo, 'cron', day_of_week=6, hour=18, minute=0)
scheduler.add_job(foo2, 'cron', day_of_week=6, hour=10, minute=0)
scheduler.add_job(foo2, "cron", day_of_week=2, hour=4, minute=30)
# scheduler.add_job(foo, "cron", day_of_week=1, hour=16, minute=24)
scheduler.add_job(foo3, "cron", day_of_week=2, hour=6, minute=0)
scheduler.add_job(foo3, "cron", day_of_week=2, hour=7, minute=0)
# scheduler.add_job(foo3, "cron", day_of_week=2, hour=13, minute=30)


if __name__ == "__main__" or __name__ != "__main__":
    scheduler.start()
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

