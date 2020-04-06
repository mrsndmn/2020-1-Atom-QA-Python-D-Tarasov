import pytest
from ui.base import BaseCase

class TestUI(BaseCase):

    @pytest.mark.UI
    def test_login(self, logined_driver):
        assert 'error_code' not in logined_driver.current_url

    @pytest.mark.UI
    def test_bad_login(self, driver, login_page):
        login_page.login("no_such_email@example.com", "no_such_password")
        print(driver.current_url)
        assert 'error_code' in driver.current_url

    @pytest.mark.UI
    def test_new_campaign(self, campaign_page, test_img):
        campaign_page.create(test_img)
