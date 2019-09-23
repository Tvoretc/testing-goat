from selenium.webdriver.common.keys import Keys
# from functional_tests.base.FunctionalTest import wait


class ListPage(object):

    def __init__(self, test):
        self.test = test

    def get_share_box(self):
        return self.test.browser.find_element_by_css_selector(
            'input[name="share"]'
        )

    def get_shared_with_list(self):
        return self.test.browser.find_element_by_css_selector(
            '.list-share'
        )

    def get_list_owner(self):
        return self.test.browser.find_element_by_id('id_list_owner').text

    def share_list_with(self, email):
        self.get_share_box().send_keys(email)
        self.get_share_box().send_keys(keys.ENTER)
        self.test.wait_for(lambda: self.test.assertIn(
            email,
            [item.text for item in self.get_shared_with_list()]
        ))

    def assert_email_in_share_list(self, email):
        share_box = self.browser.find_element_by_css_selector(
            'input[name="share"]'
        )
        self.assertEqual(
            share_box.get_attribute('placeholder'),
            email
        )
