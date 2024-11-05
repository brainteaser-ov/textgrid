# import os
#
#
# def delete_wav_textgrid_pairs(folder_path, file_numbers):
#     # Преобразуем номера в строковый формат с учетом формата файла
#     file_numbers = [str(num) for num in file_numbers]
#
#     for num in file_numbers:
#         wav_file = os.path.join(folder_path, f"f_{num}.wav")
#         textgrid_file = os.path.join(folder_path, f"f_{num}.TextGrid")
#
#         # Удаляем wav файл, если он существует
#         if os.path.isfile(wav_file):
#             os.remove(wav_file)
#             print(f"Удалён файл: {wav_file}")
#
#         # Удаляем TextGrid файл, если он существует
#         if os.path.isfile(textgrid_file):
#             os.remove(textgrid_file)
#             print(f"Удалён файл: {textgrid_file}")
#
#
# # Пример использования
# folder_path = '/Users/oksanagoncarova/Рабочий стол/работа/И РАН/Словарь волжского диалекта марийского языка 2/all_data'
# file_numbers = [209, 1166, 1167, 156, 354, 1205, 234, 1165, 1159, 1164,
#                 353, 421, 384, 1148, 1160, 1161, 1149, 1203, 387, 1163,
#                 1162, 147, 386, 243, 293, 292, 468, 289, 301, 214, 374,
#                 176, 1153, 1152, 177, 149, 175, 1151, 1186, 148, 1155,
#                 1154, 171, 417, 173, 1156, 1157, 358, 1235]
#
# delete_wav_textgrid_pairs(folder_path, file_numbers)

# import csv
#
# unique_sounds = set()
#
# with open('/Users/oksanagoncarova/Desktop/ipynb/new.csv', 'r', encoding='utf-8') as csvfile:
#     reader = csv.reader(csvfile)
#     for row in reader:
#         transcript = row[1]  # Предполагая, что второй столбец – транскрипция
#         sounds = transcript.strip().split()
#         unique_sounds.update(sounds)
#
# print("Уникальные звуки:")
# for sound in sorted(unique_sounds):
#     print(sound)

import pandas as pd


def process_csv_file(csv_file_path):
    # Чтение CSV-файла в DataFrame
    df = pd.read_csv(csv_file_path)

    # Проверка наличия необходимых столбцов
    if 'file' not in df.columns or 'transcription' not in df.columns:
        print("CSV-файл должен содержать столбцы 'file' и 'transcription'.")
        return [], []

    # 1а. Поиск строк, где в 'transcription' встречается слово 'transcript'
    mask_transcript = df['transcription'].str.contains('transcript', case=False, na=False)
    files_with_transcript = df.loc[mask_transcript, 'file']

    if not files_with_transcript.empty:
        print("Файлы, в которых 'transcript' встречается в столбце 'transcription':")
        print(files_with_transcript.tolist())
    else:
        print("Слово 'transcript' не найдено в столбце 'transcription'.")

    # 1б. Поиск полных дубликатов по столбцу 'transcription'
    duplicates_mask = df.duplicated(subset='transcription', keep=False)
    duplicates_df = df[duplicates_mask]

    duplicate_files = []
    if not duplicates_df.empty:
        # Группировка по 'transcription' и получение списка файлов-дубликатов
        duplicates_grouped = duplicates_df.groupby('transcription')
        for transcription, group in duplicates_grouped:
            filenames = group['file'].tolist()
            if len(filenames) > 1:
                # Добавляем все, кроме первого файла (его оставим)
                filenames_to_delete = filenames[1:]
                duplicate_files.extend(filenames_to_delete)

        if duplicate_files:
            print("Файлы-двойники, которые нужно удалить:")
            print(duplicate_files)
        else:
            print("Дубликатов не найдено.")
    else:
        print("Дубликатов не найдено в столбце 'transcription'.")

    # Возвращаем список файлов с 'transcript' и список файлов-двойников
    return files_with_transcript.tolist(), duplicate_files


import os


def delete_duplicate_files(duplicate_file_list, folder_path):
    total_files_deleted = 0
    for filename in duplicate_file_list:
        # Формируем пути к файлам
        base_filename, ext = os.path.splitext(filename)
        wav_file = base_filename + '.wav'
        textgrid_file = base_filename + '.TextGrid'

        # Полные пути к файлам
        original_file_path = os.path.join(folder_path, filename)
        wav_path = os.path.join(folder_path, wav_file)
        textgrid_path = os.path.join(folder_path, textgrid_file)

        # Удаляем файлы, если они существуют
        files_deleted = []
        for file_path in [original_file_path, wav_path, textgrid_path]:
            if os.path.exists(file_path):
                os.remove(file_path)
                files_deleted.append(file_path)

        if files_deleted:
            print(f"Удалены файлы для дубликата '{filename}':")
            for f in files_deleted:
                print(f"  {f}")
            total_files_deleted += 1
        else:
            print(f"Файлы для '{filename}' не найдены или уже были удалены.")

    print(f"Всего удалено дубликатов: {total_files_deleted}")


