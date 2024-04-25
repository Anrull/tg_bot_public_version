from aiogram import types
# from backend.dirty_backend.user import User
import backend.dirty_backend.db.new_user as user
import config as config
import backend.callbacks.callbacks as callbacks


async def choice_lang(message: types.Message):
    # user.add_settings(message)
    await message.answer("Выберите язык расписания", reply_markup=callbacks.builder_lang_keyboards)