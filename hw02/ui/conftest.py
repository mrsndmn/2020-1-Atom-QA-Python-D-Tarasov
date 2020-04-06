from ui.fixtures import *
import pytest
import allure


class UnsupportedBrowserException(Exception):
    pass


def pytest_addoption(parser):
    parser.addoption('--url', default='https://account.my.com/')
    parser.addoption('--browser', default='chrome')
    parser.addoption('--chrome-path', default='')
    parser.addoption('--browser_ver', default='80.0.3987.106')
    parser.addoption('--selenoid', default='')


@pytest.fixture(scope='session')
def config(request):
    url = request.config.getoption('--url')
    browser = request.config.getoption('--browser')
    version = request.config.getoption('--browser_ver')
    chrome_path = request.config.getoption('--chrome-path')
    selenoid = request.config.getoption('--selenoid')

    return {'browser': browser, 'version': version, 'url': url, 'chrome_path': chrome_path, 'selenoid': selenoid}


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


@pytest.fixture(scope="function", autouse=True)
def take_screenshot_when_failure(request, driver):
    yield
    if request.node.rep_call.failed:
        allure.attach('\n'.join(driver.get_log('browser')),
                      name='console.log',
                      attachment_type=allure.attachment_type.TEXT)
        allure.attach(driver.get_screenshot_as_png(),
                      name=request.node.location[-1],
                      attachment_type=allure.attachment_type.PNG)
