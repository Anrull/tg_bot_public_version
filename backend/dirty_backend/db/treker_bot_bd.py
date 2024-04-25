from peewee import *


class Family(Model):
    created_at = TextField()
    full_name = TextField()
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
    mother_position = TextField()
    mother_phone_number = TextField()
    father_full_name = TextField()
    father_workplace = TextField()
    father_position = TextField()
    father_phone_number = TextField()

    class Meta:
        database = SqliteDatabase('db/student.db')


def get_info_by_snils(snils):
    return Family.get(Family.snils == snils)