# # Укажите пути к вашим файлам
# csv_file_path = '/Users/oksanagoncarova/Desktop/ipynb/new.csv'
# folder_path = '/Users/oksanagoncarova/Рабочий стол/работа/И РАН/Словарь волжского диалекта марийского языка 2/all_data'
#
# # Вызов первой функции для обработки CSV-файла
# files_with_transcript, duplicate_files = process_csv_file(csv_file_path)
#
# # Вы можете обработать файлы, содержащие 'transcript', по необходимости
# # Например, вывести их или записать в файл
#
# # Вызов второй функции для удаления файлов-дубликатов
# delete_duplicate_files(duplicate_files, folder_path)

mapping = {
    # Гласные
    'a': 'a',
    'a:': 'aː',
    'aa': 'aː',
    'á': 'a',
    'à': 'a',
    'á': 'a',
    'à': 'a',
    'ä': 'æ',
    'æ': 'æ',
    'æ:': 'æ',
    'ǽ': 'æ',
    'æ̀': 'æ',
    'e': 'e',
    'e:': 'eː',
    'é': 'e',
    'è': 'e',
    'é': 'e',
    'è': 'e',
    'i': 'i',
    'i:': 'iː',
    'í': 'i',
    'í': 'i',
    'o': 'o',
    'o:': 'oː',
    'ó': 'o',
    'ó': 'o',
    'u': 'u',
    'u:': 'uː',
    'ú': 'u',
    'ú': 'u',
    'ə': 'ə',
    'ɛ': 'ɛ',
    'ɛː': 'ɛː',
    'ɐ': 'ɐ',
    'ɐː': 'ɐː',
    'ɑ': 'ɑ',
    'ɑː': 'ɑː',
    'ɒ': 'ɒ',
    'ɒː': 'ɒː',
    'ɔ': 'ɔ',
    'ɔː': 'ɔː',
    'ø': 'ø',
    'ø:': 'øː',
    'œ': 'œ',
    'y': 'y',
    'yː': 'yː',
    'ɯ': 'ɯ',
    'ɨ': 'ɨ',
    'ʊ': 'ʊ',
    'ʊː': 'ʊ',
    'ʌ': 'ʌ',
    'ɤ': 'ɤ',
    'ɤ:': 'ɤː',
    'ɜ': 'ɜ',
    'ɜː': 'ɜː',
    'æ̈': 'æ',
    'ü': 'y',
    'ü:': 'yː',
    'ö': 'ø',
    'ö': 'ø',

    # Согласные
    'b': 'b',
    'b\'': 'b',
    'bʲ': 'b',
    'p': 'p',
    'p\'': 'p',
    'pʼ': 'p',
    't': 't',
    't\'': 't',
    'tʼ': 't',
    'd': 'd',
    'd\'': 'd',
    'dʲ': 'd',
    'k': 'k',
    'k\'': 'k',
    'kʼ': 'k',
    'g': 'ɡ',
    'g\'': 'ɡ',
    'gʲ': 'ɡ',
    'm': 'm',
    'm\'': 'm',
    'mʲ': 'm',
    'n': 'n',
    'n\'': 'n',
    'nʲ': 'n',
    'ŋ': 'ŋ',
    'ŋʲ': 'ŋ',
    'f': 'f',
    'v': 'v',
    'v\'': 'v',
    'vʲ': 'v',
    'θ': 'θ',
    'ð': 'ð',
    's': 's',
    's\'': 's',
    'sʲ': 's',
    'z': 'z',
    'z\'': 'z',
    'zʲ': 'z',
    'ʃ': 'ʃ',
    'ʒ': 'ʒ',
    'h': 'h',
    'x': 'x',
    'xʲ': 'x',
    'ʁ': 'ʁ',
    'l': 'l',
    'l\'': 'l',
    'lʲ': 'l',
    'r': 'r',
    'r\'': 'r',
    'rʲ': 'r',
    'j': 'j',
    'w': 'w',
    'w\'': 'w',
    'wʲ': 'w',
    'ç': 'ç',
    'ʋ': 'ʋ',
    'ɹ': 'ɹ',
    'ɻ': 'ɻ',
    'ʍ': 'ʍ',
    'ɥ': 'ɥ',
    'ɕ': 'ɕ',
    'ʑ': 'ʑ',
    'ʂ': 'ʂ',
    'ʐ': 'ʐ',
    'ɦ': 'ɦ',
    'ʔ': 'ʔ',
    'ʡ': 'ʡ',
    'q': 'q',
    'q\'': 'q',
    'qʲ': 'q',
    'qʼ': 'qʼ',

    # Аффрикаты
    'tʃ': 'tʃ',
    'tʃʲ': 'tʃ',
    'dʒ': 'dʒ',
    'dʒʲ': 'dʒ',
    'ts': 'ts',
    'dz': 'dz',
    'tɕ': 'tɕ',
    'dʑ': 'dʑ',
    'tɕʲ': 'tɕ',
    'ʦ': 'ts',
    'ʣ': 'dz',
    'ʨ': 'tɕ',
    'ʥ': 'dʑ',
    'č': 'tʃ',
    'čč': 'tʃ',
    'š': 'ʃ',
    'šš': 'ʃ',
    'ž': 'ʒ',
    'k::': 'k',
    't:': 't',
    'r::': 'r',
    'h1': 'h',
    'h1#': 'h',
    'e::': 'ɜ',
    't::': 't',
    '7': 'œ',
    'l:': 'l',
    'r0': 'ɛ',
    'a::': 'a',
    'y::': 'ø',
    't1': 't',
    'v0': 'ɜ',
    '2::': 'o',
    'h::': 'h',
    't\'::': 'ø',
    'u::': 'u',
    'õ': 'œ',
    't#': 'ɯ',
    'n::': 'n',
    '2::': 'ʌ',
    't:%': 't',
    'k::': 'k',
    'k1': 'ɨ',
    'h::1': 'ɛ',
    's\'::': 's',
    'k::%': 'ɛ',
    'l0': 'ɘ',
    'N': 'ɵ',
    's1': 's',
    'k::#': 'k',
    'j0': 'ø',
    'e0+': 'œ',
'a+': 'ʌ',
    'o+': 'ɞ',
    'm+':'m',
    'e+': 'a',

    # Долгие согласные (геминирование)
    'pp': 'pː',
    'tt': 'tː',
    'kk': 'kː',
    'bb': 'bː',
    'dd': 'dː',
    'ɡɡ': 'ɡː',
    'mm': 'mː',
    'nn': 'nː',
    'ff': 'fː',
    'ss': 'sː',
    'ʃʃ': 'ʃː',
    'll': 'lː',
    'rr': 'rː',
    'vv': 'vː',
    'zz': 'zː',

    # Другие символы
    'ə': 'ə',
    'æ': 'æ',
    'ə': 'ə',
    'ç': 'ç',
    'ɟ': 'ɟ',
    'ʎ': 'ʎ',
    'ɲ': 'ɲ',
    'ɕ': 'ɕ',
    'ʑ': 'ʑ',
    'β': 'β',
    'ɣ': 'ɣ',
    'χ': 'χ',
    'ħ': 'ħ',
    'ʕ': 'ʕ',
    'ɐ': 'ɐ',
    'ɺ': 'ɺ',
    'ɧ': 'ɧ',
    'ʢ': 'ʢ',
    'ʜ': 'ʜ',
    'ʢ': 'ʢ',
    'ʘ': 'ʘ',
    'ǀ': 'ǀ',
    'ǁ': 'ǁ',
    'ǂ': 'ǂ',
    'ǃ': 'ǃ',
    'ɗ': 'ɗ',
    'ɓ': 'ɓ',
    'ʄ': 'ʄ',
    'ɠ': 'ɠ',
    'ʛ': 'ʛ',
    'ʼ': 'ʼ',
    'ɡ': 'ɡ',

    # Дифтонги и трифтонги
    'ai': 'aɪ',
    'ei': 'eɪ',
    'oi': 'oɪ',
    'au': 'aʊ',
    'eu': 'ɛʊ',
    'ui': 'uɪ',
    "\\ng": "ŋ",
    "b̪̚ˀ": "b",
    "d'ʒ'": "dʒ",
    "ḋ̺̪ː": "d",
    "ḋ̺̪ ᶭˀ": "d",
    "ḋ̺̪̪̬ᶭ": "d",
    "ḋ̺̪̪̬ᶭː": "d",
    "kːː’ʷ": "k",
    "l\\^j": "j",
    "l͇̠͚̈": "i",
    "ŏ́": "o",
    "p`": "p",
    "s": "s",
    "s̠ˁːː": "s",
    "s̪͢s͇ʲ₎͈": "s",
    "s̪̆͢s͇ʲ₎͈": "s",
    "s̺̪͢s̠ʲː": "s",
    "s̺̪͢s̺̪͢ˁː": "s",
    "s͇̻s͇̻ˁʷ": "s",
    "s͇̻s͇̻̆ˁʷ": "s",
    "s͇͢s͇ʲ": "s",
    "t'ʰ\\Uv": "t",
    "t\\0v": "t",
    "tt͡ʃ": "tʃ",
    "t͡ʃᵘ": "tʃ",
    "ŭ": "u",
    "ŭˀ": "u",
    "ŭ́": "u",
    "v'v'": "v",
    "w͡ʋᵝː": "w",
    "w͚͡ʋ͚ᵝ": "w",
    "yː": "y",
    "æ'": "æ",
    "æʶˑ": "æ",
    "æ̆́": "æ",
    "æ̘̈͡a̘ˀ": "æ",
    "æ̘̈͡a̘ˀːː": "æ",
    "æ̘̃ꟸ̆": "æ",
    "æ̙ˑ": "æ",
    "æ̹": "æ",
    "ð": "ð̠",
    "ð ̩": "ð̠",
    "ö'": "o",
    "ü'": "u",
    "üü": "u",
    "ƙ̆ʷ": "k",
    "ȶ͈͡ʃ̠̻ʷ": "tʃ",
    "ɜ̙̈̆": "ɜ",
    "ɜ̘̆ˡ": "ɜ",
    "ɜ̘͚ˁ": "ɜ",
    "ɜ̙": "ɜ",
    "ɜ̙ˑ": "ɜ",
    "ɜ̞ˑ": "ɜ",
    "ɜ̟͡ˀɭ̆͜ʟ̆": "ɜ",
    "ɜ̟͡ˀɭ̆͜ʟ̆ˀ": "ɜ",
    "ɜ̥̆": "ɜ",
    "с": "s"
}

