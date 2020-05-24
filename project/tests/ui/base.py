import pytest

@pytest.mark.ui
class BaseCase:
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request, logger):
        self.driver = driver
        self.config = config
        self.logger = logger

        print("logger", logger)
        # self.login_page: LoginPage = request.getfixturevalue('login_page')

