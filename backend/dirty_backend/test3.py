from PIL import Image, ImageDraw, ImageFont


dict_timetable = {"1": "8.30 - 9.10",
                  "2": "9.20 - 10.00",
                  "3": "10.20 - 11.00",
                  "4": "11.10 - 11.50",
                  "5": "12.00 - 12.40",
                  "6": "13.00 - 13.40",
                  "7": "14.00 - 14.40",
                  "8": "14.50 - 15.30",
                  "9": "15.40 - 16.20"}


# Создание функции для рисования расписания
def draw_timetable(lessons, data, teacher=False, num=False):
    if teacher:
        new_lessons = []
        count = 0
        for i in lessons[::-1]:
            if i[0] != "None" and i[0] != "None" and i[0] is not None:
                new_lessons.append([i[0], dict_timetable[str(i[1])]])
                count = 1
            else:
                if count:
                    new_lessons.append(["Окно"])

        lessons = new_lessons[::-1]
        # lessons = [[i[0], dict_timetable[str(i[1])]] for i in lessons if (i[0] != "None") and (i[0] != "") and
        #            (i[0] is not None)]
    image_width, image_height = 400, (len(lessons) + 1) * 50

    # Создание изображения
    image = Image.new("RGB", (image_width, image_height), "white")
    draw = ImageDraw.Draw(image)

    # Установка шрифта
    font = ImageFont.truetype("fonts/ofont.ru_GOST type B.ttf", 20, encoding="UTF-8")

    # Рисование расписания
    y = 50
    count = 0
    draw.text((10, 10), f"{data}", font=font, fill="black")
    for i, lesson in enumerate(lessons):
        if count < 2:
            # color = (66, 170, 255)
            color = (131, 236, 156)
            count += 1
        elif count < 4:
            count += 1
            color = "white"
            # color = (131, 236, 202)
        else:
            count = 1
            # color = (66, 170, 255)
            color = (131, 236, 156)
        draw.rectangle([(0, y), (image_width, y + 50)], fill=color)
        draw.text((10, y + 10), f"{i + 1}. {lesson[0]}", font=font, fill="black")
        try:
            if teacher:
                draw.text((image_width - 150, y + 10), lesson[1], font=font, fill="black")
            else:
                draw.text((image_width - 100, y + 10), lesson[1], font=font, fill="black")
        except Exception:
            pass
        y += 50

    # Возврат изображения
    if not num:
        image.save("images/schedule.png")
    else:
        image.save(f"images/schedule{num}.png")


if __name__ == "__main__":
    draw_timetable([['Литература', '5'], ['Литература', '5'], ['Башкирский язык', '3/мк'],
                    ['Башкирский язык', '3/мк'], ['Физкультура'], ['Физкультура'], ['Классный час', '5']],
                   "somebody")

