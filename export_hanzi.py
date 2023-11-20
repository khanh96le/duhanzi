from anki_connect import find_notes, notes_info

if __name__ == '__main__':
    hanzi_list = []

    notes = find_notes('Chinese')
    notes_data = notes_info(notes)
    for note_info in notes_data:
        if note_info['modelName'] != 'Chinese-Tiếng Việt - Hán tự - Pinyin - Audio (and reverse card)':
            continue
        hanzi = note_info['fields']['Hán tự']['value']
        if len(hanzi) > 3:
            continue
        hanzi_list.append(hanzi)
    print('Len = ', len(hanzi_list))
    print(hanzi_list)
