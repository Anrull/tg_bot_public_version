from aiogram import types
# from backend.dirty_backend.user import User
import backend.dirty_backend.db.new_user as user
import config as config
import backend.callbacks.callbacks as callbacks
from aiogram.utils.keyboard import ReplyKeyboardBuilder


hello_message = """🤙 Привет, это бот-расписание. Кто ты?"""


async def get_start(message: types.Message):
    user.new_users(message)

    # await message.answer(text=config.hello_message, reply_markup=callbacks.builder_classes_keyboards)

    await message.answer(text=hello_message, reply_markup=callbacks.builder_who_are_you_keyboard)


async def get_treker_start(message: types.Message):
    await message.answer("Для начала работы напиши свой номер СНИЛС")


async def get_start_work(message: types.Message):
    user.new_users(message)

    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text="Расписание"),
        types.KeyboardButton(text="РСОШ трекер")
    )

    await message.answer("Выберите бота", reply_markup=builder.as_markup(resize_keyboard=True))
