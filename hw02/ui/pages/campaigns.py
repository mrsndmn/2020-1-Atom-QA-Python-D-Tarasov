from .base import BasePage
from ui.locators.locators import CampaignsPageLocators


class CampaignsPage(BasePage):
    locators = CampaignsPageLocators()

    def create(self, test_img, compaign_url="https://ok.ru/bezkote",
               compaign_name="test compaign name", compaing_desc="Test banner description"):

        self.driver.get("https://target.my.com/campaign/new")  # todo urljoin
        self.click(self.locators.SOCIAL_ACTION_CONVERSION_BUTTON)
        self.fill_input(self.locators.LINK_INPUT, compaign_url)

        self.fill_input(self.locators.BANNER_TITLE_INPUT, compaign_name)
        self.fill_input(self.locators.BANNER_DESCRIPTION_INPUT, compaing_desc, no_clear=True)
        # self.driver.implicitly_wait(10)
        self.fill_input(self.locators.BANNER_LITTLE_IMG_INPUT, test_img, no_clear=True)

        self.click(self.locators.BANNER_IMG_SUBMIT_INPUT)

        self.click(self.locators.SUBMIT_NEW_CAMPAIGN)

        self.check_campaign_was_created()

    def check_campaign_was_created(self):
        self.driver.get('https://target.my.com/campaigns/list')
        self.driver.implicitly_wait(10)

