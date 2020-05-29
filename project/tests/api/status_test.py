import requests

from tests.api.api_test import TestAPIBase


class TestAPIStatus(TestAPIBase):

    def test_status(self):
        """
        Проверка работоспособности приложения
        """
        resp = self.myapp_client.status()
        assert resp.status_code == 200
        assert resp.json() == {"status":"ok"}

    def test_status_unauthorized(self):
        """
        Проверка работоспособности приложения без авторизации
        """
        self.myapp_client.session = requests.Session()
        resp = self.myapp_client.status()
        assert resp.status_code == 200
        assert resp.json() == {"status":"ok"}
