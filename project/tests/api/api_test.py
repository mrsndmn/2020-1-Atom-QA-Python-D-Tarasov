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

    myapp_client = MyAppClient(os.getenv('MYAPP_URL', 'http://localhost:8001'))

    @pytest.mark.parametrize('username, password, email', [
        ('testqa', 'qatest', 'mrsndmn@example.com'),
        ('x' * 16, 'y'*255, 'z'*(52) + '@example.com'), # граничный случай
    ])
    def test_positive_create_user(self, username, password, email):
        '''
        Позитивные кейсы по созданию пользователей.
        '''
        resp = self.myapp_client.add_user(username, password, email)

        print(resp.json())
        assert resp.status_code == 200

    # def test_create_user(self, faker, myqsl_session, regular_user):