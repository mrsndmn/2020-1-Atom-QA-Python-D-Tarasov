import pytest
from webdriver_manager.firefox import GeckoDriverManager

from ui.pages.main import MainPage

class BaseCase:
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request):
        self.driver: GeckoDriverManager = driver
        self.config = config
        self.main_page: MainPage = request.getfixturevalue('main_page')
