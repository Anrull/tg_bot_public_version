import openpyxl
import asyncio
from peewee import *
# import backend.dirty_backend.db.new_user as user


db = SqliteDatabase(r"C:\Users\bogda\PycharmProjects\Tg_bot\db\users.db")


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    user_id = TextField("id")
    name = TextField("name")
    username = TextField("username")
    classes = TextField("classes")
    role = TextField("role")
    name_teacher = TextField("name_teacher")
    settings = TextField("settings")
    newsletter = TextField("newsletter")
    bot = TextField("bot")
    last_ids = TextField("last_ids")


class Treker(BaseModel):
    user_id = TextField()
    time = TextField()
    name = TextField()
    classes = TextField()
    snils = TextField()
    olimps = TextField()
    last_id_olimps = IntegerField()


class Members(BaseModel):
    date = CharField()
    full_names = TextField()
    classes = CharField()
    olimps = TextField()
    stage = CharField()
    subjects = CharField()
    other = CharField()
    teacher = CharField()


db.create_tables([User, Treker, Members])


def update_db(path):
    book = openpyxl.load_workbook(path, read_only=True)
    book.active = 0
    sheet = book.active

    for row in range(1, sheet.max_row):
        try:
            try:
                query = Members.select().where(
                    full_names=f"{sheet[row][2].value}",
                    classes=f"{sheet[row][3].value}",
                    olimps=f"{sheet[row][4].value}",
                    stage=f"{sheet[row][5].value}",
                    subjects=f"{sheet[row][6].value}",
                    teacher=f"{sheet[row][8].value}")
                if query:
                    continue
            except:
                pass

            Members.create(date=f"{sheet[row][1].value}",
                                full_names=str(sheet[row][2].value.replace(" ", " ")),
                                classes=sheet[row][3].value,
                                olimps=f"{sheet[row][4].value}",
                                stage=f"{sheet[row][5].value.replace(" ", " ")}",
                                subjects=f"{sheet[row][6].value.replace(" ", " ")}",
                                other=str(sheet[row][7].value),
                                teacher=f"{sheet[row][8].value.replace(" ", " ")}")

            print(row)
        except:
            print(0)
            return


if __name__ == "__main__":
    update_db(r"C:\Users\bogda\Downloads\Telegram Desktop\Таблица РСОШ.Трекер 2023_2024 (3).xlsx")
