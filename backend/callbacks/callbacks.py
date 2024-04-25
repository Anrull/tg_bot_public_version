from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import list_classes, list_days, dict_days, list_olimps, list_olimps_full, list_teachers_for_treker
import config
import json


class SortCallbacks(CallbackData, prefix="my"):
    foo: str
    sub: int
    command: str


with open("dicts/teachers.json") as js:
    teachers = json.load(js)


class ClassesCallback(CallbackData, prefix="my"):
    foo: str
    classes: str


class DeleteCallback(CallbackData, prefix="my"):
    foo: str
    index: int


class OtherCallbacks(CallbackData, prefix="my"):
    foo: str
    other: str


class ChoiceRoleBotCallbacks(CallbackData, prefix="my"):
    foo: str
    model: str


class DaysCallback(CallbackData, prefix="my"):
    foo: str
    day: str
    week: str


class AdminCallback(CallbackData, prefix="my"):
    foo: str
    count_user: bool
    all_files: bool
    get_logs: bool
    get_treker: bool


class UserCallback(CallbackData, prefix="my"):
    foo: str


class SubjectsCallback(CallbackData, prefix="my"):
    foo: str
    sub: str
    smbd: str


class LangCallback(CallbackData, prefix="my"):
    foo: str
    lang: str


class AddNewsletter(CallbackData, prefix="my"):
    foo: str
    remove: bool
    add: bool


class YesOrNoCallback(CallbackData, prefix="my"):
    foo: str
    status: bool
    

class OlimpsCallback(CallbackData, prefix="my"):
    foo: str
    olimp: str
    smbd: str


sort_builder = InlineKeyboardBuilder()
for command in ["Заполнить форму", "Просмотреть новости", "Просмотреть олимпиады", "Удалить олимпиаду"]:
    sort_builder.button(text=f"{command}", callback_data=SortCallbacks(foo="sort", sub=0, command=f"{command}"))
sort_builder.adjust(1)
sort_builder = sort_builder.as_markup()


get_olimps_builder_keyboards = InlineKeyboardBuilder()
for command in ["Получить все олимпиады", "0тфильтровать по олимпиаде", "0тфильтровать по этапу",
                "0тфильтровать по предмету", "0тфильтровать по наставнику"]:
    get_olimps_builder_keyboards.button(text=f"{command}",
                                        callback_data=SortCallbacks(foo="sort", sub=0, command=f"{command}"))
get_olimps_builder_keyboards = get_olimps_builder_keyboards.adjust(1).as_markup()


# Создание кнопок меню для бота-расписания
funct_builder = InlineKeyboardBuilder()
for command in ["Получить расписание", "Выбрать роль", "Посмотреть текущую неделю"]:
    funct_builder.button(text=f"{command}", callback_data=SortCallbacks(foo="sort", sub=0, command=f"{command}"))
funct_builder = funct_builder.as_markup()


# Создание меню кнопок для удаления
delete_menu = InlineKeyboardBuilder()
for command in ["Посмотреть все", "Удалить по этапу", "Удалить по предмету",
                "Удалить по олимпиаде", "Удалить по наставнику"]:
    delete_menu.button(text=f"{command}", callback_data=SortCallbacks(foo="sort", sub=0, command=f"{command}"))
delete_menu = delete_menu.adjust(1).as_markup()


# Создание кнопок меню для бота-расписания
funct_builder2 = InlineKeyboardBuilder()
for command in ["За сегодня", "Завтра", "По дням"]:
    funct_builder2.button(text=f"{command}", callback_data=SortCallbacks(foo="sort", sub=0, command=f"{command}"))
funct_builder2 = funct_builder2.as_markup()


# Создание клавиатуры, для выбора класса
builder_classes_keyboards = InlineKeyboardBuilder()
for i in list_classes:
    builder_classes_keyboards.button(text=f"{i}", callback_data=ClassesCallback(foo="choice", classes=i))
builder_classes_keyboards.adjust(4, 4)
builder_classes_keyboards = builder_classes_keyboards.as_markup()


# Создание клавиатуры администратора
builder_admin_keyboards = InlineKeyboardBuilder()
builder_admin_keyboards.button(
    text="Получиить все файлы",
    callback_data=AdminCallback(foo="admin", count_user=False, all_files=True, get_logs=False, get_treker=False))
