
from tests.ui.pages.base import BasePage
from tests.ui.locators.locators import WelcomePageLocators

class WellcomePage(BasePage):
    locators = WelcomePageLocators

    def logout(self):
        return self.click(self.locators.LOGOUT_BUTTON)

    def user_info(self):
        return self.find(self.locators.LOGIN_NAME)