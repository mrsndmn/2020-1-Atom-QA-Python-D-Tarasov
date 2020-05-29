from tests.api.api_test import TestAPIBase
from model.myapp_user import User, MysqlOrmConnection


class TestAPIUnBlockUser(TestAPIBase):

    def test_too_long_username(self, long_username):
        """
        Проверка ограничений на кол-во символов в нике пользователя
        """
        resp = self.myapp_client.unblock_user(long_username)
        assert resp.status_code == 400

    def test_unblock(self, api_client, mysql_session, regular_user, logger):
        """
        Метод разблокировки снимает флажок access
        """
        logger.debug(f"regular_user {regular_user}")
        regular_user.access = None
        mysql_session.commit()

        res = api_client.unblock_user(regular_user.username)
        assert res.status_code == 200

        user = MysqlOrmConnection().session.query(User).filter_by(username=regular_user.username).first()
        assert user.access == 1

