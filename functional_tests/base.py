""" Functional tests for the to-do list app based on user story. """
import sys
import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from .server_tools import reset_database

SCREEN_DUMP_LOCATION = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'screendumps')
FIREFOX_PROFILE_PATH = '/home/haakenlid/.mozilla/firefox/selenium-profile'
PHANTOM_JS_BIN_PATH = '/home/haakenlid/node_modules/phantomjs/lib/phantom/bin/phantomjs'


class FunctionalTest(StaticLiveServerTestCase):

    # test_browser = 'PhantomJS'  # PhantomJS(faster) or Chrome or Firefox
    # test_browser = 'Chrome'  # PhantomJS(faster) or Chrome or Firefox
    test_browser = 'Firefox'  # PhantomJS(faster) or Chrome or Firefox

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
        print('\n{test_name:<80} ({browser})  '.format(
            test_name=' '.join(self.id().split('.')[-2:]),
            browser=self.test_browser,
        ))

        if self.against_staging:
            reset_database(self.server_host)

        if self.test_browser == 'Firefox':
            self.browser = webdriver.Firefox()
            # selenium_firefox_profile = webdriver.FirefoxProfile(FIREFOX_PROFILE_PATH)
            # self.browser = webdriver.Firefox(firefox_profile=selenium_firefox_profile)
        elif self.test_browser == 'Chrome':
            self.browser = webdriver.Chrome()
        elif self.test_browser == 'PhantomJS':
            self.browser = webdriver.PhantomJS(
                executable_path=PHANTOM_JS_BIN_PATH)
        self.browser.implicitly_wait(1)

    def tearDown(self):
        if self._test_has_failed():
            if not os.path.exists(SCREEN_DUMP_LOCATION):
                os.makedirs(SCREEN_DUMP_LOCATION)
            for ix, handle in enumerate(self.browser.window_handles):
                self._windowid = ix
                self.browser.switch_to_window(handle)
                self.take_screenshot()
                self.dump_html()
        self.browser.quit()
        super().tearDown()

    def _test_has_failed(self):
        for method, error in self._outcome.errors:
            if error:
                return True
        return False

    def _get_filename(self):
        timestamp = datetime.now().isoformat().replace(':', '.')[:19]
        return '{folder}/{classname}.{method}-window{windowid}-{timestamp}'.format(
            folder=SCREEN_DUMP_LOCATION,
            classname=self.__class__.__name__,
            method=self._testMethodName,
            windowid=self._windowid,
            timestamp=timestamp,
        )

    def take_screenshot(self):
        filename = self._get_filename() + '.png'
        print('screenshotting to', filename)
        self.browser.get_screenshot_as_file(filename)

    def dump_html(self):
        filename = self._get_filename() + '.html'
        print('dumping page HTML to', filename)
        with open(filename, 'w') as f:
            f.write(self.browser.page_source)

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