builder_admin_keyboards.button(
    text="Узнать кол-во юзеров",
    callback_data=AdminCallback(foo="admin", count_user=True, all_files=False, get_logs=False, get_treker=False))
builder_admin_keyboards.button(
    text="Получить логи",
    callback_data=AdminCallback(foo="admin", get_logs=True, count_user=False, all_files=False, get_treker=False))
builder_admin_keyboards.button(
    text="Получить таблицу-трекер",
    callback_data=AdminCallback(foo="admin", get_logs=False, count_user=False, all_files=False, get_treker=True))
builder_admin_keyboards.adjust(2, 2)
builder_admin_keyboards = builder_admin_keyboards.as_markup()


# Создание клавиатуры учитель/ученик
builder_who_are_you_keyboard = InlineKeyboardBuilder()
builder_who_are_you_keyboard.button(text="Учитель", callback_data=UserCallback(foo="teacher"))
builder_who_are_you_keyboard.button(text="Ученик", callback_data=UserCallback(foo="student"))
builder_who_are_you_keyboard.adjust(2, 1)
builder_who_are_you_keyboard = builder_who_are_you_keyboard.as_markup()


# создание кнопки для добавление олимпиады
builder_add_button = InlineKeyboardBuilder()
builder_add_button.button(text="Добавить олимпиаду", callback_data=UserCallback(foo="add_olimp"))
builder_add_button = builder_add_button.as_markup()


# создание клавиатуры по дням
async def create_days_keyboard(week):
    builder = InlineKeyboardBuilder()
    for elem in list_days:
        builder.button(text=f"{elem}", callback_data=DaysCallback(foo="days", day=dict_days[elem], week=week))
    builder.adjust(5, 1)
    return builder.as_markup()


# создание клавиатуры выбора учителя
builder_subjects_keyboards = InlineKeyboardBuilder()
for i, j in teachers["0"].items():
    builder_subjects_keyboards.button(
        text=f"{i}", callback_data=SubjectsCallback(foo="subjects", sub=f"{i}", smbd="add"))
builder_subjects_keyboards.adjust(3, 3, 3)
builder_subjects_keyboards = builder_subjects_keyboards.as_markup()


# Создание клавиатуры выбора языка
builder_lang_keyboards = InlineKeyboardBuilder()
builder_lang_keyboards.button(text="English", callback_data=LangCallback(foo="language", lang="en"))
builder_lang_keyboards.button(text="français", callback_data=LangCallback(foo="language", lang="fr"))
builder_lang_keyboards.button(text="Русский", callback_data=LangCallback(foo="language", lang="ru"))
builder_lang_keyboards.adjust(2, 1)
builder_lang_keyboards = builder_lang_keyboards.as_markup()


# Создание клавиатуры администратора
builder_newsletter_keyboards = InlineKeyboardBuilder()
builder_newsletter_keyboards.button(
    text="Включить", callback_data=AddNewsletter(foo="newsletter", remove=False, add=True))
builder_newsletter_keyboards.button(
    text="Выключить", callback_data=AddNewsletter(foo="newsletter", remove=True, add=False))
builder_newsletter_keyboards.adjust(2, 1)
builder_newsletter_keyboards = builder_newsletter_keyboards.as_markup()


# Создание клавиатуры выбора бота
builder_bot_keyboards = InlineKeyboardBuilder()
builder_bot_keyboards.button(
    text="Бот-расписание", callback_data=ChoiceRoleBotCallbacks(foo="choicebot", model="bot-schedule"))
builder_bot_keyboards.button(
    text="Бот-трекер", callback_data=ChoiceRoleBotCallbacks(foo="choicebot", model="bot-treker"))
builder_bot_keyboards = builder_bot_keyboards.as_markup()


# Создание кнопок Yes/No для подтверждения личности
builder_yes_or_no_button = InlineKeyboardBuilder()
builder_yes_or_no_button.button(text="Да", callback_data=YesOrNoCallback(foo="choice", status=True))
builder_yes_or_no_button.button(text="Нет", callback_data=YesOrNoCallback(foo="choice", status=False))
builder_yes_or_no_button.adjust(2, 1)
builder_yes_or_no_button = builder_yes_or_no_button.as_markup()


