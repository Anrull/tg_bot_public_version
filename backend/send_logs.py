from aiogram.types import FSInputFile
from aiogram import Bot
import config
import backend.dirty_backend.make_zip as make_zip


bot = Bot(token=config.TOKEN)


async def send_logs(user_id):
    await make_zip.made_zip_files_logs()
    
    file = FSInputFile("time_files/logs.zip")
    
    await bot.send_document(user_id, file)
