import time

from anki_connect import find_notes, notes_info, update_hanzi_audio, update_sentence_audio

if __name__ == '__main__':
    start_time = time.time()
    notes = find_notes('Chinese')
    notes_data = notes_info(notes)
    for note_info in notes_data:
        if note_info['modelName'] == 'Chinese-Tiếng Việt - Hán tự - Pinyin - Audio (and reverse card)':
            update_hanzi_audio(note_info)
        elif note_info['modelName'] == 'Chinese-Tiếng Việt-Hán tự (and reverse card)':
            update_sentence_audio(note_info)
    end_time = time.time()
    print(f"Finished in {end_time - start_time}s")
