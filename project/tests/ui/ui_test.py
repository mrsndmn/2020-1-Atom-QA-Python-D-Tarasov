import pytest
import time
from tests.ui.base import BaseCase

from tests.ui.pages.login import LoginPage


class TestLogin(BaseCase):

    def test_happy_case(self, login_page, regular_user):
        login_page.login(regular_user.username, regular_user.password)
        assert '/welcome/' in login_page.driver.current_url

    @pytest.mark.parametrize("username", ['1', '12345'])
    def test_short_username(self, login_page, username):
        login_page.login(username, '1')

        assert '/login' in login_page.driver.current_url
        error = login_page.login_error()
        assert error == 'Incorrect username length'

    def test_invalid_username(self, login_page, mysql_session, regular_user):
        mysql_session.delete(regular_user)
        mysql_session.commit()

        login_page.login(regular_user.username, regular_user.password)

        assert '/login' in login_page.driver.current_url
        error = login_page.login_error()
        assert error == 'Invalid username or password'
