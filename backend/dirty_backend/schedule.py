import asyncio
import json

with open("dicts/dict.json") as js:
    table = json.load(js)


async def send_schedule_text(text_class, week="1", day="0"):
    return list(table[str(week)][text_class][str(day)])
    # return list(table[str(week)][text_class])


if __name__ == "__main__":
    print(asyncio.run(send_schedule_text("9B", week=1, day=3)))
