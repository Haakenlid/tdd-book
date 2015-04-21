""" Test that user can log in with Mozilla Persona """
# from unittest import skip
from .base import FunctionalTest

FIRST_EMAIL = 'edith@example.com'
SECOND_EMAIL = 'onni@example.com'
PLACEHOLDER_EMAIL = 'your-friend@example.com'


def quit_if_possible(browser):
    """ Make sure testing browser is closed in cleanup step. """
    try:
        browser.quit()
    except:
        pass


class SharingTest(FunctionalTest):

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        # Edith is a ligged-in user.
        self.create_pre_authenticated_session(FIRST_EMAIL)
        edith_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(edith_browser))

        # Her friend Onni is also hanging out on the lists site.
        onni_browser = self.get_default_browser()
        self.addCleanup(lambda: quit_if_possible(onni_browser))
        self.create_pre_authenticated_session(SECOND_EMAIL)

        # Edith goes to the home page and starts a list.
        self.browser = edith_browser
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('Get help\n')

        # She notices a "Share this list" option.
        share_box = self.browser.find_element_by_css_selector(
            'input[name=email]')
        self.assertEqual(
            share_box.get_attribute('placeholder'),
            PLACEHOLDER_EMAIL
        )
