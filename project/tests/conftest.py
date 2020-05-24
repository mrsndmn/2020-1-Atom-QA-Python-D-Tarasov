import allure
import pytest
import logging
import os
import uuid

from testcontainers.general import TestContainer
from testcontainers.mysql import MySqlContainer

import testcontainers


@pytest.fixture(scope='function')
def logger(request):
    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    log_file = str(uuid.uuid1())

    file_handler = logging.FileHandler(log_file, 'w')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.INFO)

    log = logging.getLogger('api_log')
    log.propogate = False
    log.setLevel(logging.DEBUG)
    log.addHandler(file_handler)

    failed_count = request.session.testsfailed
    yield log
    if request.session.testsfailed > failed_count:
        with open(log_file, 'r') as f:
            allure.attach(f.read(), name=request.node.location[-1], attachment_type=allure.attachment_type.TEXT)

    os.remove(log_file)


def pytest_addoption(parser):
    parser.addoption('--url', default='http://192.168.122.221:8001/login')
    parser.addoption('--browser', default='chrome')
    parser.addoption('--chrome-path', default='')
    # parser.addoption('--browser_ver', default='80.0.3987.106')
    parser.addoption('--browser_ver', default=None)
    parser.addoption('--selenoid', default='192.168.122.122:4444')


@pytest.fixture(scope='session')
def config(request):
    url = request.config.getoption('--url')
    browser = request.config.getoption('--browser')
    version = request.config.getoption('--browser_ver')
    chrome_path = request.config.getoption('--chrome-path')
    selenoid = request.config.getoption('--selenoid')

    return {'browser': browser, 'version': version, 'url': url, 'chrome_path': chrome_path, 'selenoid': selenoid}

