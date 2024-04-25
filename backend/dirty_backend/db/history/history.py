import datetime
import asyncio
from peewee import *

db = SqliteDatabase('backend/dirty_backend/db/history/history.db')
# db = SqliteDatabase('history.db')


class History(Model):
    date = DateField(default=datetime.datetime.today())
    name = TextField()
    olimps = TextField()
    stage = TextField()
    teacher = TextField()
    subjects = TextField()

    class Meta:
        database = db


async def get_history(limit=15):
    entries = History.select().order_by(History.date.desc()).limit(limit)
    return [{"date": elem.date, "name": elem.name, "olimps": elem.olimps,
             "stage": elem.stage, "teacher": elem.teacher, "sub": elem.subjects} for elem in entries]


async def add_history(data):
    history = History(
        name=data.get("name"),
        olimps=data["olimps"],
        stage=data["stage"],
        teacher=data["teacher"],
        subjects=data["subjects"]
    )
    history.save()


def delete_history(data):
    history = History.get(
        History.name == data["name"],
        History.olimps == data["olimps"],
        History.stage == data["stage"],
        History.teacher == data["teacher"],
        History.subjects == data["sub"]
    )
    history.delete_instance()


# db.create_tables([History])

if __name__ == "__main__":
    print(asyncio.run(get_history()))