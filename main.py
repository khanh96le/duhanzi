import requests

from googletts import do_gtts

# Define the AnkiConnect endpoint
anki_url = "http://127.0.0.1:8765"


def make_request(action, params, version=6):
    return requests.post(
        anki_url,
        json={
            "action": action,
            "version": version,
            "params": params
        }
    ).json()['result']


# Request the list of cards in your deck
def find_cards(deck_name):
    return make_request(
        "findCards",
         {"query": f"deck:{deck_name}"}
    )


def find_notes(deck_name):
    return make_request(
        "findNotes",
        {"query": f"deck:{deck_name}"}
    )


def notes_info(node_id: str):
    result = make_request(
        "notesInfo",
        {"notes": [node_id]}
    )
    if not result:
        return []
    return result[0]


def update_note_audio(note: dict, audio_file: str):
    param_data = {
            "note": {
                "id": note["noteId"],
                "fields": {
                    "Audio": ""
                },
                "audio": [{
                    "url": f"http://localhost:8000/data/{audio_file}",
                    "filename": audio_file,
                    "fields": [
                        "Audio"
                    ]
                }]
            }
        }
    return make_request(
        action="updateNoteFields",
        params=param_data
    )


def update_hanzi_audio(note: dict):
    hanzi = note['fields']['Hán tự']['value']
    audio = do_gtts(hanzi)

    note['fields']['Audio']['value'] = audio
    result = update_note_audio(note, audio)
    print(f"{note['noteId']} - {result}")


notes = find_notes('Chinese')
for note_id in notes:
    note_info = notes_info(note_id)
    if note_info['modelName'] != 'Chinese-Tiếng Việt - Hán tự - Pinyin (and reverse card)':
        print(f"Skip {note_info}")
        continue
    update_hanzi_audio(note_info)



