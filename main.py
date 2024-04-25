from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
import asyncio
import tracemalloc
from aiogram.types import CallbackQuery
import config
import logging
import backend.new as news
import backend.callbacks.callbacks as callbacks
import backend.dirty_backend.db.new_user as user
import backend.dirty_backend.db.add_members as add_members
from backend.dirty_backend.timer import Timer
from backend.send_logs import send_logs
import backend.start as start
import backend.add_treker as add_tr
from backend.helppy import get_help
from backend.callbacks_handlers import get_teacher_or_student, get_teacher, get_student, get_language, get_days_value
from backend.callbacks_handlers import send_zip, get_add_sub, get_add_newsletter, get_send_random_value, sort_menu
from backend.other_message import other_message_handler
from backend.command_schedule import send_tomorrow_schedule, send_schedule, get_week, schedule_time
from backend.days import get_days_schedule
from backend.admin import get_admin
import backend.admin as admin_commands
from backend.newsletter import get_newsletter
from backend.settings import choice_lang
import backend.timetable as timetable
import backend.callbacks_handlers as callbacks_hand

# олимпиады -> как вывести

print("main program running")

logging.basicConfig(level=logging.INFO, filename="logs/py_log_bot.log", filemode="a")

bot = Bot(token=config.TOKEN)
dp = Dispatcher()


@dp.message.register(start.get_start_work, Command("start"))
@dp.message.register(get_week, Command("week"))
@dp.message.register(schedule_time, Command("time"))
@dp.message.register(news.get_last_news, Command("news"))
@dp.message.register(add_tr.get_add_command1, Command("add"))
@dp.message.register(add_tr.get_all_treker_xlsx, Command("get_treker"))
@dp.message.register(add_tr.get_my_olimps, Command("my_olimps"))
@dp.message.register(callbacks_hand.get_delete_olimps, Command("delete_olimps"))
@dp.message.register(get_help, Command("help"))
@dp.message.register(get_days_schedule, Command("days"))
@dp.message.register(get_admin, Command("admin"))
@dp.message.register(admin_commands.get_admin_shutdown, Command("shutdown"))
@dp.message.register(choice_lang, Command("language"))
@dp.message.register(get_newsletter, Command("newsletter"))
@dp.message.register(admin_commands.send_newsletter, Command("send"))
@dp.message.register(send_schedule, Command("schedule"))
@dp.message.register(send_tomorrow_schedule, Command("tomorrow"))
@dp.callback_query(callbacks.OtherCallbacks.filter(F.foo == "fullsheet"))
async def choice_bot(query: types.CallbackQuery, callback_data: callbacks.OtherCallbacks):
    match callback_data.other:
        case "user":
            await add_tr.get_my_olimps_full(query.message)
        case "filter":
            await add_tr.get_filter_my_olimps(query.message)
        case "delete":
            msg = await query.message.answer("Выберите желаемую опцию", reply_markup=callbacks.delete_menu)
            user.add_ids(query.message, msg.message_id)
    await query.answer()


@dp.callback_query(callbacks.ChoiceRoleBotCallbacks.filter(F.foo == "choicebot"))
async def choice_bot(query: types.CallbackQuery, callback_data: callbacks.ChoiceRoleBotCallbacks):
    model = callback_data.model
    if model == "bot-treker":
        user.rewrite_model_bot(query.message, "bot-treker")
        await query.message.answer(
            "Добро пожаловать в РСОШ.Трекер. Для начала работы напишите свой СНИЛС, или напишите команду /help если "
            "уже были зарегистрированы"
        )
    elif model == "bot-schedule":
        user.rewrite_model_bot(query.message, "bot-schedule")
        await query.message.answer(text="""🤙 Привет, это бот-расписание. Кто ты?""",
                                   reply_markup=callbacks.builder_who_are_you_keyboard)
    await query.answer()


@dp.callback_query(callbacks.SortCallbacks.filter(F.foo == "sort"))
async def sort_func(query: types.CallbackQuery, callback_data: callbacks.SortCallbacks):
    await sort_menu(query, callback_data)


