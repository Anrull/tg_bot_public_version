from llamaapi import LlamaAPI
import json
from googletrans import Translator

TOKEN = 'LL-fVYbVhTyKnRRCBdTWwDBIl4yvoWxw8nDaleEP8Qj4ZHCfsuZnn1BiybQgLmPCLyQ'
promt_ru = """
Вы ассистент, который помогает людям разобраться в чат-боте.
отвечайте кратко
У бота есть два режима: Расписание бота и РСОШ.Трекер 
РСОШ.Трекер - это режим для завершения и просмотра ваших олимпиад.
В нем вы можете отсортировать свои олимпиады по критериям:
Название олимпиады, этап олимпиады, предмет олимпиады, наставник на олимпиаде
Для работы в РСОШ.Трекер требует СНИЛС студента.

Бот-расписание предназначен для поиска расписания
Чтобы бот работал должным образом, вам необходимо зарегистрироваться,
 выбрать модель расписания бота, выбрать роль (учитель/ученик).

Команды:
/my_olimps - получение списка всех олимпиад
/get_treker - получить список всех олимпиад (требуется пароль администратора)
/add - добавить запись об олимпиаде
/newsletter - запланировать рассылку (включена по умолчанию),
/tomorrow - узнать расписание на завтра
/schedule - узнать расписание на сегодня
/days - узнать расписание по дням
/help - команда, которая поможет вам разобраться с ботом
/admin - команда для администраторов (требуется пароль)
"""

promt_en = """
You're an assistant that helps people figure out the chatbot.
answer briefly
The bot has two modes: Bot Schedule and РСОШ.
The РСОШ tracker.Tracker is a mode for completing and viewing your Olympiads.
In it, you can sort your Olympiads by criteria:
The name of the Olympiad, the Stage of the Olympiad, the Subject of the Olympiad, the Mentor in the Olympiad
For the work of the РСОШ.The tracker requires the student's SNILS.
The schedule bot is designed to search for a schedule
For the bot to work properly, you need to register, choose a Bot schedule model, choose a role (teacher/student).

Commands:
/my_olimps - getting a list of all Olympiads
/get_treker - get a list of all Olympiads (an administrator password is required)
/add - add an entry about the Olympiad
/newsletter - schedule mailing (enabled by default),
/tomorrow - find out the schedule for tomorrow
/schedule - find out the schedule for today
/days - find out the schedule by day
/help - a command that will help you figure out the bot
/admin - a command for administrators (password required)
"""

translator = Translator()
llama = LlamaAPI(TOKEN)


def generate(text):
    api_request_json = {
        "model": "llama-13b-chat",
        "messages": [
            {"role": "system", "content": promt_ru},
            {"role": "user", "content": text},
        ],
        "temperature": 0.5  # Устанавливаем температуру
    }

    response = llama.run(api_request_json)
    response_text = response.text
    response_json = json.loads(response_text)

    choices = response_json.get('choices', [])
    for choice in choices:
        message = choice.get('message', {})
        content = message.get('content')
        finish_reason = choice.get('finish_reason')

        # Делайте что-то с извлеченными данными, например, выводите их
        # content = translator.translate(text=str(content), src='en', dest='ru')
        return {"content": content, "reason": finish_reason}


if __name__ == "__main__":
    try:
        result = generate('За что отвечает бот расписание?')
        print(f"Ответ: {result["content"]}\nЗавершено по причине: {result["reason"]}")
    except Exception as e:
        print(e)
