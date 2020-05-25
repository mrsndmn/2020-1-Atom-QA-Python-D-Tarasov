import pytest
import time
from tests.ui.base import BaseCase


class TestLogin(BaseCase):

    def test_happy_case(self, login_page, regular_user):
        """
        Успешный логин пользователя
        """
        login_page.login(regular_user.username, regular_user.password)
        assert '/welcome/' in login_page.driver.current_url

        # todo check regular_user updated, active

    @pytest.mark.parametrize("username", ['1', '12345'])
    def test_short_username(self, login_page, username):
        """
        Имя пользователя слишком короткое
        """
        login_page.login(username, '1')

        assert '/login' in login_page.driver.current_url
        time.sleep(0.5)
        error = login_page.login_error()
        assert error == 'Incorrect username length'

    def test_invalid_username(self, login_page, mysql_session, regular_user):
        """
        Имя пользователя
        """
        mysql_session.delete(regular_user)
        mysql_session.commit()

        login_page.login(regular_user.username, regular_user.password)

        assert '/login' in login_page.driver.current_url
        time.sleep(0.5)
        error = login_page.login_error()
        assert error == 'Invalid username or password'

    def test_register_button(self, login_page):
        """
        При клике на кнопку регистрации нудно перекидывать на страницу регистрации
        """
        registration_page = login_page.move_to_regiter()
        assert '/reg' in registration_page.driver.current_url

    def test_login_blocked_user(self, login_page, regular_user, mysql_session):
        """
        Если пользователя заблокировали, он не должен залогиниться
        """
        regular_user.access = 0
        mysql_session.commit()

        login_page.login(regular_user.username, regular_user.password)

        assert '/login' in login_page.driver.current_url
        time.sleep(0.5)
        error = login_page.login_error()
        assert error == 'Ваша учетная запись заблокирована'

