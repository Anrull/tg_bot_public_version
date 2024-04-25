from aiogram import types, Bot, utils
from aiogram.enums import ParseMode
from aiogram.types import FSInputFile
import backend.dirty_backend.db.new_user as user
import config as config
import os
from openpyxl import Workbook
import backend.callbacks.callbacks as callbacks

# olimp - int искать по list_olimps_full в БД

bot = Bot(config.TOKEN)

try:
    os.remove("Books/treker.xlsx")
except:
    pass


async def send_create_fullsheet(message, members, msg):
    file_name = f"time_files/{members[0].full_names}.xlsx"

    try:
        os.remove(file_name)
    except:
        pass

    list_olimps = [[member.teacher, member.subjects, member.olimps, member.stage] for member in members]

    workbook = Workbook()
    sheet = workbook.active
    sheet.append(["Teacher", "Subjects", "Olimps", "Stages"])

    for i in list_olimps:
        sheet.append(i)

    workbook.save(file_name)

    await bot.send_document(message.chat.id, FSInputFile(file_name))

    await bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)


async def get_user_data(members, msg, message, lst=None):
    print(lst)
    try:
        name = members[0].full_names
        classes = members[0].classes
    except:
        await msg.edit_text(
            "У вас нет олимпиад.\nЧтобы добавить олипиаду введите команду /add или нажмите на кнопку ниже",
            reply_markup=callbacks.builder_add_button
        )
        return

    text = f"""{name}, {classes}\n\n💬 Ваши олимпиады:\n"""

    if len(members) < 6:
        for member in members:
            text = text + "👨‍🏫 Наставник - {}\n📚 Предмет - {}\n🦾 Олимпиада - {}\n🪜 Этап - {}\n\n".format(
                member.teacher, member.subjects, member.olimps, member.stage)
        else:
            text = text + "✍️ Новая запись - /add"
            if not lst:
                await msg.edit_text(text, reply_markup=callbacks.builder_fullsheet_keyboards)
            else:
                user.add_filters(message, lst)
                await msg.edit_text(text, reply_markup=callbacks.builder_filter_fullsheet_keyboards)
    else:
        parts = []
        for member in members:
            if len(text) < 3072:
                pass
            else:
                parts.append(text)
                text = ""
            text = text + "👨‍🏫 Наставник - {}\n📚 Предмет - {}\n🦾 Олимпиада - {}\n🪜 Этап - {}\n\n".format(
                member.teacher, member.subjects, member.olimps, member.stage)
        parts.append(text)
        for part in parts:
            print(1)
            await message.answer(part)
        await msg.delete()
        if lst:
            user.add_filters(message, lst)
            await message.answer("✍️ Новая запись - /add", reply_markup=callbacks.builder_filter_fullsheet_keyboards)
        else:
            await message.answer("✍️ Новая запись - /add", reply_markup=callbacks.builder_fullsheet_keyboards)


async def add_command(message):
    msg = await message.answer("Выберите наставника", reply_markup=callbacks.builder_teacher_keyboards)
    user.add_ids(message, msg.message_id)
    user.add_new_treker_start(message)


async def get_add_command2(message: types.Message):
    await message.answer("Выберите олимпиаду", reply_markup=callbacks.builder_olimps_keyboards)


async def get_add_command1(message: types.Message):
    await add_command(message)


async def get_add_command3(message: types.Message):
    msg = await message.answer("Выберите предмет", reply_markup=callbacks.builder_subjects_for_treker)
    user.add_ids(message, msg.message_id)


async def get_add_command4(message: types.Message):
    msg = await message.answer("Этап олимпиады", reply_markup=callbacks.builder_stage_keyboards)
    user.add_ids(message, msg.message_id)


async def get_my_olimps(message: types.Message):
    msg = await message.answer("Обработка запроса...")
    try:
        olimps = user.get_olimps_treker(message)
        await get_user_data(olimps, msg, message)
    except Exception:
        await msg.edit_text("Не удалось обработать запрос...")


async def get_filter_my_olimps(message):
    print("start get_filter_my_olimps")
    msg = await message.answer("Обработка...")
    try:
        filters = user.get_filters(message)
        members = user.get_elem_treker(message, filters["name"], role=filters["role"])
        await send_create_fullsheet(message, members, msg)
    except:
        await msg.edit_text("Ошибка в отправке xlxs файла")


async def get_my_olimps_full(message):
    # user_id, file_name, list_olimps
    msg = await message.answer("Обработка...")
    try:
        members = user.get_olimps_treker(message)
        await send_create_fullsheet(message, members, msg)
    except:
        await msg.edit_text("Ошибка в отправке xlxs файла")


async def get_all_treker_xlsx(message: types.Message):
    password = message.text.replace('/get_treker ', '')

    status_message = await message.answer("Обработка запроса...")

    if password == "anmori":
        await send_sheet(message, status_message)
    else:
        await status_message.edit_text("Неправильный пароль")


async def send_sheet(message, status_message):
    await status_message.edit_text("Создание таблицы...")
    try:
        os.remove("Books/treker.xlsx")
    except:
        pass
    members = user.get_all_treker()
    file_name = "Books/treker.xlsx"

    list_olimps = [[member.date, member.full_names, member.teacher, member.subjects, member.olimps, member.stage]
                   for member in members]

    workbook = Workbook()
    sheet = workbook.active
    sheet.append(["Date", "Name", "Teacher", "Subjects", "Olimps", "Stages"])

    for i in list_olimps:
        sheet.append(i)

    workbook.save(file_name)

    await bot.send_document(message.chat.id, FSInputFile(file_name))

    await bot.delete_message(chat_id=message.chat.id, message_id=status_message.message_id)


async def get_elem_treker(query, members, *lst):
    msg = await query.message.answer("Обработка...")
    try:
        await delete_messages(query.message)

        await get_user_data(members, msg, query.message, lst)
    except:
        await msg.edit_text("Ошибка")


async def send_delete_olimps(members, message, msg):
    try:
        name = members[0].full_names
        classes = members[0].classes
    except:
        await msg.edit_text(
            "У вас нет олимпиад.\nЧтобы добавить олипиаду введите команду /add или нажмите на кнопку ниже",
            reply_markup=callbacks.builder_add_button
        )
        return

    text = f"""{name}, {classes}\n\n💬 Ваши олимпиады:\n"""

    parts = []
    parts_db = {}
    for i, member in enumerate(members):
        if len(text) < 3078:
            pass
        else:
            parts.append(text)
            text = ""
        text = text + "№ {}:\n👨‍🏫 Наставник - {}\n📚 Предмет - {}\n🦾 Олимпиада - {}\n🪜 Этап - {}\n\n".format(
            i, member.teacher, member.subjects, member.olimps, member.stage)
        parts_db[i] = {"teacher": member.teacher, "subjects": member.subjects,
                       "olimps": member.olimps, "stage": member.stage}
    parts.append(text)
    list_msg = []
    for part in parts:
        msg1 = await message.answer(part)
        list_msg.append(msg1.message_id)
    user.add_delete_olimps(message, parts_db)
    await msg.delete()
    msg = await message.answer("Выберите олимпиаду для удаления",
                               reply_markup=await callbacks.get_delete_olimps_buttons(len(parts_db)))
    list_msg.append(msg.message_id)
    user.add_ids(message, *list_msg)


async def delete_messages(query):
    try:
        last_ids = user.get_last_ids(query.message)
        for msg_id in last_ids:
            await bot.delete_message(
                chat_id=query.message.chat.id,
                message_id=msg_id
            )
    except:
        pass
