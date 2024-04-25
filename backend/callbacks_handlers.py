from aiogram import types, Bot
from aiogram.types.input_file import FSInputFile
from backend.command_schedule import get_week, schedule_time
from backend.command_schedule import send_tomorrow_schedule, send_schedule
import config as config
import backend.new as news
from backend.days import get_days_schedule
import backend.add_treker as add_tr
import backend.timetable as timetable
import backend.dirty_backend.translator as tr
import backend.dirty_backend.db.new_user as user
import backend.callbacks.callbacks as callbacks
from backend.dirty_backend.make_zip import zip_files

bot = Bot(token=config.TOKEN)


async def get_teacher_or_student(query: types.CallbackQuery, callback_data: callbacks.UserCallback):
    status_message = await query.message.answer("Обработка...")
    user.add_sub(query.message, callback_data.sub)

    # await status_message.edit_text("Роль учителя пока в разработке. Если хотит
    # е начать работу с ботом - выберите роль ученика :) by @Anrull")
    await status_message.edit_text("Выберите предмет", reply_markup=callbacks.builder_subjects_keyboards)
    await query.answer()


async def get_teacher(query: types.CallbackQuery, callback_data: callbacks.UserCallback):
    status_message = await query.message.answer("Обработка...")
    user.add_role(query.message, "teacher")

    # await status_message.edit_text("Роль учителя пока в разработке. Если хотите
    # начать работу с ботом - выберите роль ученика :) by @Anrull")
    await status_message.edit_text("Кто именно?", reply_markup=callbacks.builder_subjects_keyboards)
    await query.answer()


async def get_student(query: types.CallbackQuery, callback_data: callbacks.UserCallback):
    status_message = await query.message.answer("Обработка...")
    user.add_role(query.message, "student")
    
    await status_message.edit_text("Отлично! Теперь выберите класс:", reply_markup=callbacks.builder_classes_keyboards)
    await query.answer()
    

async def send_zip(query: types.CallbackQuery):
    status_message = await query.message.answer("Обработка запроса...")
    try:
        await status_message.edit_text("Создание zip... 📁")
        await zip_files()
    except:
        await status_message.edit_text("Ошибка в создании файла")

    try:
        await status_message.edit_text("Отправка файла 📨")
        await bot.send_document(query.from_user.id, FSInputFile("time_files/Files_by_Anloss.zip"))
        await status_message.edit_text("✅ Готово")
        await bot.delete_message(message_id=status_message.message_id, chat_id=query.message.chat.id)
    except:
        await query.message.answer("❌ Простите, не получилось отправить файлы. Напишите @Anrull")
    
    await query.answer()


async def get_add_sub(query: types.CallbackQuery, callback_data: callbacks.SubjectsCallback):
    """Выбор класса"""
    user.add_sub(query.message, callback_data.sub)
    await query.message.answer(f"Отлично, команда /help поможет разобраться в боте и его командах",
                               reply_markup=callbacks.funct_builder)
    await query.answer()


async def get_add_newsletter(query: types.CallbackQuery, callback_data: callbacks.AddNewsletter):
    status_mesage = await query.message.answer("Обработка...")
    user.add_newsletter(query.message.chat.id, str(int(callback_data.add)))
    await status_mesage.edit_text(
        "Принято, теперь вам {}будут приходить сообщения".format(config.dict_of_not[str(int(callback_data.add))]))
    await query.answer()


async def get_days_value(query: types.CallbackQuery, callback_data: callbacks.DaysCallback):
    role = user.get_role(query.message.chat.id)
    # print(query.message.from_user.id)
    # print(query.message.chat.id)
    
    if role == "student":
        await timetable.send_timetable(query.message, week=callback_data.week, day=callback_data.day)
    elif role == "teacher":
        await timetable.send_timetable_teacher(query.message, week=callback_data.week, day=callback_data.day)
    
    await query.answer()


async def get_language(query: types.CallbackQuery, callback_data: callbacks.LangCallback):
    user.add_settings(query.message, [[callback_data.lang]])
    if callback_data.lang != "ru":
        await query.message.answer(await tr.translate_text("Прекрасный выбор!", callback_data.lang))
    else:
        await query.message.answer("Прекрасный выбор")
    await query.answer()


async def get_send_random_value(query: types.CallbackQuery, callback_data: callbacks.ClassesCallback):
    """Выбор класса"""
    status_mssg = await query.message.answer('Ожидайте...\n☕ Завариваем кофе')
    
    # user(query.message)
    user.new_users(query.message)
    text_class = callback_data.classes
    user.add_class(message=query.message, text_class=text_class)
    
    await status_mssg.edit_text('Готово ✅')
    await status_mssg.edit_text(f'Принято, ученик {text_class} класса 📚\nКоманда /help поможет разобраться в боте')
    await query.answer()


