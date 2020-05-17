import pytest
import os
from model.myapp_user import User, MysqlOrmConnection
from myapp.client import MyAppClient

import faker
from faker.providers import internet

@pytest.fixture(scope='session', autouse=True)
def faker_session_locale():
    return ['en_US']

@pytest.fixture(scope='session')
def myqsl_session():
    return MysqlOrmConnection().session

@pytest.fixture(scope='session')
def api_client():
    return MyAppClient(os.getenv('MYAPP_URL', 'http://localhost:8001'))

@pytest.fixture
def regular_user(myqsl_session):

    username = 'testqaqaqa'
    user = myqsl_session.query(User).filter_by(username=username).first()
    if user is not None:
        myqsl_session.session.delete(user)

    user = User(username=username, password='qaqaqatest', email='testqaqaqa@example.com')

    myqsl_session.add(user)
    myqsl_session.commit()