@dp.callback_query(callbacks.UserCallback.filter(F.foo == "add_olimp"))
async def teacher_or_student(query: types.CallbackQuery, callback_data: callbacks.UserCallback):
    await add_tr.add_command(query.message)
    await query.answer()


@dp.callback_query(callbacks.YesOrNoCallback.filter(F.foo == "choice"))
async def teacher_or_student(query: types.CallbackQuery, callback_data: callbacks.YesOrNoCallback):
    if callback_data.status:
        await query.message.answer(
            "Отлично! Вот некоторый функционал:", reply_markup=callbacks.sort_builder
        )
    else:
        await query.message.answer("Повторите процедуру регистрации заново введя свой СНИЛС (зеленая бумажка)")
    await query.answer()


@dp.callback_query(callbacks.YesOrNoCallback.filter(F.foo == "choice2"))
async def teacher_or_student(query: types.CallbackQuery, callback_data: callbacks.YesOrNoCallback):
    if callback_data.status:
        msg = await query.message.answer("Отправка")
        text = await user.new_add_treker(query.message)
        # if text == "":
        #     if olimps[3] not in ["Прошел регистрацию", "Написал отборочные этапы (волну, тур)"]:
        #         data = {"name": tr.name, "olimps": olimps[2],
        #                 "stage": olimps[3], "subjects": olimps[1], "teacher": olimps[0]}
        #         asyncio.run(add_history(data))
        await msg.edit_text(text)
    else:
        await query.message.answer("Хорошо, данные не были отправлены")

    await add_tr.delete_messages(query)
    await query.answer()


@dp.callback_query(callbacks.ClassesCallback.filter(F.foo == "choice"))
async def send_random_value(query: types.CallbackQuery, callback_data: callbacks.ClassesCallback):
    await get_send_random_value(query=query, callback_data=callback_data)


@dp.callback_query(callbacks.LangCallback.filter(F.foo == "language"))
async def send_random_value(query: types.CallbackQuery, callback_data: callbacks.LangCallback):
    await get_language(query=query, callback_data=callback_data)


@dp.callback_query(callbacks.DaysCallback.filter(F.foo == "days"))
async def send_random_value(query: types.CallbackQuery, callback_data: callbacks.DaysCallback):
    await get_days_value(query=query, callback_data=callback_data)


@dp.callback_query(callbacks.AddNewsletter.filter(F.foo == "newsletter"))
async def add_newsletter(query: types.CallbackQuery, callback_data: callbacks.AddNewsletter):
    await get_add_newsletter(query=query, callback_data=callback_data)


@dp.callback_query(callbacks.SubjectsCallback.filter(F.foo == "subjects"))
async def add_sub(query: types.CallbackQuery, callback_data: callbacks.SubjectsCallback):
    await get_add_sub(query=query, callback_data=callback_data)


@dp.callback_query(callbacks.AdminCallback.filter(F.foo == "admin" and F.all_files))
async def await_send_zip(query: types.CallbackQuery):
    await send_zip(query=query)


@dp.callback_query(callbacks.AdminCallback.filter(F.foo == "admin" and F.count_user))
async def send_count_users(query: types.CallbackQuery):
    await query.message.answer(f"На данный момент в боте - {user.get_user_count()} человек")
    await query.answer()


@dp.callback_query(callbacks.AdminCallback.filter(F.foo == "admin" and F.get_logs))
async def send_logfile(query: types.CallbackQuery):
    await send_logs(query.message.chat.id)
    await query.answer()


@dp.callback_query(callbacks.AdminCallback.filter(F.foo == "admin" and F.get_treker))
async def all_send_tomorrow_schedule(query: types.CallbackQuery):
    status_message = await query.message.answer("Обработка запроса...")

    await add_tr.send_sheet(query.message, status_message)

    await query.answer()


