from selenium.webdriver.common.by import By

class MainPageLocators():
    EMAIL_INPUT = (By.ID, 'email')
    PASSWORD_INPUT = (By.ID, 'password')
    LOGIN_BUTTON = (By.XPATH, '//button[contains(text(), "LOG IN")]')