unassigned_symbols = [
    "1]",
    "2]",
    "3]",
    "4]",
    "N",
    "Q̔͜ʜ̆ʰʷ",
    "Q͡ːθːʷ",
    "Q͡ːθ̟ːʷ",
    "[БАА:",
    "[БИН:",
    "[БИН]",
    "\\\\\\\\w",
    "\\^h",
    "\\ab",
    "\\ae",
    "\\ae\\'1\\:f",
    "\\ae\\:f",
    "\\aeu",
    "\\as\\:f",
    "\\cc",
    "\\cf",
    "\\ct",
    "\\ct\\:f",
    "\\dh\\^j",
    "\\ef",
    "\\h^",
    "\\hs",
    "\\hs\\'1\\:f",
    "\\i-",
    "\\lc\\-v",
    "\\nj",
    "\\o-",
    "\\o-\\:f",
    "\\o-u",
    "\\sw",
    "\\yc\\:f",
    "a\\:f",
    "b\\^w",
    "cˑʰ",
    "d'd'",
    "ḋ̺̪̬͡ːṫ̺̪ˀː",
    "e\\:f",
    "e̠͢ø̈",
    "ĩ̠̙̬ˑ",
    "i͡i˥˩",
    "jɔʹ",
    "k\\^j",
    "kːʖ",
    "k̚͡ːθ̇ːʷ",
    "k͡sᶭˑ",
    "l'l",
    "l'l'",
    "n'n'",
    "n̆͡й",
    "o\\:f",
    "o̝͡ɔˑ",
    "p\\^j",
    "q\\^?",
    "q\\^?\\^w",
    "qːːʰʷ",
    "q͡ʜ",
    "q͡ʡ",
    "r\\^j",
    "s\\^j",
    "t\\T^\\Uv",
    "t\\^h\\Uv",
    "t͡ɕ",
    "u\\:f",
    "x̆͡ʲç",
    "čč",
    "č́",
    "ħ͡ʜʶ",
    "œ̝̰̽",
    "ƥ̪̆",
    "ǘ",
    "ǯ",
    "ɐ˥˩",
    "ɐ̘ˑ",
    "ɐ̝͡æ̝̽",
    "ɐ̽",
    "ɐᵸ",
    "ɑu\\nv",
    "ɑ̘ˑ̰",
    "ɑ̟̘ʶ",
    "ɑ̟̘ʶˑ",
    "ɑ̟͚ˑ",
    "ɑ̟͡ʟ̆̚",
    "ɑ̟͡ꜝꜝʟ̆̚",
    "ɒ̹ʶˑ",
    "ɒ̆͡ᴀ̠̰ᵸ",
    "ɔɔ",
    "ɔ̃̃ʶˑ",
    "ɔ̘̆̆ˀ",
    "ɔ̞͚͜ːɔ̆ˡ",
    "ɔ̞͡ːɔ̞͚̃ː",
    "ɕ",
    "ɖ͇ː",
    "ɘ̝̆͡ˀɜ͚",
    "ɛi̯",
    "ɜ̙ˡ",
    "ɜ̙̆͡ʟ̆",
    "ɜ̙͡ˀɭ̆ʟ̆͜",
    "ɜ̝̽͡ˑu",
    "ɜ̟̃͡ˀɭ̆͜ʟ̆ˀ",
    "ɜ̹̙͡ˑɪ̝ʶˑ",
    "ɜ̹̙͡ˑɪ̝ˑ",
    "ɜ̹̙͡ˑɪ̝̙ˑ",
    "ɜ͚ˑ",
    "ɜ͡ɭ̈̆",
    "ɜ̞͡ɭ̈̆",
    "ɜ͚͡ɭ̈̆",
    "ɞ̝̆̆͡ʟ̆",
    "ɟ͡ð̠ʲ",
    "ɟ๋̆͡ð̠ʲ",
    "ɡ ʱꜞ",
    "ɡ̟̬ː",
    "ɡ̬͡ɢ̬ː",
    "ɢʲ",
    "ɢ̬ː",
    "ɤ̞̽̆",
    "ɨ'",
    "ɨ͡l",
    "ɨʹ",
    "ɪ̰̃ꜝꜝ",
    "ɪ̰̃ꜝꜝˑ",
    "ɪ̆ˁꟸ̇",
    "ɪ̰̆",
    "ɪ̝̃ːˑ",
    "ɪ̝̃͡i",
    "ɪ̝ ˑ",
    "ɪ̝̆͡",
    "ɪ̞̆",
    "ɪ̞͚ːː",
    "ɪ̞͚ˑ",
    "ɪ̟ꜝꜝːˑ",
    "ɪ̯̆ ͈ᶞ",
    "ɪ̯̆ ᶞ",
    "ɪ̯͡Ͷ",
    "ɪ͚ꟸ",
    "ɪᶞ",
    "ɪꟸ",
    "ɭ͇̃̆",
    "ɭᶭ",
    "ɱ̆́ʶ",
    "ɲɲ",
    "ɲ̠̞̆",
    "ɳ̆ᶭʷ",
    "ɳ͇ʷ",
    "ɳᶭ",
    "ɴʲ",
    "ɵ̝̆",
    "ɵ̠ᵝ",
    "ɶ",
    "ɶ:",
    "ɶː",
    "ɹ̆̃ˀ",
    "ɹ̆͢ɾ ̝",
    "ɺ͇̠̈͡ɜ̘ˡ",
    "ɺ͇̠̈͡ɺ͇̠̈͡ɺ͇̠̈",
    "ɺ̢͇̃",
    "ɾ̈͡ɹ̈̆",
    "ɾ͡ɾᶭ",
    "ʃʲʃʲ",
    "ʈˑᶭ",
    "ʈ͇͉ʷ",
    "ʉ̞̆ᶞ",
    "ʉ̠̆₎̥",
    "ʉ͚̟ˑˀ",
    "ʊ\\:^",
    "ʊ̃̆̆",
    "ʊ̃̆͡ʊ",
    "ʊ̞̃̈ˡˑ",
    "ʊ̃͡ʊ̠",
    "ʊ̝̹̆̆",
    "ʊ̠ˀˑ",
    "ʊ̠̃ːˑ",
    "ʊ̠̆̆̃",
    "ʊ̠͚ˑ",
    "ʊ̠͚͚͡ˑʊ̠̝͚͚̃ː",
    "ʊ̹ᶞ",
    "ʊ̝̽̆",
    "ʊ̽ᵝˀᶞˑ",
    "ʋ̩̃̃",
    "ʌ̞̽",
    "ʏ̆͡ʉ͚̟ˀ",
    "ʏ̝ːː",
    "ʏ̝̆͡ʉ̆",
    "ʏ͚̝ˀ",
    "ʔ͡k̠ᵡ",
    "ʔ͡ʡː͡ᴤ",
    "ʔ͡ːᴤ̆",
    "ʔ᷂",
    "ʔ᷂ːː’",
    "ʔꜝꜝ’ː",
    "ʖʶ",
    "ʖꜝꜝˤˑ",
    "ʚ",
    "ʚʹ",
    "ʛːː",
    "ʜʲ",
    "ʜ̣ꜝꜝ",
    "ʜ͢ʶɦ̥ʶ",
    "ʝ̰",
    "ʟ̥̚",
    "ʡ",
    "ʡ̆",
    "ʡᵊ",
    "ʡ’",
    "ʢ͉̆",
    "ʤʲ",
    "ʥ",
    "ʥ'",
    "ʨ",
    "ʨ'",
    "ʨʨ",
    "ˀæ̙ː",
    "ˀɐ̝ːˑ",
    "ˀɐ̝̙ːː",
    "ˀʈ̪ʷ",
    "ˀʋ",
    "ˀχʲ",
    "ˀⁿɡ̟̬ː",
    "ˀⁿɡ͡ɢːˑ",
    "ːḋ̺̪̪̬ˀᶭː",
    "ˡɞ",
    "ˤq",
    "ˤɐ",
    "̬ʔ͡ʖ",
    "̬ʔ͡ʡː͡ᴤ",
    "̬ʔ͡ːᴤ",
    "̬ʔ̰͡ʖ",
    "͚͉",
    "͚͉ɟ̟̬ːʷ",
    "͚͉ɟ̬ːʱ",
    "͚͉ⁿˑɟ̟̬ʷː",
    "ͧ",
    "Ͷ̰̆",
    "έ",
    "έ:",
    "β",
    "βʲ",
    "β͜w",
    "γ",
    "δ",
    "ε",
    "θ",
    "θ̆͢s̺̪",
    "χ",
    "ϣ̝͡ϣ̝ʷ",
    "а",
    "г̙̆",
    "г̘ ˀ",
    "г̠͔͉͡ʎ̝̆",
    "ӗ",
    "иˑᴳ",
    "йˀ",
    "и̩",
    "и̩͡ʷꜦː",
    "и̩͡ʷꜦˑ",
    "и͜ʔ",
    "х",
    "ә",
    "ᴀʶʶːːː",
    "ᴀːː",
    "ᴀ̆͡ᴀ͚͚ːˑ",
    "ᴀ̘̈",
    "ᴀ̘̈̆",
    "ᴀ̘̈̆ˀ",
    "ᴀ̘̈̆",
    "ᴀ̘͡ˑăˀ",
    "ᴀ̠̙ːˑ",
    "ᴀ̠̙ːˑɪ̝",
    "ᴀ̠͚ːˑɪ̝͚ˑ",
    "ᴀ͚ːˑ",
    "ᴀ͚̘",
    "ᴀ͚̹͡ă",
    "ᴊ",
    "ᴤ",
    "ᴤ̆",
    "ᵓ",
    "ᵗθ͇͉ꟹˑ",
    "ᶦˁꟸ̇",
    "ḷ",
    "ṇ",
    "ⁿȡ̬ːʷ",
    "ⁿɟ̟̬ᶽ",
    "ⁿɠ̠ː",
    "ⁿɡ̟̬ː",
    "ⁿɡ̬ˀˑ",
    "ⁿɡ͡ɢ̬ːˀ",
    "ⁿɡ͡ ɢ̥ː",
    "Ꜧ̆",
    "Ꜧ͡ȵ͡ɱʶ"
]

