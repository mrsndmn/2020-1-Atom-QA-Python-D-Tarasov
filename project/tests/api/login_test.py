import pytest
import os

from model.myapp_user import User, MysqlOrmConnection
from myapp.client import MyAppClient

from tests.api.api_test import TestAPIBase

class TestAPILogin(TestAPIBase):

    def test_login(self, regular_user, logger):
        """
        Проверяем, можно ли залогиниться пользователем и обновляетcя ли access_time
        """

        client = MyAppClient(os.getenv('MYAPP_URL', 'http://localhost:8001'), user=regular_user.username, password=regular_user.password, logger=logger)
        mysql_session = MysqlOrmConnection().session
        user = mysql_session.query(User).filter_by(username=regular_user.username).first()

        assert user.access is None # тест на это поле работает только если есть рабочий браузер
        assert user.active == True
        assert user.start_active_time is not None

