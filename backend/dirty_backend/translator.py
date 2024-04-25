import googletrans as tr
import asyncio


translator = tr.Translator()


async def translate_list(input_list, language="en"):
    output_list = []
    for item in input_list:
        translated_text = translator.translate(item[0], dest=language).text
        if len(item) == 2:
            output_list.append([translated_text, translator.translate(item[1], dest=language).text])
        else:
            output_list.append([translated_text])
    return output_list


async def translate_text(text, lang="en"):
    return translator.translate(text, dast=lang).text


if __name__ == "__main__":
    out = asyncio.run(translate_list([['Литература', '5'], ['Литература', '5'], ['Башкирский язык', '3/мк'], ['Башкирский язык', '3/мк'], ['Физкультура'], ['Физкультура'], ['Классный час', '5']]))
    print(out)