@dp.callback_query(callbacks.UserCallback.filter(F.foo == "student"))
async def teacher_or_student(query: types.CallbackQuery, callback_data: callbacks.UserCallback):
    await get_student(query=query, callback_data=callback_data)


@dp.callback_query(callbacks.UserCallback.filter(F.foo == "teacher"))
async def teacher_or_student(query: types.CallbackQuery, callback_data: callbacks.UserCallback):
    await get_teacher(query=query, callback_data=callback_data)


# < ------------------------------------------------------------------------- >
# < ------------------------------------------------------------------------- >


@dp.callback_query(callbacks.SubjectsCallback.filter(F.foo == "teacher"))
async def teacher_or_student(query: types.CallbackQuery, callback_data: callbacks.SubjectsCallback):
    await add_tr.delete_messages(query)
    teacher = config.list_teachers_for_treker[int(callback_data.sub)]
    match callback_data.smbd:
        case "add":
            try:
                print(config.list_teachers_for_treker[int(callback_data.sub)])
                user.add_olimps_elem_treker(query.message, teacher)
                msg1 = await query.message.answer("Учитель принят. Выберите теперь предмет",
                                                  reply_markup=callbacks.builder_subjects_for_treker)
                id1 = msg1.message_id
                user.add_ids(query.message, id1)
            except:
                await query.message.answer("Ошибка заполнения БД")
        case "get":
            try:
                members = user.get_elem_treker(query.message, teacher, role="teacher")
                print(members)
                await add_tr.get_elem_treker(query, members, teacher, "teacher")
            except:
                print("Error: teacher")
        case "delete":
            try:
                members = user.get_elem_treker(query.message, teacher, role="teacher")
                await callbacks_hand.delete_olimps(query.message, members)
            except:
                print("Error: delete teacher")
    await query.answer()


@dp.callback_query(callbacks.SubjectsCallback.filter(F.foo == "sub_olimp"))
async def teacher_or_student(query: types.CallbackQuery, callback_data: callbacks.SubjectsCallback):
    await add_tr.delete_messages(query)
    sub = config.list_subjects_for_button[
        int(callback_data.sub)] if "$" not in callback_data.sub else "ERROR: teacher_or_student: sub_olimp"
    match callback_data.smbd:
        case "add":
            step = config.olimp_list_step
            spif = 0  # стартовый индекс
            if "$" not in callback_data.sub:
                try:
                    user.add_olimps_elem_treker(query.message, sub)
                except:
                    await query.message.answer("Не удалось связаться с Базой данных")
            else:
                spif = int(callback_data.sub.lstrip("$"))
            spif_min = 0 if spif - step < 0 else spif - step
            llp = len(callbacks.builder_olimps_keyboard.inline_keyboard)
            spif_max = llp - step if spif + step > llp - step else spif + step
            will = callbacks.builder_olimps_keyboard.model_copy()
            will.inline_keyboard = callbacks.builder_olimps_keyboard.inline_keyboard[spif:spif + step]
            will.inline_keyboard.insert(
                0, [callbacks.InlineKeyboardButton(text=config.olimp_list_left,
                                                   callback_data=f'my:sub_olimp:${spif_min}:add'),
                    callbacks.InlineKeyboardButton(text=config.olimp_list_right,
                                                   callback_data=f'my:sub_olimp:${spif_max}:add')])
            msg1 = await query.message.answer("Предмет принят. Выберите теперь олимпиаду", reply_markup=will)
            id1 = msg1.message_id
            user.add_ids(query.message, id1)
        case "get":
            """
            вот тут
            """
            try:
                members = user.get_elem_treker(query.message, sub, role="sub")
                await add_tr.get_elem_treker(query, members, sub, "sub")
            except:
                print("Error: sub")
        case "delete":
            try:
                members = user.get_elem_treker(query.message, sub, role="sub")
                await callbacks_hand.delete_olimps(query.message, members)
            except:
                print("Error: delete sub")
    await query.answer()