async def sort_menu(query, callback_data):
    if callback_data.command not in ["0тфильтровать по олимпиаде", "Удалить по олимпиаде"]:
        await add_tr.delete_messages(query)

    match callback_data.command:
        case "Расписание звонков":
            await schedule_time(query.message)
        case "Просмотреть новости":
            await news.get_last_news(query.message)
        case "Посмотреть текущую неделю":
            await get_week(query.message)
        case "Заполнить форму":
            await add_tr.add_command(query.message)
        case "Получить все олимпиады":
            await add_tr.get_my_olimps(query.message)
        case "Просмотреть олимпиады":
            await query.message.answer('Выберите фильтр', reply_markup=callbacks.get_olimps_builder_keyboards)
        case "0тфильтровать по олимпиаде":
            step = config.olimp_list_step
            spif = callback_data.sub
            spif_min = 0 if spif - step < 0 else spif - step
            llp = len(callbacks.builder_get_olimps_keyboard.inline_keyboard)
            spif_max = llp - step if spif + step > llp - step else spif + step
            will = callbacks.builder_get_olimps_keyboard.model_copy()
            will.inline_keyboard = callbacks.builder_get_olimps_keyboard.inline_keyboard[spif:spif + step]
            will.inline_keyboard.insert(0, [
                callbacks.InlineKeyboardButton(text=config.olimp_list_left,
                                               callback_data=f'my:sort:{spif_min}:0тфильтровать по олимпиаде'),
                callbacks.InlineKeyboardButton(text=config.olimp_list_right,
                                               callback_data=f'my:sort:{spif_max}:0тфильтровать по олимпиаде')])
            if query.message.reply_markup.inline_keyboard[0][0].text == config.olimp_list_left:
                msg = await query.message.edit_reply_markup(reply_markup=will)
            else:
                msg = await query.message.answer("Выберите олимпиаду:", reply_markup=will)
        case "0тфильтровать по этапу":
            msg = await query.message.answer(
                text="Выберите этап олимпиады", reply_markup=callbacks.sort_builder_stage_keyboard)
        case "0тфильтровать по предмету":
            msg = await query.message.answer(
                "Выберите предмет", reply_markup=callbacks.sort_builder_subjects_keyboard
            )
        case "0тфильтровать по наставнику":
            msg = await query.message.answer(
                "Выберите наставника:", reply_markup=callbacks.builder_get_teacher_keyboard)
        case "Получить расписание":
            msg = await query.message.answer(
                "Выберите желаемое расписание", reply_markup=callbacks.funct_builder2
            )
        case "Выбрать роль":
            msg = await query.message.answer(
                """🤙 Привет, это бот-расписание. Кто ты?""",
                reply_markup=callbacks.builder_who_are_you_keyboard
            )
        case "За сегодня":
            await send_schedule(query.message)
        case "Завтра":
            await send_tomorrow_schedule(query.message)
        case "По дням":
            await get_days_schedule(query.message)
        case "Удалить олимпиаду":
            msg = await query.message.answer("Выберите желаемую опцию", reply_markup=callbacks.delete_menu)
        case "Удалить по этапу":
            msg = await query.message.answer("Выберите этап", reply_markup=callbacks.builder_delete_stage_keyboards)
        case "Удалить по предмету":
            msg = await query.message.answer("Выберите предмет",
                                             reply_markup=callbacks.builder_delete_subjects_for_treker)
        case "Удалить по олимпиаде":
            step = config.olimp_list_step
            spif = callback_data.sub
            spif_min = 0 if spif - step < 0 else spif - step
            llp = len(callbacks.builder_delete_olimps_keyboard.inline_keyboard)
            spif_max = llp - step if spif + step > llp - step else spif + step
            will = callbacks.builder_delete_olimps_keyboard.model_copy()
            will.inline_keyboard = callbacks.builder_delete_olimps_keyboard.inline_keyboard[spif:spif + step]
            will.inline_keyboard.insert(0, [
                callbacks.InlineKeyboardButton(text=config.olimp_list_left,
                                               callback_data=f'my:sort:{spif_min}:Удалить по олимпиаде'),
                callbacks.InlineKeyboardButton(text=config.olimp_list_right,
                                               callback_data=f'my:sort:{spif_max}:Удалить по олимпиаде')])
            if query.message.reply_markup.inline_keyboard[0][0].text == config.olimp_list_left:
                msg = await query.message.edit_reply_markup(reply_markup=will)
            else:
                msg = await query.message.answer("Выберите олимпиаду:", reply_markup=will)
        case "Удалить по наставнику":
            msg = await query.message.answer("Выберите наставника",
                                             reply_markup=callbacks.builder_delete_teacher_keyboard)
        case "Посмотреть все":
            await get_delete_olimps(query.message)
    try:
        user.add_ids(query.message, msg.message_id)
    except:
        pass
    await query.answer()


async def delete_olimps(message, members=None):
    if members is None:
        members = user.get_olimps_treker(message)
    msg = await message.answer("Обработка запроса...")
    await add_tr.send_delete_olimps(members, message, msg)


async def get_delete_olimps(message: types.Message):
    await delete_olimps(message)


async def delete_olimp_for_callbacks(query, callback_data):
    index = callback_data.index
    msg = await query.message.answer("Обработка...")
    match index:
        case 999:
            await msg.edit_text("Удаление олимпиады было отменено")
        case _:
            try:
                user.get_delete_olimps(query.message, index)
                await msg.edit_text("Запись была удалена")
            except:
                await msg.edit_text("Ошибка удаления...")