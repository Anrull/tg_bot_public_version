import sys
from aiogram import types, Bot
import config as config
import backend.dirty_backend.db.new_user as user
import backend.callbacks.callbacks as callbacks


bot = Bot(token=config.TOKEN)


async def get_admin(message: types.Message):
    password = message.text.replace('/admin ', '')
    
    status_message = await message.answer("Проверка пароля 🔐")
    
    print(password)
    
    if password == config.password:
        await status_message.edit_text("Добро пожаловать, Администратор!",
                                       reply_markup=callbacks.builder_admin_keyboards)
    else:
        await status_message.edit_text('Простите, вы что-то хотели?')


async def get_admin_shutdown(message: types.Message):
    password = message.text.replace('/shutdown ', "")
    status_message = await message.answer("Проверка пароля...")
    if password == config.password:
        await status_message.edit_text("Выключение....")
        sys.exit()
    else:
        await status_message.edit_text('Простите, вы что-то хотели?')


async def send_newsletter(message: types.Message):
    password = message.text.replace('/send ', "")
    status_message = await message.answer("Проверка пароля...")
    if config.password in password:
        text = password.replace(config.password, "")
        msg = await status_message.edit_text("Производится рассылка")
        await send_messages(text)
        await msg.edit_text("""Рассылка была завершена""")
    else:
        await status_message.edit_text('Простите, вы что-то хотели?')


async def send_messages(text_msg):
    list_id = [int(user_id.user_id) for user_id in user.get_all()]
    for user_id in list_id:
        if int(user.get_info_about_person(user_id).newsletter):
            try:
                await bot.send_message(user_id, text_msg)
            except Exception as e:
                print("Error")
