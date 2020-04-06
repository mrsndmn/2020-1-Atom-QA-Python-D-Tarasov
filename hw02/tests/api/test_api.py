import random

import pytest
import os
from api.mytarget_client import MyTargetClient

class TestMyTargetAPI:

    @pytest.fixture(scope='class')
    def api_client(self):
        return MyTargetClient(os.getenv("MYTARGET_USER"), os.getenv("MYTARGET_PASSWORD"))

    @pytest.fixture(scope='function')
    def segment(self, api_client):
        test_seg_name = 'test_segment' + str(random.randint(0,100500))
        json_response = api_client.new_segment(test_seg_name)
        assert json_response['name'] == test_seg_name
        return json_response

    def test_login(self, api_client):
        print(api_client.session)

    def test_new_segment(self, segment):
        assert 'id' in segment

    def test_del_segment(self, api_client, segment):
        assert 'id' in segment
        api_client.del_segment(segment['id'])

