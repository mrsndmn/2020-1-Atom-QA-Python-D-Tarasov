import pytest
import requests
import os

from model.myapp_user import User, MysqlOrmConnection
from myapp.client import MyAppClient

# длинное пользовательское имя
# неуникальность емайла, логина
# null в базе там, где, возможно, это не предусмотрели
# обновление последнего захода пользвоателя

import faker
from faker.providers import internet

fake = faker.Faker()


@pytest.mark.api
class TestAPIBase:
    myapp_client: MyAppClient

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, request, logger):
        self.myapp_client: MyAppClient = request.getfixturevalue('api_client')
        self.myapp_client.logger = logger
        self.logger = logger


class TestAPICreateUser(TestAPIBase):

    @pytest.mark.parametrize('username, password, email', [
        (fake.lexify('?'*16), fake.lexify('?'*255), fake.lexify('?'*52) + '@example.com'),  # граничный случай
    ])
    def test_positive_boundary(self, username, password, email):
        '''
        Логин, пароль и почта максимально допустимой длинны
        '''
        resp = self.myapp_client.add_user(username, password, email)
        assert resp.status_code == 201

    @pytest.mark.parametrize('badpassword, desc', [
        (fake.lexify('?'*256), 'Слишком длинный пароль'),
        ('еёюя', 'Кириллица запрещена'),
        ('1', 'Слишком короткий пароль'),
    ])
    def test_bad_username(self, username, badpassword, email, desc):
        '''
        Негативные кейсы по созданию пользователей.
        '''
        resp = self.myapp_client.add_user(username, badpassword, email)
        assert resp.status_code == 400, desc

    @pytest.mark.parametrize('badusername, desc', [
        (fake.lexify('?'*256), 'Слишком длинный логин'),
        (str(fake.random_number()), 'Ник, состоящий только из цифр должен быть запрещен (нужно для корректной работы vkapi)'),
        ('ёёёёёёеёюя', 'Кириллица запрещена'),
        ('1', 'Слишком короткий логин'),
    ])
    def test_bad_username(self, badusername, password, email, desc):
        '''
        Негативные кейсы по созданию пользователей.
        '''
        resp = self.myapp_client.add_user(badusername, password, email)
        assert resp.status_code == 400, desc


    @pytest.mark.parametrize('bademail, desc', [
        ('@', 'Невалидный email'),
        (fake.lexify(text='?'*53)+'@example.com' , 'Слишком длинная почта'),
    ])
    def test_bad_email(self, username, password, bademail, desc):
        '''
        Кейсы с невалидой почтой
        '''
        resp = self.myapp_client.add_user(username, password, bademail)
        assert resp.status_code == 400, desc

    def test_duplicate_full(self, username, password, email):
        """
        При повторном создании пользователя должна возвращаться ошибка 304, already exists
        """
        resp = self.myapp_client.add_user(username, password, email)
        resp = self.myapp_client.add_user(username, password, email)
        assert resp.status_code == 304

    def test_duplicate_username(self, username, password, email):
        """
        При создании пользователя с одинаковым username, должа возвращаться 304
        """
        resp = self.myapp_client.add_user(username, password, email)

        username = fake.user_name()
        resp = self.myapp_client.add_user(username, password, email)
        assert resp.status_code == 304

    def test_duplicate_email(self, username, password, email):
        """
        При создании пользователя с одинаковым email, должа возвращаться 304
        """
        resp = self.myapp_client.add_user(username, password, email)

        email = fake.ascii_email()
        resp = self.myapp_client.add_user(username, password, email)
        assert resp.status_code == 304

    def test_unauthorized(self, username, password, email):

        old_session = self.myapp_client.req_session
        self.myapp_client.req_session = requests.Session()

        try:
            resp = self.myapp_client.add_user(username, password, email)
            assert resp.status_code == 401
        finally:
            self.myapp_client.req_session = old_session

class TestAPIDelUser(TestAPIBase):

    def test_happy_case(self, regular_user, myqsl_session):
        self.logger.debug(f"regular_user {regular_user}")

        username = regular_user.username
        resp = self.myapp_client.delete_user(username)
        assert resp.status_code == 204

        user = MysqlOrmConnection().session.query(User).filter_by(username=username).first()
        self.logger.debug(f'user from db: {user}')
        assert user is None

    def test_user_not_exists(self, myqsl_session, username):
        """
        Удаление несуществующего пользователя
        """
        user = myqsl_session.query(User).filter_by(username=username).first()
        if user is not None:
            myqsl_session.delete(user)

        resp = self.myapp_client.delete_user(username)
        assert resp.status_code == 404

    def test_too_long_username(self, myqsl_session):
        """
        Проверка ограничений на кол-во символов в нике пользователя
        """

        long_username = fake.lexify('?'*17)
        resp = self.myapp_client.delete_user(long_username)
        assert resp.status_code == 400

        user = MysqlOrmConnection().session.query(User).filter_by(username=long_username).first()
        self.logger.debug(f'user from db: {user}')
        assert user is None


class TestAPIBlockUser(TestAPIBase):
    pass

    # resp = self.myapp_client.block_user(username)


class TestAPIUnBlockUser(TestAPIBase):
    pass

    # resp = self.myapp_client.unblock_user(username)



class TestAPIStatus(TestAPIBase):
    pass
    # resp = self.myapp_client.status()


