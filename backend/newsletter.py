from aiogram import types
# from backend.dirty_backend.user import User
import backend.dirty_backend.db.new_user as user
import backend.callbacks.callbacks as callbacks


async def get_newsletter(message: types.Message):
    newsletter = user.get_info_about_person(user_id=message.chat.id).newsletter
    if int(newsletter):
        await message.answer("На данный момент вам должны приходить расписания, желаете отключить?", reply_markup=callbacks.builder_newsletter_keyboards)
    else:
        await message.answer("На данный момент вам не должны приходить расписания, желаете включить?", reply_markup=callbacks.builder_newsletter_keyboards)
