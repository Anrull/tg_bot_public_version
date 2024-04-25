import json
import asyncio

with open("dicts/dict.json") as js:
    tabel = json.load(js)

with open("dicts/subjects.json") as js:
    subjects = json.load(js)

with open("dicts/teachers.json") as js:
    schedule_teacher = json.load(js)

# print(subjects)

list_classes = ["11B", "11A", "10B", "10A", "9B", "9A", "8B", "8A", "7C", "7B", "7A", "6B", "6A"]


async def search(sub, week, day):
    list_schedule = []
    for j in list_classes:
        for k in tabel[str(week)][j][str(day)]:
            if "/" in k[0]:
                if len(k) == 2:
                    if "/" in k[1]:
                        nums = k[1].split("/")
                    else:
                        nums = k[1]
                else:
                    nums = False
                subs = k[0].split("/")
                for i in range(len(subs)):
                    if subs[i] in subjects[sub]:
                        if nums:
                            list_schedule.append([subs[i], nums[i]])
                        else:
                            list_schedule.append([subs[i]])
            if k[0] in subjects[sub]:
                list_schedule.append(k)
    return list_schedule


async def upgrate_search(name, week, day):
    return schedule_teacher[str(week)][str(name)][str(day)]


if __name__ == "__main__":
    # print(asyncio.run(search("Информатика", 1, 4)))
    print(asyncio.run(upgrate_search("Суяргулова Г.З.", 1, 0)))
