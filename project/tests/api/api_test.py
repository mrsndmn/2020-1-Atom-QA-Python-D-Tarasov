import pytest
import requests
import os

from model.myapp_user import User
from myapp.client import MyAppClient

# длинное пользовательское имя
# Длинный пароль
# длинный емейл
# логин null
# неуникальность емайла, логина
# null в базе там, где, возможно, это не предусмотрели
# обновление последнего захода пользвоателя

import faker
from faker.providers import internet

fake = faker.Faker()


@pytest.mark.api
class TestAPI:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, request, logger):
        self.myapp_client: MyAppClient = request.getfixturevalue('api_client')
        self.myapp_client.logger = logger


    @pytest.mark.parametrize('username, password, email', [
        (fake.lexify('?'*16), fake.lexify('?'*255), fake.lexify('?'*52) + '@example.com'),  # граничный случай
    ])
    def test_create_user_positive_boundary(self, username, password, email):
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
    def test_create_user_bad_username(self, username, badpassword, email, desc):
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
    def test_create_user_bad_username(self, badusername, password, email, desc):
        '''
        Негативные кейсы по созданию пользователей.
        '''
        resp = self.myapp_client.add_user(badusername, password, email)
        assert resp.status_code == 400, desc


    @pytest.mark.parametrize('bademail, desc', [
        ('@', 'Невалидный email'),
        (fake.lexify(text='?'*53)+'@example.com' , 'Слишком длинная почта'),
    ])
    def test_create_user_bad_email(self, username, password, bademail, desc):
        '''
        Кейсы с невалидой почтой
        '''
        resp = self.myapp_client.add_user(username, password, bademail)
        assert resp.status_code == 400, desc

    def test_create_user_duplicate(self, username, password, email):
        """
        При повторном создании пользователя должна возвращаться ошибка 304, already exists
        """
        resp = self.myapp_client.add_user(username, password, email)
        resp = self.myapp_client.add_user(username, password, email)
        assert resp.status_code == 304

    def test_create_user_unauthorized(self, username, password, email):

        old_session = self.myapp_client.req_session
        self.myapp_client.req_session = requests.Session()

        try:
            resp = self.myapp_client.add_user(username, password, email)
            assert resp.status_code == 401
        finally:
            self.myapp_client.req_session = old_session

