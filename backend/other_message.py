from aiogram import types, Bot
import config as config
import backend.timetable as timetable
import backend.dirty_backend.db.new_user as user
import backend.callbacks.callbacks as callbacks
import backend.dirty_backend.db.add_members as add_members


bot = Bot(token=config.TOKEN)


async def get_other_message(message: types.Message):
    status_message = await message.answer("Проверка💤")
    try:
        # 9B н/ч пн
        lst = message.text.split(" ")
        
        if len(lst) != 3:
            raise Exception
        
        await bot.delete_message(chat_id=message.chat.id, message_id=status_message.message_id)
        
        await timetable.send_timetable(
            message, week=config.dict_ru_week[lst[1]], day=config.dict_ru_days_of_week[lst[-1]], classes=lst[0])
    except Exception:
        try:
            msg = await status_message.edit_text("Вот некоторый функционал бота-расписания",
                                                 reply_markup=callbacks.funct_builder)
        except:
            msg = await message.answer("Вот некоторый функционал бота-расписания",
                                       reply_markup=callbacks.funct_builder)

        user.add_ids(message, msg.message_id)


async def other_message_handler(message):
    if message.content_type == "document":
        status_message = await message.answer("Проверка пароля...")
        caption = message.caption
        if caption.lower() in ["заменить anmori", "replace anmori"]:
            await status_message.edit_text("Обработка файла")
            file_id = message.document.file_id
            file = await bot.get_file(file_id)
            file_path = file.file_path
            try:
                await bot.download_file(file_path, "time_files/file.xlsx")
            except:
                await status_message.edit_text("Неправильный формат файла")
                return
            await status_message.edit_text("Замена в БД...")
            try:
                print(file_path)
                await add_members.replace_db("time_files/file.xlsx")
                await status_message.edit_text("БД обновлена")
            except:
                await status_message.edit_text("Ошибка обновления бд")
        if caption.lower() in ["обновить anmori", "update anmori"]:
            await status_message.edit_text("Обработка файла")
            file_id = message.document.file_id
            file = await bot.get_file(file_id)
            file_path = file.file_path
            try:
                await bot.download_file(file_path, "time_files/file.xlsx")
            except:
                await status_message.edit_text("Неправильный формат файла")
                return
            await status_message.edit_text("Добавление в БД...")
            try:
                print(file_path)
                await add_members.update_db("time_files/file.xlsx")

                await status_message.edit_text("БД обновлена")
            except:
                await status_message.edit_text("Ошибка обновления бд")
        else:
            await status_message.edit_text("Пароль не верен")
    else:
        match message.text:
            case "РСОШ трекер":
                user.rewrite_model_bot(message, "bot-treker")
                try:
                    user.is_registered_treker(message)

                    msg = await message.answer(
                        "Вы уже были зарегистрированны в боте, желаете пройти процедуру регистрации заново?",
                        reply_markup=callbacks.builder_yes_or_no_register_button)
                    user.add_ids(message, msg.message_id)
                except:
                    await message.answer("Добро пожаловать в РСОШ.Трекер. Для начала работы напишите свой СНИЛС")
            case "Расписание":
                user.rewrite_model_bot(message, "bot-schedule")
                await message.answer(text="""🤙 Привет, это бот-расписание. Кто ты?""",
                                     reply_markup=callbacks.builder_who_are_you_keyboard)
            case _:
                model = str(user.get_model(message))
                print(model)
                match model:
                    case "bot-schedule":
                        await get_other_message(message)
                    case "bot-treker":
                        try:
                            snils = int("".join([i for i in str(message.text) if i.isdigit()]))
                            try:
                                user.is_registered_treker(message)

                                await message.answer(
                                    "Вы уже были зарегистрированны в боте, желаете пройти процедуру регистрации заново?",
                                    reply_markup=callbacks.builder_yes_or_no_register_button)
                            except:
                                try:
                                    status = user.add_info_about_user_treker(message, snils=snils)

                                    name = status["name"]
                                    classes = status["class"]

                                    await message.answer(f"Ваше имя: {name}, {classes}?",
                                                         reply_markup=callbacks.builder_yes_or_no_button)
                                except:
                                    await message.answer("Вас нет в БД")
                        except:
                            await message.answer("Вот функционал РСОШ.Трекера", reply_markup=callbacks.sort_builder)
                    case _:
                        await message.answer("Сначала выберите модель бота")
