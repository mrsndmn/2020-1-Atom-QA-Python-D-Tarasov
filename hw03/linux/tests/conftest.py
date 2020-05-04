import time

from paramiko import SSHClient, AutoAddPolicy, AuthenticationException, SSHException
import pytest

import os
from dotenv import load_dotenv
load_dotenv()

class SSH:
    def __init__(self):
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())

        try:
            self.client.connect(
                hostname=os.getenv('TEST_SSH_HOST'),
                port=int(os.getenv('TEST_SSH_PORT', 22)),
                username=os.getenv('TEST_SSH_USER'),
                password=os.getenv('TEST_SSH_PASSWORD'),
            )
        except AuthenticationException:
            print("Authentication failed, please verify your credentials")
        except SSHException as sshException:
            print(f"Could not establish SSH connection {sshException}")

        return

    def sudo_exec_cmd(self, cmd):
        # todo сделать нормальный эскейп того, что передается в cmd
        # сейчас нельзя использвоать в команде одинарные кавычки
        stdin, stdout, stderr = self.client.exec_command(f'echo "{os.getenv("TEST_SSH_PASSWORD")}" | sudo -S bash -c \'' + cmd + '\'')

        res = stdout.readlines()
        return res

    def exec_cmd(self, cmd, ignore_stderr=False):
        stdin, stdout, stderr = self.client.exec_command(cmd)
        data = stdout.read()
        data = data.decode()

        err = stderr.read()
        err = err.decode()

        if err and not ignore_stderr:
            raise Exception(f'Err:{err}')

        return data

@pytest.fixture(scope='function')
def ssh_client():
    return SSH()

@pytest.fixture(scope='session')
def nginx_port():
    return os.getenv("TEST_NGINX_PORT")

@pytest.fixture(scope='session')
def nginx_url(nginx_port):
    return "http://" + os.getenv("TEST_SSH_HOST")+":"+nginx_port