import requests
from urllib.parse import urljoin

class MyAppClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def _request(self, method, url, **kwargs):
        url = urljoin(self.base_url, url)
        return requests.request(method, url, **kwargs)

    def add_user(self, username, password, email) -> requests.Response:
        return self._request('POST', '/api/add_user', json={"username": username,"password": password,"email": email})

    def delete_user(self, username):
        # это плохо удалять пользователей с помощью метода GET
        return self._request('GET', f"/api/del_user/{username}")

    def block_user(self, username):
        return self._request('GET', f"/api/block_user/{username}")

    def unblock_user(self, username):
        return self._request('GET', f"/api/accept_user/{username}")

    def status(self):
        return self._request('GET', '/status')