import os

from textgrid import IntervalTier, TextGrid


def process_textgrids(folder_path, mapping, unassigned_symbols):
    total_files = 0
    total_files_deleted = 0
    total_intervals = 0
    total_intervals_modified = 0
    total_intervals_deleted = 0

    for filename in os.listdir(folder_path):
        if filename.endswith(".TextGrid"):
            total_files += 1  # Увеличить счётчик файлов
            textgrid_path = os.path.join(folder_path, filename)
            # Загрузить TextGrid
            tg = TextGrid()
            tg.read(textgrid_path)
            modified = False  # Флаг для проверки, были ли изменены интервалы
            intervals_in_file = 0
            intervals_deleted_in_file = 0
            intervals_modified_in_file = 0
            new_tiers = []

            for tier in tg.tiers:
                if isinstance(tier, IntervalTier):
                    new_intervals = []
                    for interval in tier.intervals:
                        total_intervals += 1  # Увеличить общий счётчик интервалов
                        intervals_in_file += 1
                        symbol = interval.mark.strip()
                        if symbol in mapping:
                            # Отобразить символ на его новое значение
                            if interval.mark != mapping[symbol]:
                                intervals_modified_in_file += 1
                                total_intervals_modified += 1
                                interval.mark = mapping[symbol]
                            new_intervals.append(interval)
                        elif symbol in unassigned_symbols:
                            # Удалить интервал (не добавлять в new_intervals)
                            modified = True
                            intervals_deleted_in_file += 1
                            total_intervals_deleted += 1
                            continue
                        else:
                            # Символ не в mapping и не в unassigned_symbols; удалить интервал
                            modified = True
                            intervals_deleted_in_file += 1
                            total_intervals_deleted += 1
                            continue
                    # Если остались интервалы, добавить новый уровень
                    if new_intervals:
                        new_tier = IntervalTier(name=tier.name, minTime=tier.minTime, maxTime=tier.maxTime)
                        for interval in new_intervals:
                            new_tier.add(interval.minTime, interval.maxTime, interval.mark)
                        new_tiers.append(new_tier)
                else:
                    # Для уровней, не являющихся IntervalTier, оставить как есть
                    new_tiers.append(tier)

            # Посчитать общее количество интервалов во всех уровнях
            total_intervals_in_tiers = sum(len(tier.intervals) for tier in new_tiers if isinstance(tier, IntervalTier))
            if total_intervals_in_tiers < 2:
                # Удалить файл TextGrid и соответствующий WAV-файл
                os.remove(textgrid_path)
                wav_filename = filename.replace(".TextGrid", ".wav")
                wav_path = os.path.join(folder_path, wav_filename)
                if os.path.exists(wav_path):
                    os.remove(wav_path)
                total_files_deleted += 1
            else:
                # Сохранить измененный TextGrid
                tg.tiers = new_tiers
                tg.write(textgrid_path)

    # Возврат статистики
    stats = {
        "total_files": total_files,
        "total_files_deleted": total_files_deleted,
        "total_intervals": total_intervals,
        "total_intervals_modified": total_intervals_modified,
        "total_intervals_deleted": total_intervals_deleted
    }
    return stats


