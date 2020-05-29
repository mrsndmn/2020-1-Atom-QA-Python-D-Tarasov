import pytest
import time
from tests.ui.base import BaseCase


class TestRegistration(BaseCase):

    def test_happy_case(self, registration_page, username, password, email):
        """
        Новый пользователь должен попасть на страницу welcome после регистрации
        """
        registration_page.register(username, email, password)
        assert '/welcome/' in registration_page.driver.current_url

    def test_error_no_checkbox(self, registration_page, username, password, email):
        """
        Если пользователь не поставил галочку, то ничего не происходит
        """
        registration_page.register(username, email, password, accept_sdet_checkbox=False)
        time.sleep(0.5)
        # todo честно говоря, не понятно, как потестить всплывашку
        assert '/reg' in registration_page.driver.current_url

    def test_passwords_mismatch(self, registration_page, username, password, email):
        """
        Должна отображаться ошибка, если пароли не совпадают
        """

        registration_page.register(username, email, password, confirm_password=password[1:])
        assert '/reg' in registration_page.driver.current_url
        time.sleep(0.5)
        err = registration_page.error()
        assert err == 'Passwords must match'

    def test_all_wrong(self, registration_page, username, password):
        """
        Слишком короткий логин, несовпали пароли, невалидный и слишком коротний emal. Все сообщения об ошибках должны вывестись
        """

        registration_page.register(username[:2], username[:1], password, confirm_password=password[1:])
        assert '/reg' in registration_page.driver.current_url
        time.sleep(0.5)
        err = registration_page.error()
        assert err == {'username': ['Incorrect username length'], 'email': ['Incorrect email length', 'Invalid email address'], 'password': ['Passwords must match']}


    def test_already_exists_user_same_username_email(self, registration_page, regular_user):
        """
        Пользователь с таким логином и почтой уже был зарегистрирован
        """
        registration_page.register(regular_user.username, regular_user.email, regular_user.password)
        time.sleep(0.5)
        err = registration_page.error()
        assert err == 'User already exist'

    def test_already_exists_user_email(self, registration_page, regular_user):
        """
        Пользователь с таким логином и почтой уже был зарегистрирован
        """
        registration_page.register(regular_user.username[1:], regular_user.email, regular_user.password)
        time.sleep(0.5)
        err = registration_page.error()
        assert err == 'User already exist'

    def test_already_exists_same_username(self, registration_page, regular_user):
        """
        Пользователь с таким логином уже был зарегистрирован
        """
        registration_page.register(regular_user.username, regular_user.email[1:], regular_user.password)
        time.sleep(0.5)
        err = registration_page.error()
        assert err == 'User already exist'

    def test_login_page(self, registration_page):
        """
        Кнопка перехода на страницу логина должна работать
        """
        registration_page.move_to_login()
        time.sleep(0.5)
        assert '/login' in registration_page.driver.current_url
