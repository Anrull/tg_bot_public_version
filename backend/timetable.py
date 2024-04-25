from aiogram.types import FSInputFile
from aiogram import Bot

import backend.dirty_backend.schedule as schedule
import backend.dirty_backend.translator as tr
import backend.dirty_backend.db.new_user as User
import backend.dirty_backend.test3 as test3
import backend.dirty_backend.search as search
import ast
from config import TOKEN

weeks = {0: "чет", 1: "нечет"}
days = {0: "пн", 1: "вт", 2: "ср", 3: "чт", 4: "пт"}

bot = Bot(TOKEN)


async def send_timetable(message, day=0, week=1, classes=None):
    status_mssg = await message.answer("Проверка... ⌛")
    # User.new_users()
    result = User.check(message)
    if result:
        await status_mssg.edit_text("Подготовка расписания 🕑")

        try:
            try:
                await status_mssg.edit_text("Идет поиск расписания")
                
                if not classes:
                    list_schedule = await schedule.send_schedule_text(result, week=week, day=day)
                else:
                    list_schedule = await schedule.send_schedule_text(classes, week=week, day=day)
                lang = User.get_lang(message)
                lang = ast.literal_eval(lang)
                if lang[0][0] != "ru":
                    list_schedule = await tr.translate_list(list_schedule, lang[0][0])
            except:
                print("ошибка в генерации расписания")
                raise Exception

            await status_mssg.edit_text("Происходит подготовка изображения 🖼")

            try:
                if not classes:
                    data = f"{result}, нед: {weeks[int(week)]}, день: {days[int(day)]}, lang: {lang[0][0]}"
                else:
                    data = f"{classes}, нед: {weeks[int(week)]}, день: {days[int(day)]}, lang: {lang[0][0]}"
                # print(1)
                test3.draw_timetable(list_schedule, data)
            except Exception:
                print(list_schedule)
                print("ошибка в отрисовке расписания")
                raise Exception
            
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=status_mssg.message_id)
            except:
                print("ошибка в удалении сообщения")

            try:
                # photo = FSInputFile("images/output.png")
                photo = FSInputFile("images/schedule.png")

                await bot.send_photo(chat_id=message.chat.id, photo=photo)
            except:
                print("ошибка в отправке фотографии расписания")
                raise Exception
        except Exception:
            await status_mssg.edit_text("❌ Ошибка, напишите @Anrull для разбора полета")
    else:
        await status_mssg.edit_text("Извините, сначала надо указать класс 🔐")
        

async def send_timetable_teacher(message, day=0, week=1):
    status_mssg = await message.answer("Проверка... ⌛")
    User.new_users(message)
    sub = User.get_sub(message)
    if sub != "student":
        await status_mssg.edit_text("Подготовка расписания 🕑")

        try:
            try:
                await status_mssg.edit_text("Идет поиск расписания")
                # print(sub)
                list_schedule = await search.upgrate_search(sub, week, day)
                lang = User.get_lang(message)
                lang = ast.literal_eval(lang)
                if lang[0][0] != "ru":
                    list_schedule = await tr.translate_list(list_schedule, lang[0][0])
            except:
                print("ошибка в генерации расписания")
                raise Exception

            await status_mssg.edit_text("Происходит подготовка изображения 🖼")

            try:
                print(sub, day, week)
                data = f"{sub}, нед: {weeks[int(week)]}, день: {days[int(day)]}, lang: {lang[0][0]}"
                # print(data)
                test3.draw_timetable(list_schedule, data, teacher=True)
            except Exception:
                print(list_schedule)
                print("ошибка в отрисовке расписания")
                raise Exception
            
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=status_mssg.message_id)
            except:
                print("ошибка в удалении сообщения")

            try:
                # photo = FSInputFile("images/output.png")
                photo = FSInputFile("images/schedule.png")

                await bot.send_photo(chat_id=message.chat.id, photo=photo)
            except:
                print("ошибка в отправке фотографии расписания")
                raise Exception
        except Exception:
            await status_mssg.edit_text("❌ Ошибка, напишите @Anrull для разбора полета")
    else:
        await status_mssg.edit_text(
            "Извините, сначала надо пройти процедуру регистрации, и пожалуйста, не пропускайте некоторые пункты")


async def send_timetable_schedule(user_id, num=0, day=0, week=1, classes=None):
    # User.new_users()
    result = User.check_schedule(user_id)
    if result:
        try:
            try:                
                if not classes:
                    list_schedule = await schedule.send_schedule_text(result, week=week, day=day)
                else:
                    list_schedule = await schedule.send_schedule_text(classes, week=week, day=day)
                lang = User.get_lang(user_id=user_id)
                lang = ast.literal_eval(lang)
                if lang[0][0] != "ru":
                    list_schedule = await tr.translate_list(list_schedule, lang[0][0])
            except:
                print("ошибка в генерации расписания")
                raise Exception

            try:
                if not classes:
                    data = f"{result}, нед: {weeks[int(week)]}, день: {days[int(day)]}, lang: {lang[0][0]}"
                else:
                    data = f"{classes}, нед: {weeks[int(week)]}, день: {days[int(day)]}, lang: {lang[0][0]}"
                # print(1)
                test3.draw_timetable(list_schedule, data, num=num)
            except Exception:
                print(list_schedule)
                print("ошибка в отрисовке расписания")
                raise Exception
            try:
                # photo = FSInputFile("images/output.png")
                photo = FSInputFile(f"images/schedule{num}.png")

                await bot.send_photo(chat_id=user_id, photo=photo)
            except:
                print("ошибка в отправке фотографии расписания")
                raise Exception
            # # Выберите файл, который нужно удалить
            # file_path = f"images/schedule{num}.png"

            # # Удалите файл
            # os.remove(file_path)

            # # Проверьте, был ли файл успешно удален
            # if not os.path.exists(file_path):
            #     print("Файл был успешно удален.")
            # else:
            #     print("Не удалось удалить файл.")
        except Exception:
            pass


async def send_timetable_teacher_schedule(user_id, num=0, day=0, week=1):
    sub = User.get_sub(user_id=user_id)
    if sub != "student":
        try:
            try:
                # print(sub)
                list_schedule = await search.upgrate_search(sub, week, day)
                lang = User.get_lang(user_id=user_id)
                lang = ast.literal_eval(lang)
                if lang[0][0] != "ru":
                    list_schedule = await tr.translate_list(list_schedule, lang[0][0])
            except:
                print("ошибка в генерации расписания")
                raise Exception

            try:
                print(sub, day, week)
                data = f"{sub}, нед: {weeks[int(week)]}, день: {days[int(day)]}, lang: {lang[0][0]}"
                # print(data)
                test3.draw_timetable(list_schedule, data, num=num, teacher=True)
            except Exception:
                print(list_schedule)
                print("ошибка в отрисовке расписания")
                raise Exception

            try:
                # photo = FSInputFile("images/output.png")
                photo = FSInputFile(f"images/schedule{num}.png")

                await bot.send_photo(chat_id=user_id, photo=photo)
            except:
                print("ошибка в отправке фотографии расписания")
                raise Exception
            # # Выберите файл, который нужно удалить
            # file_path = f"images/schedule{num}.png"

            # # Удалите файл
            # os.remove(file_path)

            # # Проверьте, был ли файл успешно удален
            # if not os.path.exists(file_path):
            #     print("Файл был успешно удален.")
            # else:
            #     print("Не удалось удалить файл.")
        except Exception:
            pass
