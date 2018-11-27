import json

import requests

tuling = "a2a5f3a066ce46a083f6bfd454024747"
api_url = "http://openapi.tuling123.com/openapi/api/v2"


def get_message(message, userid):
    """
    接入到图灵机器人，传入文字，返回回答
    :param message:
    :param userid:
    :return:
    """
    req = {
        "perception":
            {
                "inputText":
                    {
                        "text": message
                    }
            },
        "userInfo":
            {
                "apiKey": tuling,
                "userId": userid
            }
    }

    http_post = requests.post(api_url, json=req)
    response = http_post.json()
    return response.get("results")[0]["values"]["text"]
