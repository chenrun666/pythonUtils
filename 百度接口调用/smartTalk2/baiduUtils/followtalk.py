import os

from uuid import uuid4

from aip import AipSpeech
from aip import AipNlp

from .robots import get_message

APP_ID = '14941465'
API_KEY = '9DrdmMkmHcieI6RWTqqGGRQ1'
SECRET_KEY = '3FmQ3ephXiuMxovwyTH90Cy7xeRi3q12'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
client_nlp = AipNlp(APP_ID, API_KEY, SECRET_KEY)


def text_tran_audio(text):
    filename = uuid4()
    result = client.synthesis(text, 'zh', 1, {
        'vol': 5,
        'per': 4,
    })
    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        with open(f'{filename}.mp3', 'wb') as f:
            f.write(result)
    return f"{filename}.mp3"


def audio_tran_text(filepath):
    os.system(f"ffmpeg -y  -i {filepath}  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 {filepath}.pcm")

    with open(f"{filepath}.pcm", 'rb') as fp:
        res = client.asr(fp.read(), 'pcm', 16000, {
            'dev_pid': 1536,
        })
    return res.get("result")[0]


def my_nlp(text):

    if client_nlp.simnet("你叫什么名字", text).get("score") >= 0.7:
        return text_tran_audio("我的名字叫陈润")

    if client_nlp.simnet("你今年多大了", text).get("score") >= 0.7:
        return text_tran_audio("我今年9岁了")
    else:
        return text_tran_audio(get_message(text, "monkey"))
