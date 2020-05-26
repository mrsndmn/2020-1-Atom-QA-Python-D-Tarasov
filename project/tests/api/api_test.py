import pytest

from myapp.client import MyAppClient

@pytest.mark.api
class TestAPIBase:
    myapp_client: MyAppClient

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, request, logger, api_client):
        self.myapp_client: MyAppClient = api_client
        self.myapp_client.logger = logger
        self.logger = logger

