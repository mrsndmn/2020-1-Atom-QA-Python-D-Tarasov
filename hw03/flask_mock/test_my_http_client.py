from flask_mock.my_http_client import MyHTTPClient


def test_simple_get():
    client = MyHTTPClient()

    resp = client.request('GET', 'http://www.python.org/')

    assert resp['code'] == 301
    assert resp['headers']['Location'] == 'https://www.python.org/'