import requests

from model.myapp_user import User, MysqlOrmConnection
from tests.api.api_test import TestAPIBase


class TestAPIDelUser(TestAPIBase):

    def test_happy_case(self, regular_user, mysql_session):
        self.logger.debug(f"regular_user {regular_user}")

        username = regular_user.username
        resp = self.myapp_client.delete_user(username)
        assert resp.status_code == 204

        user = MysqlOrmConnection().session.query(User).filter_by(username=username).first()

        self.logger.debug(f'user from db: {user}')
        assert user is None

    def test_user_not_exists(self, mysql_session, username):
        """
        Удаление несуществующего пользователя
        """
        user = mysql_session.query(User).filter_by(username=username).first()
        if user is not None:
            mysql_session.delete(user)

        resp = self.myapp_client.delete_user(username)
        assert resp.status_code == 404

    def test_too_long_username(self, long_username):
        """
        Проверка ограничений на кол-во символов в нике пользователя
        """
        resp = self.myapp_client.delete_user(long_username)
        assert resp.status_code == 400

    def test_unauthorized(self, username):
        """
        Если пользователь неавторизован, он не должен името доступа к апишке
        """

        old_session = self.myapp_client.req_session
        self.myapp_client.req_session = requests.Session()

        try:
            resp = self.myapp_client.delete_user(username)
            assert resp.status_code == 401
        finally:
            self.myapp_client.req_session = old_session

