from flask import Flask
from flask import request, make_response

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


mock_override = dict()

@app.route('/vk_id/<shortname>', methods=['GET', 'PUT'])
def get_user_id_by_shortname(shortname: str):

    if request.method == 'PUT':
        mock_override[shortname] = request.form.get('data')
        return {}

    if shortname in mock_override:
        return { "vk_id": mock_override[shortname] }

    if re.match(r'^\d+$', shortname):
        return make_response("Shortname can't be a digits", 400)

    # в id должны быть только буквы, цифры и "_"
    if not re.match(r'^[a-zA-Z0-9_]+$', shortname):
        return make_response("Unallowed symbol in shortname", 400)

    try:
        res = vk_session.method('users.get', values={"user_ids": shortname})

        if isinstance(res, list) and len(res) > 0:
            return {"vk_id": res[0]['id']}

        return
    except Exception as e:
        return make_response("Internal server error", 500)

    return {}


if __name__ == '__main__':
    app.run(host=host, port=port)