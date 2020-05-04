import json
import time

from flask_mock.my_http_client import MyHTTPClient
import flask_mock.mymock as fm
import pytest

mock_host = '127.0.0.1'
mock_port = '5000'
mock_addr = 'http://' +mock_host +":"+mock_port

class TestMyMocks():

    @pytest.fixture(scope='session')
    def test_user1(self):
        return {'name': 'Ilya', 'surname': 'Kirillov', 'nick': 'root'}

    @pytest.fixture(scope='session')
    def test_user2(self):
        return {'name': 'Ilya2', 'surname': 'Kirillov2', 'nick': 'root2'}

    @pytest.fixture(scope='session', autouse=True)
    def setup(self, test_user1, test_user2):
        fm.run_mock(mock_host, mock_port)

        time.sleep(1)
        print('creating ilya')
        client = MyHTTPClient()
        client.request('POST', mock_addr + "/user/1", headers={'Content-Type': 'application/json'},
                       body=json.dumps(test_user1))

        client.request('POST', mock_addr + "/user/2", headers={'Content-Type': 'application/json'},
                       body=json.dumps(test_user2))

        yield

        client.request('POST', mock_addr + "/shutdown")

        return

    def test_user_get(self, test_user1):
        result = MyHTTPClient().request('GET', mock_addr + "/user/1")
        assert result['code'] == 200
        assert len(result['body']) == 2

        assert json.loads(result['body'][1]) == test_user1

    def test_user_nick(self, test_user2):
        # да, если на самом деле, очень хотелось бы научить клиент
        # норамльно поддерживать json запросы, но нет времени(((
        result = MyHTTPClient().request('GET', mock_addr + "/user/2")
        assert result['code'] == 200
        assert len(result['body']) == 2

        user2 = json.loads(result['body'][1])
        assert user2['nick'] == test_user2['nick']

        # обновляем ник
        new_nick = user2['nick'] + "_test"
        result = MyHTTPClient().request('POST', mock_addr + "/nick/2", headers={'Content-Type': 'application/json'},
                       body=json.dumps({"nick": new_nick}))
        assert result['code'] == 200

        result = MyHTTPClient().request('GET', mock_addr + "/user/2")
        assert result['code'] == 200
        assert len(result['body']) == 2

        user2 = json.loads(result['body'][1])
        assert user2['nick'] == new_nick

    def test_negative_user_id(self):
        result = MyHTTPClient().request('GET', mock_addr + "/user/-3")
        assert  result['code'] == 400

        result = MyHTTPClient().request('POST', mock_addr + "/nick/-3")
        assert result['code'] == 400