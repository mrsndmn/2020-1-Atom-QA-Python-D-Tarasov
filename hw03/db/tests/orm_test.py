
import os
from faker import Faker
import pytest
from db.mysql_client import MysqlOrmConnection
from db.models.nginxlogs import NginxLog
from dotenv import load_dotenv
load_dotenv()

fake = Faker(locale='ru_RU')

# если бы было больше тестов, возможно, стило бы
# это унести в conftest. Но тк тест один и он очень простой,
# кажется, можно сделать это тут
@pytest.fixture(scope='function')
def nginx_log():
    return NginxLog(
        ip=fake.ipv4_private(),
        method='GET',
        path='/',
        status=200,
        size=100500,
    )

@pytest.fixture(scope='function')
def mysql_connection():
    return MysqlOrmConnection(os.getenv("MYSQL_USER"), os.getenv("MYSQL_PASSWORD"),
                                     db_name=os.getenv("MYSQL_DB"))

class TestOrmMysql:
    def test_logs_create(self, mysql_connection, nginx_log):
        mysql_connection.session.add(nginx_log)
        mysql_connection.session.flush()

        selected_log = mysql_connection.session.query(NginxLog).get(nginx_log.id)

        assert selected_log.id == nginx_log.id
        assert selected_log.ip == nginx_log.ip
        assert selected_log.method == nginx_log.method
        assert selected_log.path == nginx_log.path
        assert selected_log.status == nginx_log.status
        assert selected_log.size == nginx_log.size

