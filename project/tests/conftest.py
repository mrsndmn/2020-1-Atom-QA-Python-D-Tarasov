import allure
import pytest
import logging
import os
import uuid


@pytest.fixture(scope='function')
def logger(request):
    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    print("request.node", request.node.location[-1])
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
