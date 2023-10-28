from gtts import gTTS
import hashlib


def do_gtts(hanzi: str):
    hashed = hashlib.md5(hanzi.encode('utf-8')).hexdigest()

    file_name = f"{hashed}.mp3"
    gTTS(hanzi, lang="zh-CN").save(f"data/{file_name}")
    return file_name


do_gtts("你叫什么名字？")