# folder_path = '/Users/oksanagoncarova/Рабочий стол/работа/И РАН/Словарь/Новая папка'
# stats = process_textgrids(folder_path, mapping, unassigned_symbols)
# print("Обработано файлов:", stats["total_files"])
# print("Удалено файлов:", stats["total_files_deleted"])
# print("Всего интервалов:", stats["total_intervals"])
# print("Изменено интервалов:", stats["total_intervals_modified"])
# print("Удалено интервалов:", stats["total_intervals_deleted"])

import os


def rename_files_in_folder(folder_path):
    # Получаем список всех файлов в папке
    files_in_folder = os.listdir(folder_path)

    # Создаем словари для файлов .wav и .TextGrid с базовыми именами в качестве ключей
    wav_files = {}
    textgrid_files = {}

    # Проходим по всем файлам и заполняем словари
    for file_name in files_in_folder:
        base_name, ext = os.path.splitext(file_name)
        ext = ext.lower()
        if ext == '.wav':
            wav_files[base_name] = file_name
        elif ext == '.textgrid':
            textgrid_files[base_name] = file_name

    # Находим общие базовые имена, которые есть и в wav, и в TextGrid файлах
    common_basenames = sorted(set(wav_files.keys()) & set(textgrid_files.keys()))

    if not common_basenames:
        print("Не найдено соответствующих пар файлов для переименования.")
        return

    # Переименовываем файлы
    print("Начало переименования файлов...")
    for idx, base_name in enumerate(common_basenames, start=1):
        new_base_name = f"w_{idx}"

        old_wav_path = os.path.join(folder_path, wav_files[base_name])
        new_wav_name = f"{new_base_name}.wav"
        new_wav_path = os.path.join(folder_path, new_wav_name)

        old_textgrid_path = os.path.join(folder_path, textgrid_files[base_name])
        new_textgrid_name = f"{new_base_name}.TextGrid"
        new_textgrid_path = os.path.join(folder_path, new_textgrid_name)

        # Переименовываем файлы
        os.rename(old_wav_path, new_wav_path)
        os.rename(old_textgrid_path, new_textgrid_path)

        print(f"Переименовано: {wav_files[base_name]} -> {new_wav_name}")
        print(f"Переименовано: {textgrid_files[base_name]} -> {new_textgrid_name}")

    print("Переименование файлов завершено.")


