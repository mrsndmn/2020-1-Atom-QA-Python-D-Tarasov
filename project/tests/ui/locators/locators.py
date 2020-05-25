from selenium.webdriver.common.by import By

class LoginPageLocators():

    USERNAME_INPUT = (By.ID, 'username')
    PASSWORD_INPUT = (By.ID, 'password')
    LOGIN_BUTTON = (By.ID, 'submit')

    ERROR_FIELD = (By.ID, 'flash')

    REGISTER_BUTTON = (By.XPATH, '//*[text()="Create an account"]')

class RegisterPageLocators():
    USERNAME_INPUT = (By.ID, 'username')
    EMAIL_INPUT = (By.ID, 'email')
    PASSWORD_INPUT = (By.ID, 'password')
    CONFIRM_PASSWORD_INPUT = (By.ID, 'confirm')
    ACCEPT_SDET_CHECKBOX = (By.ID, 'term')

    REGISTER_BUTTON = (By.ID, 'submit')
    ERROR_FIELD = (By.ID, 'flash')

    LOGIN_BUTTON = (By.XPATH, '//*[text()="Log in"]')


class WelcomePageLocators():
    LOGIN_NAME = (By.ID, 'login-name')
    LOGOUT_BUTTON = (By.ID, 'logout')
