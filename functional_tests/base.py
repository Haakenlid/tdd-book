""" Functional tests for the to-do list app based on user story. """
import sys
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerCase


class FunctionalTest(StaticLiveServerCase):

    # WEBDRIVER = 'PhantomJS'  # PhantomJS(faster) or Chrome or Firefox
    WEBDRIVER = 'Chrome'  # PhantomJS(faster) or Chrome or Firefox
    # WEBDRIVER = 'Firefox'  # PhantomJS(faster) or Chrome or Firefox

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

    def setUp(self):
        if self.WEBDRIVER == 'Firefox':
            selenium_firefox_profile = webdriver.FirefoxProfile(
                '/home/haakenlid/.mozilla/firefox/selenium-profile')
            self.browser = webdriver.Firefox(
                firefox_profile=selenium_firefox_profile)
        elif self.WEBDRIVER == 'Chrome':
            self.browser = webdriver.Chrome()
        elif self.WEBDRIVER == 'PhantomJS':
            # self.browser = webdriver.PhantomJS()  # Ubuntu version.
            self.browser = webdriver.PhantomJS(
                executable_path='/home/haakenlid/node_modules/phantomjs/lib/phantom/bin/phantomjs')
        self.browser.implicitly_wait(1)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')
