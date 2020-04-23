from urllib.parse import urljoin

import requests
from requests.cookies import cookiejar_from_dict


class ResponseStatusCodeException(Exception):
    pass


class RequestErrorException(Exception):
    pass


class MyTargetClient:

    def __init__(self, user, password):
        self.base_url = 'https://target.my.com'

        self.session = requests.Session()
        self.csrf_token = None

        self.user = user
        self.password = password
        self.login()

    def _request(self, method, location, status_code=200, headers=None, params=None, data=None, json=None,
                 base_url=None, allow_redirects=True, with_csrf_token=False):

        if base_url is None:
            base_url = self.base_url

        if headers is None:
            headers = dict()
        if 'Referer' not in headers:
            headers['Referer'] = 'https://target.my.com/'

        if self.csrf_token is not None:
            headers['X-CSRFToken'] = self.csrf_token

        url = urljoin(base_url, location)
        print("mytarget req:", url)
        response = self.session.request(method, url, headers=headers, params=params, data=data,
                                        allow_redirects=allow_redirects, json=json)
        print("mytarget response:", response)
        print("resp headers:", response.headers)
        print("response.text", response.text)

        if response.status_code != status_code:
            raise ResponseStatusCodeException(f' Got {response.status_code} {response.reason} for URL "{url}"')

        if json is not None:
            json_response = response.json()
            return json_response
        return response

    def get_csrf_token(self):
        location = '/csrf/'
        headers = self._request('GET', location).headers
        return headers['Set-Cookie'].split(';')[0].split('=')[-1]

    def login(self):

        location = '/auth?lang=ru&nosavelogin=0'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        success_location = 'https://target.my.com/auth/mycom?state=target_login%3D1#email'
        data = {
            'email': self.user,
            'password': self.password,
            'continue': success_location,
            'failure': 'https://account.my.com/login/',
        }

        response = self._request('POST', location, headers=headers, data=data,
                                 base_url="https://auth-ac.my.com", allow_redirects=False, status_code=302)

        assert response.headers['Location'] == success_location
        assert 'Set-Cookie' in response.headers

        self.csrf_token = self.get_csrf_token()

        return

    def new_segment(self, segment_name):

        seg_json = {"name": segment_name, "pass_condition": 1,
                    "relations": [
                        {"object_type": "remarketing_player", "params": {"type": "positive", "left": 365, "right": 0}},
                        {"object_type": "remarketing_payer", "params": {"type": "positive", "left": 365, "right": 0}},
                    ], "logicType": "or"}
        location = '/api/v2/remarketing/segments.json?fields=relations__object_type,relations__object_id,relations__params,relations_count,id,name,pass_condition,created,campaign_ids,users,flags'
        return self._request('POST', location, json=seg_json)

    def del_segment(self, segment_id, status_code=204):
        location = 'api/v2/remarketing/segments/' + str(segment_id) + '.json'
        return self._request('DELETE', location, status_code=status_code)
