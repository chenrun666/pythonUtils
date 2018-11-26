import os

from aip import AipSpeech

APP_ID = ''
API_KEY = ''
SECRET_KEY = ''

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


def text_tran_audio(text):
    result = client.synthesis(text, 'zh', 1, {
        'vol': 5,
        'per': 4,
    })
    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        with open('auido.mp3', 'wb') as f:
            f.write(result)


def audio_tran_text(filepath):
    os.system(f"ffmpeg -y  -i {filepath}  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 {filepath}.pcm")

    with open(f"{filepath}.pcm", 'rb') as fp:
        res = client.asr(fp.read(), 'pcm', 16000, {
            'dev_pid': 1536,
        })
    return res.get("result")[0]


data = audio_tran_text("hisuncle.m4a")
text_tran_audio(data)
