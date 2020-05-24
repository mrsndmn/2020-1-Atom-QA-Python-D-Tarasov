import pytest
from tests.ui.base import BaseCase

from tests.ui.pages.login import LoginPage

@pytest.mark.UI
class TestLogin(BaseCase):

    def test_happy_login(self, login_page):

        login_page.login('karajones', 'karajones')
        # login_page.driver.
