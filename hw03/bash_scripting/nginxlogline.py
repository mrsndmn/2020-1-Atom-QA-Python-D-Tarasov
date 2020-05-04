import json
import re

class LogLine:
    parserRe = re.compile(
        r"^(?P<ip>\S+)(?:[^\[]+)(?:\[[^\]]+\])\s\"(?P<method>\S+)\s(?P<path>\S+) HTTP/1\.1\"\s(?P<status>\d+)\s(?P<size>\d+)")

    def __init__(self, line):
        res = self.parserRe.match(line)

        if res is None:
            raise ValueError("Passed line does not look like nginx access log line")

        self.ip = res.group('ip')
        self.method = res.group('method')
        self.path = res.group('path')
        self.status = int(res.group('status'))
        self.size = int(res.group('size'))
        return

    def __repr__(self):
        return " ".join((self.ip, self.method, self.path, str(self.status), str(self.size)))
