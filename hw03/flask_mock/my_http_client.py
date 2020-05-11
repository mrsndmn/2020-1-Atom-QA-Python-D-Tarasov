import socket
import re
import urllib.parse
from urllib.parse import urlparse
import json

class MyHTTPResp():
    def __init__(self, status_code):
        self.status_code = status_code
        self.headers = dict()
        self.body = None

class MyHTTPClient():
    def request(self, method, url, body=None, timeout=2, headers=None):

        if headers is None:
            headers = dict()

        parsed_url: urllib.parse.ParseResult = urlparse(url)

        # print(parsed_url)

        if parsed_url.scheme != 'http':
            raise ValueError("Only http proto is supported")

        ipaddr = socket.gethostbyname(parsed_url.hostname)

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(timeout)

        port = parsed_url.port
        port = port if port is not None else 80

        client.connect((ipaddr, port))

        if body is not None:
            headers['Content-Length'] = len(body)
        else:
            body = ''

        headers['Host'] = parsed_url.hostname
        if 'User-Agent' not in headers:
            headers['User-Agent'] = 'curl'

        headers_encoded = ''
        for k in headers:
            header_val = str(headers[k])
            header_val = re.sub(r"\n", ' ', header_val)
            headers_encoded += f'{k}: {header_val}\r\n'

        path = parsed_url.path + parsed_url.query
        if path == '':
            path = '/'

        request = f'{method} {path} HTTP/1.1\r\n'+ headers_encoded +'\r\n' + body


        print(request)
        client.send(request.encode())

        total_data = []
        while True:
            data = client.recv(1024)
            if data:
                total_data.append(data.decode())
            else:
                break

        data = ''.join(total_data).splitlines()

        resp = {
            'headers': dict(),
        }

        if len(data) < 1:
            return resp

        # todo check errors
        resp['code'] = int(data[0].split(" ")[1])

        for i, l in enumerate(data[1:]):
            if l == '':
                resp['body'] = data[i+1:]
                break
            header, header_value = l.split(": ")
            # todo on duplicate header we should stack them in array
            resp['headers'][header] = header_value

        print(json.dumps(resp))

        return resp