# folder_path = '/Users/oksanagoncarova/Рабочий стол/работа/И РАН/Словарь волжского диалекта марийского языка 2/Новая папка'
# rename_files_in_folder(folder_path)


import os
import shutil


def merge_subfolders(parent_folder_path):
    # Проверяем, существует ли заданная папка
    if not os.path.isdir(parent_folder_path):
        print(f"Путь {parent_folder_path} не является каталогом или не существует.")
        return

    # Создаем путь к папке all_data
    all_data_path = os.path.join(parent_folder_path, 'all_data')

    # Создаем папку all_data, если она еще не существует
    if not os.path.exists(all_data_path):
        os.makedirs(all_data_path)
        print(f"Создана папка: {all_data_path}")
    else:
        print(f"Папка {all_data_path} уже существует.")

    # Получаем список всех элементов в родительской папке
    items_in_parent = os.listdir(parent_folder_path)

    # Фильтруем только папки, исключая 'all_data'
    subfolders = [item for item in items_in_parent
                  if os.path.isdir(os.path.join(parent_folder_path, item)) and item != 'all_data']

    if not subfolders:
        print("Нет подпапок для объединения.")
        return

    # Проходим по каждой подпапке и перемещаем ее содержимое в all_data
    for subfolder in subfolders:
        subfolder_path = os.path.join(parent_folder_path, subfolder)
        print(f"Обработка папки: {subfolder_path}")

        for root, dirs, files in os.walk(subfolder_path):
            for file in files:
                source_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, subfolder_path)
                destination_dir = os.path.join(all_data_path, relative_path)

                # Создаем подкаталоги в all_data, если они есть в исходных папках
                if not os.path.exists(destination_dir):
                    os.makedirs(destination_dir)

                destination_file_path = os.path.join(destination_dir, file)

                # Проверяем на существование файла с таким же именем
                if os.path.exists(destination_file_path):
                    print(f"Файл {destination_file_path} уже существует и будет перезаписан.")
                # Перемещаем файл
                shutil.move(source_file_path, destination_file_path)

        # После перемещения файлов можно удалить пустую папку
        try:
            shutil.rmtree(subfolder_path)
            print(f"Удалена пустая папка: {subfolder_path}")
        except Exception as e:
            print(f"Ошибка при удалении папки {subfolder_path}: {e}")

    print("Объединение папок завершено.")


