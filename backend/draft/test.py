from PIL import Image, ImageDraw, ImageFont
from config import table


def draw_timetable(lst):
    width = 400
    height = 350
    
    img = Image.new('RGB', (width, height), color = 'white')

    y = 20
    count = 1

    for i in lst:
        sub = i[0]
        try:
            num = i[1]
        except Exception:
            num = ""
        
        subject = f"{count}: {sub} - {num}"
        font = ImageFont.truetype('arial.ttf', 30)
        draw = ImageDraw.Draw(img)
        draw.text((20, y), subject, fill = 'black', font = font)
        
        y += 40
        count += 1

    img.save('images/output.png')


if __name__ == "__main__":
    lst = table["1"]["9B"]["0"]
    draw_timetable(lst)
