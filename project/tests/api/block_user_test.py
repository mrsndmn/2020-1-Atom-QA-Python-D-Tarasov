import requests

from model.myapp_user import User, MysqlOrmConnection
from myapp.client import MyAppClient

from tests.api.api_test import TestAPIBase

class TestAPIBlockUser(TestAPIBase):

    def test_too_long_username(self, long_username):
        """
        Проверка ограничений на кол-во символов в нике пользователя
        """
        resp = self.myapp_client.block_user(long_username)
        assert resp.status_code == 400

    def test_block(self, api_client, mysql_session, regular_user):
        """
        Блокировка одним пользователем другого пользователя
        """

        regular_user.access = 1
        mysql_session.commit()

        res = api_client.block_user(regular_user.username)
        assert res.status_code == 200

        user = MysqlOrmConnection().session.query(User).filter_by(username=regular_user.username).first()
        assert user.access == 0

    def test_block_himself(self, api_client, mysql_session, regular_user):
        """
        Проверка, что пользователь может сам себя заблокировать
        """

        regular_user.access = 1
        mysql_session.commit()

        res = api_client.block_user(api_client.user)
        assert res.status_code != 200

        user = MysqlOrmConnection().session.query(User).filter_by(username=regular_user.username).first()
        assert user.access == 0

    def test_block_can_not_login(self, mysql_session, regular_user, logger):
        """
        Заблокированный пользователь не должен иметь возможность залогиниться
        """
        regular_user.access = 0
        mysql_session.commit()
        client = MyAppClient(logger=logger)

        resp = client.login(regular_user.username, regular_user.password)
        assert resp.status_code == 401


    def test_blocked_user_session_expires(self, mysql_session, api_client):
        """
        Если пользователь сначала логинется,
        а потом его блокируют, его сессия должна экспайриться
        """

        # api_client уже авторизован
        user = mysql_session.query(User).filter_by(username=api_client.user).first()
        user.access = 0
        mysql_session.commit()

        resp = api_client.login(api_client.user, api_client.password)
        assert resp.status_code == 401


    def test_unauthorized(self, username):
        """
        Если пользователь неавторизован, он не должен името доступа к апишке
        """

        old_session = self.myapp_client.req_session
        self.myapp_client.req_session = requests.Session()

        try:
            resp = self.myapp_client.block_user(username)
            assert resp.status_code == 401
        finally:
            self.myapp_client.req_session = old_session

