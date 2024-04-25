import openpyxl
import json
import sys


def update(path_of_xlsx):
    sys.stdout = open("dicts/weeks.json", "w")
    
    book = openpyxl.load_workbook(path_of_xlsx, read_only=True, data_only=True)
    sheet = book.active
    mega_dict = {}
    
    for j in range(1, 6):
        for i in range(sheet.max_column):
            mega_dict[str(sheet[j][i].value)[:10]] = sheet[6][i].value

    print(json.dumps(obj=mega_dict))
    # print(mega_dict)


if __name__ == "__main__":
    update("Books/Книга1.xlsx")