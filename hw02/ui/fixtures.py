import os

import pytest

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from ui.pages.base import BasePage
from ui.pages.login import LoginPage
from ui.pages.campaigns import CampaignsPage


class UsupportedBrowserException(Exception):
    pass


@pytest.fixture(scope='function')
def base_page(driver):
    return BasePage(driver)

@pytest.fixture(scope='function')
def login_page(driver):
    return LoginPage(driver)

@pytest.fixture(scope='function')
def logined_driver(driver, login_page):
    login_page.login(os.getenv("MYTARGET_USER"), os.getenv("MYTARGET_PASSWORD"))
    driver = login_page.driver
    return driver



@pytest.fixture(scope='function')
def campaign_page(logined_driver):
    logined_driver.get("https://target.my.com/campaigns/list") # todo urljoin
    return CampaignsPage(logined_driver)

@pytest.fixture(scope='session')
def test_img():
    return os.path.abspath('hw02/img/when_you_lost_root.png')

@pytest.fixture(scope='function')
def driver(config):
    browser = config['browser']
    version = config['version']
    chrome_path = config['chrome_path']
    url = config['url']

    if browser == 'chrome':
        options = ChromeOptions()
        options.binary_location = chrome_path

        manager = ChromeDriverManager(version=version)
        driver = webdriver.Chrome(executable_path=manager.install(), options=options)

        # capabilities = {'acceptInsecureCerts': True,
        #                 'browserName': 'chrome',
        #                 'version': version,
        #                 }
        #
        # driver = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub/',
        #                           options=options,
        #                           desired_capabilities=capabilities
        #                           )

    elif browser == 'firefox':
        manager = GeckoDriverManager(version=version)
        driver = webdriver.Firefox(executable_path=manager.install())

    else:
        raise UsupportedBrowserException(f'Usupported browser: "{browser}"')

    driver.get(url)
    yield driver
    driver.close()


@pytest.fixture(scope='function', params=['chrome', 'firefox'])
def all_drivers(config, request):
    browser = request.param
    url = config['url']

    if browser == 'chrome':
        manager = ChromeDriverManager(version='latest')
        driver = webdriver.Chrome(executable_path=manager.install())

    elif browser == 'firefox':
        manager = GeckoDriverManager(version='latest')
        driver = webdriver.Firefox(executable_path=manager.install())

    else:
        raise UsupportedBrowserException(f'Usupported browser: "{browser}"')

    driver.maximize_window()
    driver.get(url)
    yield driver
    driver.close()
