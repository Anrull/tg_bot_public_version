from peewee import *
import datetime
import ast
from backend.dirty_backend.db.history.history import add_history, delete_history

db = SqliteDatabase("db/users.db")
db_members = SqliteDatabase("db/members.db")


# cur = con.cursor()
# olimps = 
#    [
#     [
#      oplimp,
#      stage,
#      subject,
#      teacher
#      ]
#    ]


class Family(Model):
    user_id_by_yandex = TextField()
    created_at = TextField()
    full_name = TextField()
    classes = TextField()
    birth_date = TextField()
    phone_number = TextField()
    email = TextField()
    birth_place = TextField()
    registration_place = TextField()
    living_place = TextField()
    passport_data = TextField()
    snils = TextField()
    inn = TextField()
    mother_full_name = TextField()
    mother_workplace = TextField()
    mother_phone_number = TextField()
    father_full_name = TextField()
    father_workplace = TextField()
    father_phone_number = TextField()

    class Meta:
        database = SqliteDatabase('db/student.db')


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
    last_id_olimps = TextField()
    delete_olimps = TextField()


class Members(Model):
    date = CharField()
    full_names = TextField()
    classes = CharField()
    olimps = TextField()
    stage = CharField()
    subjects = CharField()
    other = CharField()
    teacher = CharField()

    class Meta:
        database = db_members


db.create_tables([User, Treker])


def add_delete_olimps(message, delete_olimps):
    treker = Treker.get(Treker.user_id == message.chat.id)
    treker.delete_olimps = f"{delete_olimps}"
    treker.save()


def get_delete_olimps(message, number: int):
    treker = Treker.get(Treker.user_id == message.chat.id)
    dict_olimps = ast.literal_eval(treker.delete_olimps)
    olimp = dict_olimps[number]
    members = Members.get(Members.olimps == olimp["olimps"], Members.stage == olimp["stage"],
                          Members.subjects == olimp["subjects"], Members.teacher == olimp["teacher"])
    try:
        delete_history({"olimps": olimp["olimps"], "stage": olimp["stage"], "sub": olimp["subjects"],
                    "teacher": olimp["teacher"], "name": treker.name})
    except Exception as e:
        print(e)
        print("Error delete history")
    members.delete_instance()


def add_filters(message, lst):
    treker = Treker.get(Treker.user_id == message.chat.id)
    dict_tr = {
        "name": f"{lst[0]}",
        "role": f"{lst[1]}"
    }
    treker.last_id_olimps = f"{dict_tr}"
    treker.save()
    print("Done")


def is_registered_treker(message):
    Treker.get(Treker.user_id == message.chat.id)


def delete_user_treker(message):
    treker = Treker.get(Treker.user_id == message.chat.id)
    treker.delete_instance()


def get_filters(message):
    treker = Treker.get(Treker.user_id == message.chat.id)
    return ast.literal_eval(treker.last_id_olimps)


def get_elem_treker(message, elem, role="None"):
    name = Treker.get(user_id=message.chat.id).name
    elem = f"{elem}"
    members = Members.select()
    match role:
        case "teacher":
            # .where(full_names=name, teacher=elem)
            members = members.where(Members.full_names == name, Members.teacher == elem)
        case "stage":
            # .where(full_names=name, stage=elem)
            members = members.where(Members.full_names == name, Members.stage == elem)
        case "sub":
            # .where(full_names=name, subjects=elem)
            members = members.where(Members.full_names == name, Members.subjects == elem)
        case "olimp":
            # .where(full_names=name, olimps=elem)
            members = members.where(Members.full_names == name, Members.olimps == elem)
        case _:
            raise ValueError
    return members


def get_all_treker():
    return Members.select()


def get_model(message):
    try:
        user = User.get(User.user_id == message.chat.id)
        return user.bot
    except:
        pass


def add_ids(message, *ids):
    user = User.get(User.user_id == message.chat.id)
    user.last_ids = str(ids)
    user.save()


def get_last_ids(message):
    user = User.get(User.user_id == message.chat.id)
    return ast.literal_eval(user.last_ids)


def rewrite_model_bot(message, model):
    user = User.get(User.user_id == message.chat.id)
    user.bot = model
    user.save()


def new_user_treker(message):
    user_id = message.from_user.id
    time = str(datetime.datetime.now())
    classes = "Не указан"
    name = "Не указан"
    snils = "Не указан"
    olimps = str([])
    try:
        Treker.get(Treker.user_id == user_id)
    except:
        Treker.create(user_id=user_id, time=time, name=name, classes=classes, snils=snils, olimps=olimps)


def add_info_about_user_treker(message, snils):
    user_id = message.chat.id
    result = Family.get(Family.snils == snils)

    name = result.full_name
    if name.endswith(" "):
        name = name[:-1]
    classes = result.classes

    try:
        treker = Treker.get(Treker.user_id == user_id)
        treker.name = name
        treker.classes = classes
        treker.snils = snils
        treker.save()
    except:
        Treker.create(user_id=user_id, time=datetime.datetime.now(), name=name, classes=classes, snils=snils,
                      olimps="[[]]")

    return {"name": name, "class": classes}


