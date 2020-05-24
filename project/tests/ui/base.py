import pytest

class BaseCase:
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request):
        self.driver = driver
        self.config = config
        # self.login_page: LoginPage = request.getfixturevalue('login_page')

