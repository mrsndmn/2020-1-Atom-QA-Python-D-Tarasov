import pytest

from linux.tests.conftest import SSH
import requests
import uuid

class TestLinux:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, ssh_client: SSH):
        success = ssh_client.sudo_exec_cmd(f'firewall-cmd --reload')
        assert success == ["success\n"]

    def test_i_am_root(self, ssh_client: SSH):
        res = ssh_client.sudo_exec_cmd('whoami')
        assert res == ['root\n']

        res = ssh_client.sudo_exec_cmd('id -u')
        assert res == ['0\n']

    def test_nginx_http(self, nginx_url):
        res = requests.get(nginx_url)
        assert res.status_code == 200

    def test_nginx_ssh(self, ssh_client, nginx_port):
        res = ssh_client.sudo_exec_cmd('netstat -npl | grep nginx | awk "{print $4}" |' + f' grep ":{nginx_port}"')
        assert len(res) > 1

    def test_nginx_access_log(self, ssh_client, nginx_url):

        testuuid = uuid.uuid1()
        res = requests.get(nginx_url + '?q=' + str(testuuid))
        assert res.status_code == 200

        lines = ssh_client.sudo_exec_cmd(f'grep -c "{testuuid}" /var/log/nginx/access.log')
        assert int(lines[0]) > 0

    # учитываем, что в перманентном конфиге фаервола 8080 порт открыт
    def test_nginx_firewall(self, ssh_client, nginx_url, nginx_port):
        success = ssh_client.sudo_exec_cmd(f'firewall-cmd --remove-port={nginx_port}/tcp')
        assert success == ["success\n"]

        with pytest.raises(requests.exceptions.ConnectionError):
            requests.get(nginx_url)

        res = ssh_client.sudo_exec_cmd('systemctl status nginx | grep -c "Active: active (running)"')
        assert int(res[0]) == 1

        success = ssh_client.sudo_exec_cmd(f'firewall-cmd --reload')
        assert success == ["success\n"]