# parent_folder_path = '/Users/oksanagoncarova/Рабочий стол/работа/И РАН/Словарь волжского диалекта марийского языка 2'
# merge_subfolders(parent_folder_path)


# def remove_lines(file_path, line_numbers_to_remove):
#     # Чтение всех строк из файла
#     with open(file_path, 'r', encoding='utf-8') as f:
#         lines = f.readlines()

#     # Преобразование номеров строк в множество для быстрого поиска
#     lines_to_remove = set(line_numbers_to_remove)

#     # Создание списка строк, которые нужно сохранить
#     new_lines = []
#     for i, line in enumerate(lines, 1):
#         if i not in lines_to_remove:
#             new_lines.append(line)
#         else:
#             print(f"Removing line {i}: {line.strip()}")

#     # Запись оставшихся строк обратно в файл (или в новый файл)
#     with open(file_path, 'w', encoding='utf-8') as f:
#         f.writelines(new_lines)

#     print("Готово! Указанные строки удалены.")

# # if __name__ == "__main__":
# #     # Путь к вашему текстовому файлу
# #     file_path = 'positive_pairs4.txt'

# #     # Номера строк, которые нужно удалить
# #     line_numbers_to_remove = [472550,
# # 518908,
# # 544659,
# # 563016,
# # 589801,
# # 640204,
# # 640328,
# # 651003,
# # 667660,
# # 681037,
# # 700320,
# # 712227,
# # 865197,
# # 879591,
# # 886657,
# # 901569,
# # 949734,
# # 962873,
# # 969035,
# # ]

#     remove_lines(file_path, line_numbers_to_remove)

# def remove_lines_with_1sarvi(file_path):
#     try:
#         # Создаем резервную копию исходного файла
#         import shutil
#         backup_path = file_path + '.bak'
#         shutil.copy(file_path, backup_path)
#         print(f"Резервная копия создана: {backup_path}")

