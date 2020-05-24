import pytest
import os
from model.myapp_user import User, MysqlOrmConnection
from myapp.client import MyAppClient

import faker
from faker.providers import internet

@pytest.fixture
def myqsl_session():
    return MysqlOrmConnection().session

@pytest.fixture(scope='session')
def api_client(request):
    myqsl_session = MysqlOrmConnection().session
    user = _regular_user(myqsl_session)
    return MyAppClient(os.getenv('MYAPP_URL', 'http://localhost:8001'), user=user.username, password=user.password)

@pytest.fixture()
def regular_user(myqsl_session):
    return _regular_user(myqsl_session)

fake = faker.Faker()

def _regular_user(myqsl_session):
    username = fake.user_name()[:10]
    password = username
    email = fake.ascii_email()

    user = myqsl_session.query(User).filter_by(username=username).first()
    if user is not None:
        myqsl_session.session.delete(user)

    user = User(username=username, password=password, email=email)

    myqsl_session.add(user)
    myqsl_session.commit()

    return user


# todo вообще говоря, эти фиксутры не ограничены по длинне, а должны были быть
@pytest.fixture()
def username():
    return fake.user_name()[:10]

@pytest.fixture()
def password():
    return fake.user_name()

@pytest.fixture()
def email():
    return fake.ascii_email()