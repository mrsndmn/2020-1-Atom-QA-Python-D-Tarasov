
from tests.ui.pages.base import BasePage
from tests.ui.locators.locators import LoginPageLocators

class LoginPage(BasePage):
    locators = LoginPageLocators()

    def login(self, user, password):
        self.fill_input(self.locators.USERNAME_INPUT, user)
        self.fill_input(self.locators.PASSWORD_INPUT, password)
        self.click(self.locators.LOGIN_BUTTON)
        return

    def test_bad_login(self, driver, login_page, logger):
        login_page.login("no_such_email@example.com", "no_such_password")
        logger.debug(f"driver.current_url {driver.current_url}")

        error_desc = self.find(self.locators.ERROR_FIELD, timeout=2)
        
        error_desc

        assert 'error_code' in driver.current_url
