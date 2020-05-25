import pytest
import os
from model.myapp_user import User, MysqlOrmConnection
from myapp.client import MyAppClient

import faker
from faker.providers import internet

@pytest.fixture
def mysql_session():
    sess = MysqlOrmConnection().session
    return sess

@pytest.fixture(scope='session')
def api_client(request):
    mysql_session = MysqlOrmConnection().session
    user = _regular_user(mysql_session)
    return MyAppClient(url=os.getenv('MYAPP_URL', 'http://localhost:8001'), user=user.username, password=user.password)

@pytest.fixture()
def regular_user(mysql_session):
    # todo не меньше 5 исмволов, не больше 16
    return _regular_user(mysql_session)

fake = faker.Faker()

def _regular_user(mysql_session):
    username = fake.user_name()[:10]
    password = username
    email = fake.ascii_email()

    user = mysql_session.query(User).filter_by(username=username).first()
    if user is not None:
        mysql_session.delete(user)

    user = User(username=username, password=password, email=email)

    mysql_session.add(user)
    mysql_session.commit()

    return user


@pytest.fixture()
def username():
    return fake.user_name()[:10]

@pytest.fixture
def long_username():
    return fake.lexify('?'*17)

@pytest.fixture()
def password():
    return fake.user_name()

@pytest.fixture()
def email():
    return fake.ascii_email()