@dp.callback_query(callbacks.OlimpsCallback.filter(F.foo == "olimp"))
async def teacher_or_student(query: types.CallbackQuery, callback_data: callbacks.OlimpsCallback):
    await add_tr.delete_messages(query)
    olimp = config.list_olimps_full[int(callback_data.olimp)]
    match callback_data.smbd:
        case "add":
            try:
                user.add_olimps_elem_treker(query.message, olimp)
                msg = await query.message.answer(
                    "Выберите этап олимпиады", reply_markup=callbacks.builder_stage_keyboards)
                user.add_ids(query.message, msg.message_id)
            except:
                await query.message.answer("Была ошибка")
        case "get":
            try:
                members = user.get_elem_treker(query.message, olimp, role="olimp")
                print(members)
                await add_tr.get_elem_treker(query, members, olimp, "olimp")
            except:
                print("Error: olimps")
        case "delete":
            try:
                members = user.get_elem_treker(query.message, olimp, role="olimp")
                await callbacks_hand.delete_olimps(query.message, members)
            except:
                print("Error: delete olimp")
    await query.answer()


@dp.callback_query(callbacks.OlimpsCallback.filter(F.foo == "stage"))
async def teacher_or_student(query: types.CallbackQuery, callback_data: callbacks.OlimpsCallback):
    await add_tr.delete_messages(query)
    stage = config.stages[int(callback_data.olimp)]
    match callback_data.smbd:
        case "add":
            try:
                user.add_olimps_elem_treker(query.message, stage)

                olimps = user.get_olimps(query.message)

                msg = await query.message.answer(
                    f"""Проверьте правильность своих данных:\n{olimps[0]}\n{olimps[1]}\n{olimps[2]}\n{olimps[3]}""",
                    reply_markup=callbacks.builder_yes_or_no_button2
                )

                user.add_ids(query.message, msg.message_id)
            except:
                await query.message.answer("Была ошибка")
        case "get":
            try:
                members = user.get_elem_treker(query.message, stage, role="stage")
                await add_tr.get_elem_treker(query, members, stage, "stage")
            except:
                print("Error: stage")
        case "delete":
            try:
                print(stage)
                members = user.get_elem_treker(query.message, stage, role="stage")
                await callbacks_hand.delete_olimps(query.message, members)
            except:
                print("Error: delete stage")
    await query.answer()


# < ------------------------------------------------------------------------- >
# < ------------------------------------------------------------------------- >


@dp.callback_query(callbacks.YesOrNoCallback.filter(F.foo == "reg_choice"))
async def reg_choice(query: CallbackQuery, callback_data: callbacks.YesOrNoCallback):
    match callback_data.status:
        case True:
            try:
                user.delete_user_treker(query.message)
                await query.message.answer("Для регистрации напишите свой СНИЛС (зеленая бумажка)")
            except:
                await query.message.answer("Ошибка удаления из БД")
        case False:
            await query.message.answer("Хорошо", reply_markup=callbacks.sort_builder)

    await add_tr.delete_messages(query)
    await query.answer()


@dp.callback_query(callbacks.DeleteCallback.filter(F.foo == "delete"))
async def delete_olimps_callback(query: CallbackQuery, callback_data: callbacks.DeleteCallback):
    await add_tr.delete_messages(query)
    await callbacks_hand.delete_olimp_for_callbacks(query, callback_data)


# < ------------------------------------------------------------------------- >
# < ------------------------------------------------------------------------- >


@dp.callback_query(callbacks.UserCallback.filter(F.foo == "subjects"))
async def teacher_or_student(query: types.CallbackQuery, callback_data: callbacks.UserCallback):
    await get_teacher_or_student(query=query, callback_data=callback_data)


@dp.message()
async def send_smbd(message: types.Message):
    await other_message_handler(message)


async def main():
    await dp.start_polling(bot)


timeC = Timer(10)
while config.running:
    if timeC.tk():
        try:
            tracemalloc.start()
            asyncio.run(main())
        except Exception as ex:
            print(ex)

# id - 1705933876