# Создание кнопок Yes/No для создания учетки
builder_yes_or_no_register_button = InlineKeyboardBuilder()
builder_yes_or_no_register_button.button(text="Нет", callback_data=YesOrNoCallback(foo="reg_choice", status=False))
builder_yes_or_no_register_button.button(text="Да", callback_data=YesOrNoCallback(foo="reg_choice", status=True))
builder_yes_or_no_register_button.adjust(2, 1)
builder_yes_or_no_register_button = builder_yes_or_no_register_button.as_markup()


# Создание кнопок Yes/No для подтверждения правильности данных
builder_yes_or_no_button2 = InlineKeyboardBuilder()
builder_yes_or_no_button2.button(text="Да", callback_data=YesOrNoCallback(foo="choice2", status=True))
builder_yes_or_no_button2.button(text="Нет", callback_data=YesOrNoCallback(foo="choice2", status=False))
builder_yes_or_no_button2.adjust(2, 1)
builder_yes_or_no_button2 = builder_yes_or_no_button2.as_markup()


# создание клавиатуры выбора наставника
builder_teacher_keyboards = InlineKeyboardBuilder()
builder_get_teacher_keyboard = InlineKeyboardBuilder()
builder_delete_teacher_keyboard = InlineKeyboardBuilder()
for i in range(len(list_teachers_for_treker)):
    builder_teacher_keyboards.button(
        text=f"{list_teachers_for_treker[i]}", callback_data=SubjectsCallback(foo="teacher", sub=f"{i}", smbd="add"))
    builder_get_teacher_keyboard.button(
        text=f"{list_teachers_for_treker[i]}", callback_data=SubjectsCallback(foo="teacher", sub=f"{i}", smbd="get"))
    builder_delete_teacher_keyboard.button(
        text=f"{list_teachers_for_treker[i]}", callback_data=SubjectsCallback(foo="teacher", sub=f"{i}", smbd="delete"))
builder_teacher_keyboards.adjust(3, 3, 3)
builder_get_teacher_keyboard.adjust(3, 3, 3)
builder_delete_teacher_keyboard.adjust(3, 3, 3)
builder_delete_teacher_keyboard = builder_delete_teacher_keyboard.as_markup()
builder_teacher_keyboards = builder_teacher_keyboards.as_markup()
builder_get_teacher_keyboard = builder_get_teacher_keyboard.as_markup()


# Создание клавиатуры выбора олимпиады
builder_olimps_keyboard = InlineKeyboardBuilder()
builder_get_olimps_keyboard = InlineKeyboardBuilder()
builder_delete_olimps_keyboard = InlineKeyboardBuilder()
for i in range(len(list_olimps)):
    builder_olimps_keyboard.button(
        text=f"{list_olimps_full[i]}", callback_data=OlimpsCallback(foo="olimp", olimp=f"{i}", smbd="add")
    )
    builder_get_olimps_keyboard.button(
        text=f"{list_olimps_full[i]}", callback_data=OlimpsCallback(foo="olimp", olimp=f"{i}", smbd="get")
    )
    builder_delete_olimps_keyboard.button(
        text=f"{list_olimps_full[i]}", callback_data=OlimpsCallback(foo="olimp", olimp=f"{i}", smbd="delete")
    )
builder_delete_olimps_keyboard.adjust(1)
builder_olimps_keyboard.adjust(1)
builder_get_olimps_keyboard.adjust(1)
builder_olimps_keyboard = builder_olimps_keyboard.as_markup()
builder_get_olimps_keyboard = builder_get_olimps_keyboard.as_markup()
builder_delete_olimps_keyboard = builder_delete_olimps_keyboard.as_markup()

