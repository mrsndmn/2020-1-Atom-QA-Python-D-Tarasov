
from tests.ui.pages.base import BasePage
from tests.ui.locators.locators import LoginPageLocators
from tests.ui.pages.registration import RegistrationPage

class LoginPage(BasePage):
    locators = LoginPageLocators()

    def login(self, user, password):
        self.fill_input(self.locators.USERNAME_INPUT, user)
        self.fill_input(self.locators.PASSWORD_INPUT, password)
        self.click(self.locators.LOGIN_BUTTON)
        return

    def login_error(self):
        error_desc = self.find(self.locators.ERROR_FIELD, timeout=10)
        return error_desc.text

    def move_to_regiter(self):
        self.click(self.locators.REGISTER_BUTTON)
        return RegistrationPage(self.driver, self.logger)

