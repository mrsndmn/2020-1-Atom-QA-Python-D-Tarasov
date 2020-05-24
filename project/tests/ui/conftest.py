import os

import pytest
import allure

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from tests.ui.pages.base import BasePage
from tests.ui.pages.login import LoginPage

from tests.api.conftest import *

class UsupportedBrowserException(Exception):
    pass


@pytest.fixture(scope='function')
def base_page(driver):
    return BasePage(driver)


@pytest.fixture(scope='function')
def login_page(driver, logger):
    return LoginPage(driver, logger)


@pytest.fixture(scope='function')
def logined_driver(driver, login_page):
    login_page.login(os.getenv("MYTARGET_USER"), os.getenv("MYTARGET_PASSWORD"))
    driver = login_page.driver
    return driver


@pytest.fixture(scope='function')
def driver(config, logger):
    browser = config['browser']
    version = config['version']
    chrome_path = config['chrome_path']
    url = config['url']
    selenoid = config['selenoid']


    if selenoid != '':
        options = ChromeOptions()

        capabilities = {
            'acceptInsecureCerts': True,
            'browserName': browser,
            'version': version,
            "enableVideo": True
        }

        driver = webdriver.Remote(command_executor='http://' + selenoid + '/wd/hub/',
                                    options=options,
                                    desired_capabilities=capabilities)

        allure.link('http://{selenoid}/video/{driver.session_id}.mp4', name='Browser video')

    else:
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

    driver.get(url)
    yield driver
    driver.close()

