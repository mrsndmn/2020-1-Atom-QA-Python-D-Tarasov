import os

import pytest
import allure

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from tests.ui.pages.login import LoginPage
from tests.ui.pages.registration import RegistrationPage
from tests.ui.pages.welcome import WellcomePage

from tests.api.conftest import *

class UsupportedBrowserException(Exception):
    pass


@pytest.fixture(scope='function')
def login_page(driver, logger, config):
    url = config['url'] + '/login'
    driver.get(url)
    return LoginPage(driver, logger)

@pytest.fixture(scope='function')
def registration_page(driver, logger, config):
    url = config['url'] + '/reg'
    driver.get(url)
    return RegistrationPage(driver, logger)

@pytest.fixture(scope='function')
def welcome_page(login_page, regular_user):
    return login_page.login(regular_user.username, regular_user.password)



@pytest.fixture(scope='function')
def driver(config, logger):
    browser = config['browser']
    version = config['version']
    chrome_path = config['chrome_path']
    selenoid = config['selenoid']


    if selenoid != '':
        options = ChromeOptions()

        capabilities = {
            'acceptInsecureCerts': True,
            'browserName': browser,
            'version': version,
            "enableVideo": True
        }

        driver = webdriver.Remote(command_executor=f'http://{selenoid}/wd/hub/',
                                    options=options,
                                    desired_capabilities=capabilities)

        allure.dynamic.link(f'http://{selenoid}/video/{driver.session_id}.mp4', name='Browser record')

    else:
        if version is None:
            version = 'latest'

        if browser == 'chrome':
            options = ChromeOptions()
            options.binary_location = chrome_path

            manager = ChromeDriverManager(version=version)
            driver = webdriver.Chrome(executable_path=manager.install(), options=options)
        elif browser == 'firefox':
            manager = GeckoDriverManager(version=version)
            driver = webdriver.Firefox(executable_path=manager.install())
        else:
            raise UsupportedBrowserException(f'Usupported browser: "{browser}"')

    
    yield driver
    driver.close()

