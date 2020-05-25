import json
import requests
from urllib.parse import urljoin
import os

class VKAPIClient:
    def __init__(self, url=os.getenv('VKAPI_URL', 'http://localhost:8000'), logger=None):
        self.base_url = url
        self.logger = logger

        self.req_session = requests.Session()

    def _request(self, method, url, **kwargs) -> requests.Response:
        url = urljoin(self.base_url, url)

        parse_json = kwargs.pop('parse_json', False)

        if self.logger is not None:
            self.logger.info('Performing request:')
            self.logger.info(f'{method} {url}')
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

        if parse_json:
            return json.loads(response.content)

        return response

    def mock_user(self, shortname, vk_id):
        return self._request('PUT', '/vk_id/'+shortname, data={"data":vk_id})

    def get_vk_id(self, shortname):
        return self._request('GET', '/vk_id/'+shortname, parse_json=True)

