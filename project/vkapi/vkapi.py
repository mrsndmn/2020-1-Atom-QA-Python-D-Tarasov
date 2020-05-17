from flask import Flask

import vk_api
import os
import re

from dotenv import load_dotenv
load_dotenv()

VK_API_TOKEN = os.getenv("VK_API_TOKEN")
if VK_API_TOKEN == "":
    raise ValueError("VK_API_TOKEN env variable is required")

vk_session = vk_api.VkApi(token=VK_API_TOKEN)

print(vk_session.method('users.get', values={"user_ids": "mrsndmn"}))


app = Flask(__name__)

host = '0.0.0.0'
port = os.getenv("PORT", 8000)

@app.route('/vk_id/<shortname>')
def get_user_id_by_shortname(shortname: str):
    if re.match(r'^\d+$', shortname):
        return {}

    # в id должны быть только буквы, цифры и "_"
    if not re.match(r'^[a-zA-Z0-9_]+$', shortname):
        return {}

    try:
        res = vk_session.method('users.get', values={"user_ids": "mrsndmn"})

        if isinstance(res, list) and len(res) > 0:
            return {"vk_id": res[0]['id']}

        return
    except Exception as e:
        print("Can't get user id by shortname:", e)

    return {}


if __name__ == '__main__':
    app.run(host=host, port=port)