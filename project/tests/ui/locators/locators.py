from selenium.webdriver.common.by import By

class LoginPageLocators():

    USERNAME_INPUT = (By.ID, 'username')
    PASSWORD_INPUT = (By.ID, 'password')
    LOGIN_BUTTON = (By.ID, 'submit')

    ERROR_FIELD = (By.ID, 'flash')

class RegisterPageLocators():
    pass

class MainPageLocators():
    SOCIAL_ACTION_CONVERSION_BUTTON = (By.XPATH, "//div[contains(text(), 'Действия в социальных сетях')]")
    LINK_INPUT = (By.XPATH, '//input[@placeholder="Введите ссылку"]')
    BANNER_TITLE_INPUT = (By.XPATH, '//input[@data-gtm-id="banner_form_title"]')

    BANNER_DESCRIPTION_INPUT = (By.XPATH, '//textarea[@data-gtm-id="banner_form_text"]')

    BANNER_LITTLE_IMG_INPUT = (By.XPATH, '//input[@type="file" and @data-gtm-id="load_image_btn_256_256"]')
    BANNER_BIG_IMG_INPUT = (By.XPATH, '//input[@type="file" and @data-gtm-id="load_image_btn_1080_607"]')
    BANNER_IMG_SUBMIT_INPUT = (By.XPATH, '//input[@type="submit"]')

    SUBMIT_NEW_CAMPAIGN = (By.XPATH, '//div[@class="footer"]//button[@data-class-name="Submit"]')