"""
builder_olimps_keyboard2 = InlineKeyboardBuilder()
builder_get_olimps_keyboard2 = InlineKeyboardBuilder()
for i in range(50, len(list_olimps)):
    builder_olimps_keyboard2.button(
        text=f"{list_olimps_full[i]}", callback_data=OlimpsCallback(foo="olimp", olimp=f"{i}", smbd="add")
    )
    builder_get_olimps_keyboard2.button(
        text=f"{list_olimps_full[i]}", callback_data=OlimpsCallback(foo="olimp", olimp=f"{i}", smbd="get")
    )
builder_olimps_keyboard2.adjust(1, 1, 1)
builder_get_olimps_keyboard2.adjust(1)
builder_olimps_keyboard2 = builder_olimps_keyboard2.as_markup()
builder_get_olimps_keyboard2 = builder_get_olimps_keyboard2.as_markup()
"""

# создание клавиатуры выбора предмета
builder_subjects_for_treker = InlineKeyboardBuilder()
sort_builder_subjects_keyboard = InlineKeyboardBuilder()
builder_delete_subjects_for_treker = InlineKeyboardBuilder()
for i in range(len(config.list_subjects_for_button)):
    builder_subjects_for_treker.button(
        text=f"{config.list_subjects_for_button[i]}",
        callback_data=SubjectsCallback(foo="sub_olimp", sub=f"{i}", smbd="add"))
    sort_builder_subjects_keyboard.button(
        text=f"{config.list_subjects_for_button[i]}",
        callback_data=SubjectsCallback(foo="sub_olimp", sub=f"{i}", smbd="get"))
    builder_delete_subjects_for_treker.button(
        text=f"{config.list_subjects_for_button[i]}",
        callback_data=SubjectsCallback(foo="sub_olimp", sub=f"{i}", smbd="delete"))
builder_subjects_for_treker.adjust(2)
builder_subjects_for_treker = builder_subjects_for_treker.as_markup()
builder_delete_subjects_for_treker = builder_delete_subjects_for_treker.adjust(2).as_markup()
sort_builder_subjects_keyboard = sort_builder_subjects_keyboard.adjust(2).as_markup()


# создание клавиатуры выбора по этапа
builder_stage_keyboards = InlineKeyboardBuilder()
builder_delete_stage_keyboards = InlineKeyboardBuilder()
sort_builder_stage_keyboard = InlineKeyboardBuilder()
for i in range(len(config.stages)):
    builder_stage_keyboards.button(
        text=f"{config.stages[i]}", callback_data=OlimpsCallback(foo="stage", olimp=f"{i}", smbd="add"))
    sort_builder_stage_keyboard.button(
        text=f"{config.stages[i]}", callback_data=OlimpsCallback(foo="stage", olimp=f"{i}", smbd="get"))
    builder_delete_stage_keyboards.button(
        text=f"{config.stages[i]}", callback_data=OlimpsCallback(foo="stage", olimp=f"{i}", smbd="delete"))
builder_stage_keyboards.adjust(1)
builder_stage_keyboards = builder_stage_keyboards.as_markup()
builder_delete_stage_keyboards = builder_delete_stage_keyboards.adjust(1).as_markup()
sort_builder_stage_keyboard = sort_builder_stage_keyboard.adjust(1).as_markup()


# кнопка получения таблицы
builder_fullsheet_keyboards = InlineKeyboardBuilder()
builder_fullsheet_keyboards.button(text="Получить таблицу", callback_data=OtherCallbacks(foo="fullsheet", other="user"))
builder_fullsheet_keyboards.button(text="Удалить олимпиаду", callback_data=OtherCallbacks(foo="fullsheet",
                                                                                          other="delete"))
builder_fullsheet_keyboards = builder_fullsheet_keyboards.as_markup()


builder_filter_fullsheet_keyboards = InlineKeyboardBuilder()
builder_filter_fullsheet_keyboards.button(
    text="Получить таблицу",
    callback_data=OtherCallbacks(foo="fullsheet", other="filter")
)
builder_filter_fullsheet_keyboards = builder_filter_fullsheet_keyboards.as_markup()


async def get_delete_olimps_buttons(max_index):
    """Кнопки для удаления из бд
    :param max_index: int"""
    builder = InlineKeyboardBuilder()
    builder.button(text="Отмена", callback_data=DeleteCallback(foo="delete", index=999))
    for index in range(max_index):
        builder.button(text=f"{index}", callback_data=DeleteCallback(foo="delete", index=index))
    builder.adjust(1, 5, 5)
    return builder.as_markup()
