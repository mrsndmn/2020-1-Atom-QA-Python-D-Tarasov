
from .base import BasePage
from ui.locators.locators import MainPageLocators


class LoginPage(BasePage):
    locators = MainPageLocators()

    def login(self, user, password):
        self.fill_input(self.locators.EMAIL_INPUT, user)
        self.fill_input(self.locators.PASSWORD_INPUT, password)
        self.click(self.locators.LOGIN_BUTTON)
        return
