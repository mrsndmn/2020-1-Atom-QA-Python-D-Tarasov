from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.manager import DriverManager

from .base import BasePage
from ui.locators.locators import MainPageLocators


class MainPage(BasePage):
    locators = MainPageLocators()

    def login(self, user, password):
        self.fill_input(self.locators.EMAIL_INPUT, user)
        self.fill_input(self.locators.PASSWORD_INPUT, password)
        self.click(self.locators.LOGIN_BUTTON)
        assert isinstance(self.driver, GeckoDriverManager)
        # self.driver.
        return

    # def go_to_python_events(self):
    #     self.click(self.locators.PYTHON_EVENTS)
    #     return PythonEventsPage(self.driver)
    #
    # def iframe_run_command(self, command, timeout=10):
    #     # enable interactive shell
    #     self.click(self.locators.START_SHELL)
    #
    #     # switch to main frame
    #     iframe = self.find(self.locators.MAIN_FRAME)
    #     self.driver.switch_to.frame(iframe)
    #
    #     # switch to console
    #     console = self.find(self.locators.CONSOLE)
    #     self.driver.switch_to.frame(console)
    #
    #     # switch to terminal
    #     terminal = self.find(self.locators.TERMINAL)
    #     self.driver.switch_to.frame(terminal)
    #
    #     # wait terminal ready
    #     self.find(self.locators.TERMINAL_READY, timeout=timeout)
    #
    #     # send command to terminal
    #     terminal_body = self.find(self.locators.IFRAME_BODY)
    #     terminal_body.send_keys(Keys.RETURN)
    #     terminal_body.send_keys(Keys.RETURN)
    #     terminal_body.send_keys(Keys.RETURN)
    #     terminal_body.send_keys(command + Keys.RETURN)