#         # Читаем все строки из файла
#         with open(file_path, 'r', encoding='utf-8') as file:
#             lines = file.readlines()

#         # Отфильтровываем строки, не содержащие '1sarvi'
#         filtered_lines = [line for line in lines if '1kalokci' not in line]

#         # Перезаписываем файл без строк с '1sarvi'
#         with open(file_path, 'w', encoding='utf-8') as file:
#             file.writelines(filtered_lines)
#         print(f"Файл обработан. Строки с '1sarvi' удалены.")
#     except Exception as e:
#         print(f"Произошла ошибка: {e}")

# # # Пример использования:
# # file_path = 'positive_pairs4.txt'  # Замените на путь к вашему файлу
# # remove_lines_with_1sarvi(file_path)
# import pandas as pd

# # Укажите путь к вашему файлу
# input_file = '/Users/oksanagoncarova/Downloads/CogNet-v1.0.tsv'


# # Чтение файла (укажите правильный разделитель)
# df = pd.read_csv(input_file, sep='\t')  # Замените sep на нужный разделитель

# # Извлекаем нужные столбцы
# words_df = df[['word 1', 'word 2']].copy()

# # Добавляем новый столбец со значением 1
# words_df['1'] = 1

# # Проверяем количество строк в датафрейме
# total_rows = len(words_df)
# print(f"Всего строк в файле: {total_rows}")

# # Определяем количество строк для добавления
# num_rows_to_add = min(500000, total_rows)

# # Получаем первые 500 тысяч строк
# subset_df = words_df.sample(n=num_rows_to_add, random_state=42)

# # Указываем путь к выходному файлу
# output_file = 'positive_pairs4.txt'

# # Записываем данные без заголовков и индексов, в режиме добавления
# with open(output_file, 'a', encoding='utf-8') as f:
#     subset_df.to_csv(f, sep='\t', index=False, header=False)


# print(f"{num_rows_to_add} строк добавлено в файл '{output_file}'.")

# import pandas as pd
#
# # Читаем CSV файл
# df = pd.read_csv('/Users/oksanagoncarova/Desktop/ipynb/transcriptions.csv')
#
# # Предположим, что нужный столбец называется 'путь'
# # Оставляем только часть строки после 'all_data/'
# df['file'] = df['file'].apply(lambda x: x.split('all_data/')[1] if 'all_data/' in x else x)
#
# # Сохраняем изменения в новый CSV файл
# df.to_csv('new.csv', index=False)


import os

from textgrid import IntervalTier, TextGrid


def remove_intervals_with_word(folder_path, word_to_remove):
    total_files_processed = 0
    total_files_deleted = 0
    total_intervals_processed = 0
    total_intervals_deleted = 0

    for filename in os.listdir(folder_path):
        if filename.endswith(".TextGrid"):
            total_files_processed += 1
            textgrid_path = os.path.join(folder_path, filename)
            # Загрузить TextGrid
            tg = TextGrid()
            tg.read(textgrid_path)
            modified = False
            new_tiers = []

            for tier in tg.tiers:
                if isinstance(tier, IntervalTier):
                    new_intervals = []
                    for interval in tier.intervals:
                        total_intervals_processed += 1
                        mark_normalized = interval.mark.strip().lower()
                        word_normalized = word_to_remove.strip().lower()
                        if word_normalized in mark_normalized:
                            # Удалить интервал (не добавлять в new_intervals)
                            modified = True
                            total_intervals_deleted += 1
                            continue
                        else:
                            new_intervals.append(interval)
                    # Если остались интервалы, добавить новый уровень
                    if new_intervals:
                        new_tier = IntervalTier(name=tier.name, minTime=tier.minTime, maxTime=tier.maxTime)
                        for interval in new_intervals:
                            new_tier.add(interval.minTime, interval.maxTime, interval.mark)
                        new_tiers.append(new_tier)
                else:
                    # Для уровней, не являющихся IntervalTier, оставить как есть
                    new_tiers.append(tier)

            # Посчитать общее количество интервалов во всех уровнях
            total_intervals_in_tiers = sum(len(tier.intervals) for tier in new_tiers if isinstance(tier, IntervalTier))
            if total_intervals_in_tiers < 2:
                # Удалить файл TextGrid и соответствующий WAV-файл
                os.remove(textgrid_path)
                wav_filename = filename.replace(".TextGrid", ".wav")
                wav_path = os.path.join(folder_path, wav_filename)
                if os.path.exists(wav_path):
                    os.remove(wav_path)
                total_files_deleted += 1
            else:
                # Сохранить измененный TextGrid
                tg.tiers = new_tiers
                tg.write(textgrid_path)

    # Вывод статистики
    print("Обработано файлов:", total_files_processed)
    print("Удалено файлов:", total_files_deleted)
    print("Обработано интервалов:", total_intervals_processed)
    print("Удалено интервалов:", total_intervals_deleted)

# folder_path = "/Users/oksanagoncarova/Рабочий стол/работа/И РАН/Словарь волжского диалекта марийского языка 2/all_data"
# word_to_remove = "transcript"
#
# remove_intervals_with_word(folder_path, word_to_remove)
