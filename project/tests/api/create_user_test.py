import pytest
import requests

import faker
from faker.providers import internet

from tests.api.api_test import TestAPIBase

fake = faker.Faker()
faker.Faker.seed(0)


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

    def test_email_zero_byte(self, username, password, email: str):
        '''
        Если создать пользователя с нуль-байтом перед @ в почте, в базу он попадет без @
        '''
        email = email.replace("@", "\x00@")

        resp = self.myapp_client.add_user(username, password, email)
        assert resp.status_code == 400


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
        """
        Если пользователь неавторизован, он не должен името доступа к апишке
        """

        old_session = self.myapp_client.req_session
        self.myapp_client.req_session = requests.Session()

        try:
            resp = self.myapp_client.add_user(username, password, email)
            assert resp.status_code == 401
        finally:
            self.myapp_client.req_session = old_session
