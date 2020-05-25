
from tests.ui.pages.base import BasePage
from tests.ui.locators.locators import RegisterPageLocators
import json

class RegistretionPage(BasePage):
    locators = RegisterPageLocators

    def register(self, username, email, password, confirm_password=None, accept_sdet_checkbox=True):

        if confirm_password is None:
            confirm_password = password

        self.fill_input(self.locators.USERNAME_INPUT, username)
        self.fill_input(self.locators.EMAIL_INPUT, email)
        self.fill_input(self.locators.PASSWORD_INPUT, password)
        self.fill_input(self.locators.CONFIRM_PASSWORD_INPUT, confirm_password)

        if accept_sdet_checkbox:
            self.click(self.locators.ACCEPT_SDET_CHECKBOX)

        self.click(self.locators.REGISTER_BUTTON)

    def error(self):
        err = self.find(self.locators.ERROR_FIELD)
        text: str = err.text
        text = text.replace("'", '"')

        res = text

        try:
            res = json.loads(text)
        except Exception:
            pass

        return res

    def move_to_login(self):
        return self.click(self.locators.LOGIN_BUTTON)