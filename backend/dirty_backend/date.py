from datetime import datetime, timedelta
import json
import datetime
import asyncio


"""Заменить время при публикации на сервере"""


with open("dicts/weeks.json") as js:
    tabel_weeks = json.load(js)


dict_days_of_week = {"Monday": "0", "Tuesday": "1", "Wednesday": "2", "Thursday": "3", "Friday": "4", "Saturday": "0", "Sunday": "0"}
dict_days_of_week_tomorrow = {"Monday": "1", "Tuesday": "2", "Wednesday": "3", "Thursday": "4", "Friday": "0", "Saturday": "0", "Sunday": "0"}


async def get_week(date, flag=False):
    if not flag:
        if date.weekday() == 6:
            date += timedelta(days=1)
        elif date.weekday() == 5:
            date += timedelta(days=2)
    else:
        if date.weekday() > 5:
            date -= timedelta(days=3)

    date_string = date.strftime("%Y-%m-%d")
    try:
        return tabel_weeks[date_string]
    except Exception:
        return None


async def get_next_week(date):
    if date.weekday() == 6:
        date += timedelta(days=1)
    elif date.weekday() == 5:
        date += timedelta(days=2)
    elif date.weekday() == 4:
        date += timedelta(days=3)

    date_string = date.strftime("%Y-%m-%d")
    try:
        return tabel_weeks[date_string]
    except Exception:
        return None


async def day_today():
    # now = datetime.datetime.now()
    # day_of_week = now.strftime("%A")
    # return_num = dict_days_of_week[day_of_week]
    # if now.hour > 12 or (now.hour == 12 and now.minute >= 30):
    #     return_num = int(return_num) + 1
    #     if return_num > 4:
    #         return "0"
    #     return str(return_num)
    # else:
    #     return str(return_num)
    date = datetime.datetime.now()
    if date.hour > 12 or (date.hour == 12 and date.minute >= 30):
        date += timedelta(days=1)
    return dict_days_of_week[date.strftime("%A")]


async def day_tomorrow():
    # now = datetime.datetime.now()
    # day_of_week = now.strftime("%A")
    # return_num = dict_days_of_week[day_of_week]
    # return_num = int(return_num) + 1
    # if return_num > 3:
    #     return "0"
    # return str(return_num)
    return dict_days_of_week_tomorrow[datetime.datetime.today().strftime("%A")]


if __name__ == "__main__":
    print(asyncio.run(day_today()))
    print(asyncio.run(day_tomorrow()))
    # print(asyncio.run(next_monday()))
