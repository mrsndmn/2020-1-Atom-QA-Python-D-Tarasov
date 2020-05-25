import pytest
import time
from tests.ui.base import BaseCase

from vkapi.client import VKAPIClient
from tests.ui.pages.base import BasePage


class TestWelcome(BaseCase):

    @pytest.mark.fixture(scope='class', autouse=True)
    def setup(self):
        self.vkapi_client = VKAPIClient()


    @pytest.mark.parametrize('xss_vk_id', [
        '<script> alert(1) </script>',
        '123321',
        '123321',
    ])
    def test_welcome_vk_id(self, login_page, regular_user, xss_vk_id):
        self.vkapi_client.mock_user(regular_user.username, xss_vk_id)

        welcome_page = login_page.login(regular_user.username, regular_user.password)

        assert f'VK ID: {xss_vk_id}' in welcome_page.user_info().text

    def test_logout(self, welcome_page):
        welcome_page.logout()
        time.sleep(0.5)
        assert '/login' in welcome_page.driver.current_url
