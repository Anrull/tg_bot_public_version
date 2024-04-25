from aiogram import types
import backend.callbacks.callbacks as callbacks


async def get_days_schedule(message: types.Message):
    await message.answer(text="Расписание нечетной недели", reply_markup=await callbacks.create_days_keyboard("1"))

    await message.answer(text="Расписание четной недели", reply_markup=await callbacks.create_days_keyboard("0"))