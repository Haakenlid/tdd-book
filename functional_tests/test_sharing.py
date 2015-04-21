""" Test that user can log in with Mozilla Persona """
# from unittest import skip
from .base import FunctionalTest
from .home_and_list_pages import HomePage

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

    def test_sharing_list_with_friends(self):
        # Edith is a ligged-in user.
        self.create_pre_authenticated_session(FIRST_EMAIL)
        edith_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(edith_browser))

        # Her friend Onni is also hanging out on the lists site.
        onni_browser = self.get_default_browser()
        self.addCleanup(lambda: quit_if_possible(onni_browser))
        self.browser = onni_browser
        self.create_pre_authenticated_session(SECOND_EMAIL)

        # Edith goes to the home page and starts a list.
        self.browser = edith_browser
        list_page = HomePage(self).start_new_list('Get help')

        # She notices a "Share this list" option.
        share_box = list_page.get_share_box()
        self.assertEqual(
            share_box.get_attribute('placeholder'),
            PLACEHOLDER_EMAIL
        )

        # She shares her list.
        # The page updates to say that it's shared with Onni.
        list_page.share_list_with(SECOND_EMAIL)

        # Onni now goes to the lists page with his browser.
        self.browser = onni_browser
        HomePage(self).go_to_page().go_to_my_lists_page()

        # He sees Edith's lists in there!
        self.browser.find_element_by_link_text('Get help').click()

        # On the list page, Onni can see that it says that it's Edith's list
        self.wait_for(
            lambda: self.assertEqual(
                list_page.get_list_owner(),
                FIRST_EMAIL
                )
            )
        # He adds an item to the list
        list_page.add_new_item('Hi Edith!')

        # When Edith refreshes the page, she sees Onni's addition
        self.browser = edith_browser
        self.browser.refresh()
        list_page.wait_for_new_item_in_list('Hi Edith!', 2)

