from ui.base import BaseCase


class TestUI(BaseCase):

    def test_login(self):
        self.main_page.login()
        self.driver

    # # @pytest.mark.skip(reason='TEMP')
    # @pytest.mark.parametrize('query', ['pycon', 'python'])
    # def test_search(self, query):
    #     self.main_page.search(query)
    #     assert "No results found." not in self.driver.page_source
    #
    # # @pytest.mark.skip(reason='TEMP')
    # def test_search_negative(self):
    #     self.base_page.search('23132173152361253675216735126735132516736712')
    #     self.base_page.find(self.main_page.locators.NO_RESULTS).is_displayed()
    #
    # # @pytest.mark.skip(reason='TEMP')
    # def test_carousel(self):
    #     self.main_page.click(self.main_page.locators.COMPREHENSIONS, timeout=12)
    #
    # # @pytest.mark.skip(reason='TEMP')
    # def test_count(self):
    #     with pytest.raises(TimeoutException):
    #         self.main_page.count_elements(self.main_page.locators.NO_SUCH_ELEMENT, count=2)
    #
    # # @pytest.mark.skip(reason='TEMP')
    # @allure.feature('events')
    # @allure.story('main')
    # def test_euro_python(self):
    #
    #     with allure.step('Find events page'):
    #         events = self.base_page.find(self.base_page.locators.EVENTS)
    #
    #     ac = ActionChains(self.driver)
    #     ac.move_to_element(events).perform()
    #
    #     python_events_page = self.main_page.go_to_python_events()
    #     python_events_page.click(python_events_page.locators.EURO_PYTHON)
    #
    #     allure.attach(self.driver.get_screenshot_as_png(),
    #                   name='/tmp/1/test_alert',
    #                   attachment_type=allure.attachment_type.PNG)
    #
    #
    #     assert 'Dublin' in self.driver.page_source
    #
    # # @pytest.mark.skip(reason='TEMP')
    # def test_page_changed(self):
    #     self.base_page.click(self.base_page.locators.GO_BUTTON)
    #
    # # @pytest.mark.skip(reason='TEMP')
    # def test_relative(self):
    #     intro = self.main_page.find(self.main_page.locators.INTRODUCTION)
    #     learn_more = intro.find_element(*self.main_page.locators.LEARN_MORE)
    #
    #     if self.config['url'].startswith('https'):
    #         expected = self.config['url']
    #     else:
    #         expected = self.config['url'].replace('http', 'https')
    #
    #     assert learn_more.get_attribute('href') == f'{expected}/doc/'
    #
    # # @pytest.mark.skip(reason='TEMP')
    # def test_options(self):
    #     self.driver.get('https://expired.badssl.com/')
    #     self.bad_ssl_page.find(self.bad_ssl_page.locators.H1_CONTENT)
    #
    # # @pytest.mark.skip(reason='TEMP')
    # def test_download(self):
    #     self.driver.get('https://www.python.org/downloads/release/python-382/')
    #     self.python382_page.click(self.python382_page.locators.WINDOWS_X86_X64_WEB_BASED)
    #     self.wait_download('python-3.8.2-amd64-webinstall.exe')
    #
    # # @pytest.mark.skip(reason='TEMP')
    # @pytest.mark.parametrize('command, result', [('assert 1 / 0', 'ZeroDivisionError')])
    # def test_iframe(self, command, result):
    #     self.main_page.iframe_run_command('assert 1 / 0')
    #     assert self.main_page.find((By.XPATH, self.main_page.locators.IFRAME_RESULT.format(result)))
    #     self.driver.switch_to.default_content()
    #
    #     import time
    #     time.sleep(5)
    #
    # # @pytest.mark.skip(reason='TEMP')
    # def test_alert(self):
    #     alert_msg = 'example'
    #     self.main_page.alert(alert_msg)
    #     alert = self.driver.switch_to.alert
    #     assert alert_msg == alert.text
    #     alert.accept()
    #
    # # @pytest.mark.skip(reason='TEMP')
    # def test_donate(self):
    #     pass