def is_user_registered(message):
    try:
        Treker.get(Treker.user_id == message.chat.id)
        return True
    except:
        return False


def add_olimps_elem_treker(message, elem):
    user_id = message.chat.id
    treker = Treker.get(Treker.user_id == user_id)
    olimps = ast.literal_eval(treker.olimps)
    print(olimps)

    olimps.append(elem)

    treker.olimps = olimps
    treker.save()
    # if olimps:
    #     for i in range(len(olimps)):
    #         if len(olimps[i]) and len(olimps[i]) != 4:
    #             olimps[i].append(elem)
    #             tr.olimps = olimps
    #             tr.save()
    #             return None
    # olimps.append([elem])
    # tr.olimps = olimps
    # tr.save()


def add_time_files_to_treker(messsage):
    treker = Treker.get(Treker.user_id == messsage.chat.id)
    olimp = ast.literal_eval(treker.olimps)
    Members.create(
        date=datetime.datetime.now(),
        full_names=treker.name,
        classes=treker.classes,
        olimps=olimp[2],
        stage=olimp[-1],
        subjects=olimp[1],
        other="None",
        teacher=olimp[0]
    )


def get_olimps(message):
    treker = Treker.get(Treker.user_id == message.chat.id)
    return ast.literal_eval(treker.olimps)


def add_new_treker_start(message):
    tr = Treker.get(Treker.user_id == message.chat.id)
    tr.olimps = f"[]"
    tr.save()


async def new_add_treker(message):
    tr = Treker.get(Treker.user_id == message.chat.id)

    print(0)

    olimps = ast.literal_eval(tr.olimps)
    print(olimps)
    tr.olimps = f"[]"
    tr.save()

    try:
        query = Members.get(Members.full_names == tr.name, Members.classes == tr.classes,
                            Members.olimps == olimps[2], Members.stage == olimps[3],
                            Members.subjects == olimps[1], Members.teacher == olimps[0])

        print(1)

        return "Такая запись уже существует"
    except:
        pass

    try:
        if olimps[3] not in ["Прошел регистрацию", "Написал отборочные этапы (волну, тур)"]:
            data = {"name": tr.name, "olimps": olimps[2],
                    "stage": olimps[3], "subjects": olimps[1], "teacher": olimps[0]}
            await add_history(data)
    except Exception as e:
        print(e)
        print("Error create history")
        return "Ошибка создания записи для истории"
    # name = tr.name
    try:
        Members.create(
            date=datetime.datetime.now(),
            full_names=tr.name,
            classes=tr.classes,
            olimps=olimps[2],
            stage=olimps[3],
            subjects=olimps[1],
            other=f"None",
            teacher=olimps[0]
        )
    except:
        print("Error")
        return "Ошибка создания записи"

    print(4)

    return "Форма отправлена"


def get_olimps_treker(message):
    treker = Treker.get(Treker.user_id == message.chat.id)
    name = treker.name

    member = Members.select().where(Members.full_names == name)

    return member


def new_users(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username

    classes = "Не указан"
    role = "Не указана"
    teacher = "Не указан"
    name = f"{first_name} {last_name}"
    settings = [["ru"]]
    newsletter = "1"
    bot = "bot-schedule"
    try:
        user = User.get(User.user_id == user_id)
        user.name = name
        user.username = username
        user.save()
    except User.DoesNotExist:
        User.create(user_id=user_id, name=name, username=username, classes=classes, role=role, name_teacher=teacher,
                    settings=settings, newsletter=newsletter, bot=bot)


def add_class(message, text_class):
    user = User.get(User.user_id == message.chat.id)
    user.classes = text_class
    user.save()


def check(message):
    user = User.get(User.user_id == message.chat.id)
    classes = user.classes
    return classes if classes != "Не указан" else None


def add_role(message, text_role):
    user = User.get(User.user_id == message.chat.id)
    user.role = text_role
    user.save()


def get_role(user_id):
    user = User.get(User.user_id == user_id)
    return user.role


def add_sub(message, text_subject):
    user = User.get(User.user_id == message.chat.id)
    user.name_teacher = text_subject
    user.save()


def get_sub(message=None, user_id=None):
    if message:
        user = User.get(User.user_id == message.chat.id)
    elif user_id:
        user = User.get(User.user_id == user_id)
    return user.name_teacher


def get_user_count():
    return User.select().count()


def add_settings(message, text_settings):
    user = User.get(User.user_id == message.chat.id)
    user.settings = text_settings
    user.save()


def get_lang(message=None, user_id=None):
    if message:
        user = User.get(User.user_id == message.chat.id)
    else:
        user = User.get(User.user_id == user_id)
    return user.settings


def get_all():
    return User.select()
    # return User.get(User.user_id == )


def check_schedule(user_id):
    user = User.get(User.user_id == user_id)
    classes = user.classes
    return classes if classes != "Не указан" else None


def add_newsletter(user_id, text_newsletter):
    user = User.get(User.user_id == user_id)
    user.newsletter = text_newsletter
    user.save()


def get_info_about_person(user_id):
    return User.get(User.user_id == user_id)


# if __name__ == "__main__":
#     db.create_tables([User, Treker])

if __name__ == "__main__":
    # get_elem_treker()
    pass
