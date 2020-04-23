import pytest
from webdriver_manager.firefox import GeckoDriverManager

from ui.pages.login import LoginPage

class BaseCase:
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request):
        self.driver: GeckoDriverManager = driver
        self.config = config
        self.login_page: LoginPage = request.getfixturevalue('login_page')

