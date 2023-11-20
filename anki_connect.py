import re
from typing import List

import requests

from googletts import do_gtts

# Define the AnkiConnect endpoint
anki_url = "http://127.0.0.1:8765"
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


def notes_info(node_ids: List[str]):
    result = make_request(
        "notesInfo",
        {"notes": node_ids}
    )
    return result


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
    if example and not note['fields']['ExampleAudio']['value']:
        example = "。".join(re.findall(r'[\u4e00-\u9fff]+', note['fields']['Example']['value']))
        example_audio = do_gtts(example)
        should_update = True
    if not should_update:
        return

    hanzi = note['fields']['Hán tự']['value']
    if hanzi:
        hanzi_audio = do_gtts(hanzi)
        should_update = True

    if should_update:
        update_note_audio(note, hanzi_audio, example_audio)
        print(f"{note['noteId']} - done")


def update_sentence_audio(note: dict):
    should_update = False
    sentence_audio = None

    hanzi = note['fields']['Hán tự']['value']
    audio = note['fields']['Audio']['value']
    if hanzi and not audio:
        sentence_audio = do_gtts(hanzi)
        should_update = True

    if should_update:
        update_note_audio(note, sentence_audio, None)
        print(f"{note['noteId']} - done")
