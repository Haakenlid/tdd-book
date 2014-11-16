""" Functional tests for the to-do list app based on user story. """
import sys
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from django.contrib.staticfiles.testing import StaticLiveServerCase
from .server_tools import reset_database


class FunctionalTest(StaticLiveServerCase):

    test_browser = 'PhantomJS'  # PhantomJS(faster) or Chrome or Firefox
    # test_browser = 'Chrome'  # PhantomJS(faster) or Chrome or Firefox
    # test_browser = 'Firefox'  # PhantomJS(faster) or Chrome or Firefox

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_host = arg.split('=')[1]
                cls.server_url = 'http://' + cls.server_host
                cls.against_staging = True
                return
        super().setUpClass()
        cls.against_staging = False
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

    def setUp(self):
        print('Functional test: {test}\nBrowser: {browser}'.format(test=type(self).__name__, browser=self.test_browser))
        if self.against_staging:
            reset_database(self.server_host)

        if self.test_browser == 'Firefox':
            selenium_firefox_profile = webdriver.FirefoxProfile(
                '/home/haakenlid/.mozilla/firefox/selenium-profile')
            self.browser = webdriver.Firefox(
                firefox_profile=selenium_firefox_profile)
        elif self.test_browser == 'Chrome':
            self.browser = webdriver.Chrome()
        elif self.test_browser == 'PhantomJS':
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

    def wait_to_be_logged_in(self, email):
        self.wait_for_element_with_id('id_logout')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(email, navbar.text)

    def wait_to_be_logged_out(self, email):
        self.wait_for_element_with_id('id_login')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(email, navbar.text)

    def wait_for_element_with_id(self, element_id):
        WebDriverWait(self.browser, timeout=10).until(
            lambda b: b.find_element_by_id(element_id),
            'could not find element with id "{}". Page content was \n{}'.format(
                element_id,
                self.browser.find_element_by_tag_name('body').text,
            ),
        )

    def switch_to_new_window(self, text_in_title):
        retries = 20
        while retries > 0:
            page_titles = []
            for handle in self.browser.window_handles:
                self.browser.switch_to_window(handle)
                # print(self.browser.title)
                if text_in_title in self.browser.title:
                    return
                page_titles.append(self.browser.title)
            retries -= 1
            time.sleep(0.5)
        self.fail(
            'could not find window "{}". Pages are \n{}'.format(
                text_in_title,
                page_titles,
            )
        )
