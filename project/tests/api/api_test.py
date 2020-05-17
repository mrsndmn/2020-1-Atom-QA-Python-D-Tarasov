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

@pytest.mark.api
class TestAPI:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, request, logger):
        self.myapp_client: MyAppClient = request.getfixturevalue('api_client')
        self.myapp_client.logger = logger

    @pytest.mark.parametrize('username, password, email', [
        ('testqa', 'qatest', 'mrsndmn@example.com'),
        ('x' * 16, 'y'*255, 'z'*(52) + '@example.com'), # граничный случай
    ])
    def test_positive_create_user(self, username, password, email):
        '''
        Позитивные кейсы по созданию пользователей.
        '''
        resp = self.myapp_client.add_user(username, password, email)
        assert resp.status_code in [200, 304]

    @pytest.mark.parametrize('username, password, email, desc', [
        ('', '', '', 'Все поля пустые'),
        ('username', 'password', '@', 'email невалидный'),
        ('x' * 17, 'y'*5, 'example@example.com', 'Слишком длинный логин'),
        ('x' * 5, 'y'*256, 'example@example.com', 'Слишком длинный пароль'),
        ('x' * 5, 'y'*5, 'z'*(53) + '@example.com', 'Слишком длинная почта'),
    ])
    def test_negative_create_user(self, username, password, email, desc):
        '''
        Негативные кейсы по созданию пользователей.
        '''
        resp = self.myapp_client.add_user(username, password, email)
        assert resp.status_code == 400, desc