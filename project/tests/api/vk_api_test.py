import pytest
from vkapi.client import VKAPIClient

class TestVKAPI:
    @pytest.fixture(autouse=True)
    def setup(self, logger):
        self.api_client = VKAPIClient(logger=logger)

    @pytest.mark.parametrize('vk_id', [ 1, -1, 100500 ])
    def test_mock_user(self, username, vk_id):
        """
        Проверка работоспособности мока
        """
        resp = self.api_client.mock_user(username, vk_id)
        assert resp.status_code == 200
        resp = self.api_client.get_vk_id(username)
        assert resp == {"vk_id":  str(vk_id)}
