import openpyxl
import json
import sys


def update(path_of_xlsx):
    sys.stdout = open("dicts/dict.py", "w", encoding="UTF-8")
    book = openpyxl.load_workbook(path_of_xlsx, read_only=True)

    MEGA_dict = {}

    for i in range(2):
        book.active = i
        sheet = book.active

        mega_list = ["6A", "6B", "7A", "7B", "7C", "8A", "8B", "9A", "9B", "10A", "10B", "11A", "11B"]
        mega_dict = {}
        mega_count = 0
        mega_count1, mega_count2 = 2, 3

        title = sheet[10][0].value.lower()

        for i in range(13):
            dict_object = {}
            count = 0
            count2 = 0
            lst = []

            for i in range(13, sheet.max_row):
                obj = sheet[i][mega_count1].value
                obj2 = sheet[i][mega_count2].value
                # if obj != None:
                #     count += 1
                #     if obj2:
                #         lst.append([obj, str(obj2)])
                #     else:
                #         lst.append([obj])
                #     # print(obj)
                # elif obj == None and count:
                #     dict_object[count2] = lst
                #     lst = []
                #     count = 0
                #     count2 += 1
                # elif not lst and obj == None:
                #     continue
                if str(sheet[i][1].value) != "8":
                    if not obj and not obj2:
                        continue
                    elif obj2:
                        lst.append([obj, str(obj2)])
                    else:
                        lst.append([obj])
                else:
                    dict_object[count2] = lst
                    count2 += 1
                    lst = []
            
            mega_count2 += 2
            mega_count1 += 2
            
            mega_dict[mega_list[mega_count]] = dict_object
            
            mega_count += 1

        if "НЕЧЕТН".lower() in title or "НЕЧЁТН".lower() in title:
            MEGA_dict[1] = mega_dict
            title = "четная"
        else:
            MEGA_dict[0] = mega_dict
            title = "нечетная"


    print(MEGA_dict)
    json_dict = json.dumps(obj=MEGA_dict)

    sys.stdout = open("dicts/dict.json", "w")
    print(json_dict)


if __name__ == "__main__":
    update("расписание_23_24_готово_2_полугодие (2).xlsx")