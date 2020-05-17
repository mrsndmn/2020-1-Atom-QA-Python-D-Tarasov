import pytest
from model.myapp_user import User, MysqlOrmConnection
from myapp.client import MyAppClient

import faker
from faker.providers import internet

@pytest.fixture(scope='session', autouse=True)
def faker_session_locale():
    return ['en_US']

@pytest.fixture(scope='session', autouse=True)
def myqsl_session():
    return MysqlOrmConnection().session

@pytest.fixture
def regular_user(myqsl_session, faker: faker.Faker, user_name_length=16, password_length=255, email=None):

    if email is None:
        email = faker.ascii_free_email()

    user = User(username=faker.user_name(user_name_length), password=faker.random_letters(password_length), email=email)

    myqsl_session.add(user)
    myqsl_session.commit()
