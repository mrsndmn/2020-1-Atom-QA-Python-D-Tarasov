import requests
from urllib.parse import urljoin


class MyAppClient:
    def __init__(self, base_url, user="kirill", password="kirill_pass", logger=None):
        self.base_url = base_url
        self.logger = logger

        self.req_session = requests.Session()
        self.login(user, password)

    def _request(self, method, url, **kwargs) -> requests.Response:
        url = urljoin(self.base_url, url)

        if self.logger is not None:
            self.logger.info('Performing request:')
            self.logger.info(f'url: {url}')
            if "json" in kwargs:
                self.logger.info(f'json: {kwargs["json"]}')
            if "data" in kwargs:
                self.logger.info(f'data: {kwargs["data"]}')
            self.logger.info(f'other params: { { k: kwargs[k] for k in kwargs if k not in ["json", "data"]} }')
            self.logger.info('-' * 20 + '\n')

        response = self.req_session.request(method, url, **kwargs)

        if self.logger is not None:
            self.logger.info('Got response:')
            self.logger.info(f'Status code: {response.status_code}')
            self.logger.info(f'Content: {response.text}')
            self.logger.info('-' * 50 + '\n')

        return response

    def login(self, user, password, submit="Login"):
        self._request('POST', '/login', data={"username":user, "password":password, "submit":submit})

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
