import openpyxl
import backend.dirty_backend.db.new_user as user


async def replace_db(path):
    user.Members.drop_table()
    user.db.create_tables([user.User, user.Treker, user.Members])
    await update_db(path)


async def update_db(path):
    book = openpyxl.load_workbook(path, read_only=True)
    book.active = 0
    sheet = book.active

    for row in range(1, sheet.max_row):
        try:
            try:
                query = user.Members.select().where(
                    full_names=f"{sheet[row][2].value}",
                    classes=f"{sheet[row][3].value}",
                    olimps=f"{sheet[row][4].value}",
                    stage=f"{sheet[row][5].value}",
                    subjects=f"{sheet[row][6].value}",
                    teacher=f"{sheet[row][8].value}")
                if query:
                    continue
            except:
                user.Members.create(date=f"{sheet[row][1].value}",
                                    full_names=str(sheet[row][2].value.replace(' ', ' ')),
                                    classes=sheet[row][3].value,
                                    olimps=f"{sheet[row][4].value}",
                                    stage=f"{sheet[row][5].value.replace(' ', ' ')}",
                                    subjects=f"{sheet[row][6].value.replace(' ', ' ')}",
                                    other=str(sheet[row][7].value),
                                    teacher=f"{sheet[row][8].value.replace(' ', ' ')}")

                print(1)
        except:
            print(0)
            return


if __name__ == "__main__":
    update_db(r"C:\Users\bogda\Downloads\Таблица РСОШ.Трекер 2023_2024.xlsx")
