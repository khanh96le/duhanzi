import os
import requests

from googletts import do_gtts

# Define the AnkiConnect endpoint
anki_url = "http://127.0.0.1:8765"
cwd = os.getcwd()
audio_file_server = "http://localhost:8000/data"


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


def update_note_audio(note: dict, audio_file: str, example_audio_file: str):
    audio_files = []
    if audio_file:
        audio_files.append(
            {
                "url": f"{audio_file_server}/{audio_file}",
                "filename": audio_file,
                "fields": [
                    "Audio"
                ]
            }
        )
    if example_audio_file:
        audio_files.append(
            {
                "url": f"{audio_file_server}/{example_audio_file}",
                "filename": example_audio_file,
                "fields": [
                    "ExampleAudio"
                ]
            }
        )

    param_data = {
        "note": {
            "id": note["noteId"],
                "fields": {
                    "Audio": "",
                    "ExampleAudio": "",
                },
                "audio": audio_files
            }
        }
    return make_request(
        action="updateNoteFields",
        params=param_data
    )


def update_hanzi_audio(note: dict):
    should_update = False
    hanzi_audio = None
    example_audio = None

    example = note['fields']['Example']['value']
    if example:
        example_audio = do_gtts(example)
        should_update = True
    if not should_update:
        return

    hanzi = note['fields']['Hán tự']['value']
    if hanzi:
        hanzi = note['fields']['Hán tự']['value']
        hanzi_audio = do_gtts(hanzi)
        should_update = True

    if should_update:
        update_note_audio(note, hanzi_audio, example_audio)
        print(f"{note['noteId']} - done")


notes = find_notes('Chinese')
for note_id in notes:
    note_info = notes_info(note_id)
    if note_info['modelName'] != 'Chinese-Tiếng Việt - Hán tự - Pinyin (and reverse card)':
        print(f"Skip {note_info['noteId']}")
        continue
    update_hanzi_audio(note_info)
