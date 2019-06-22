from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from unittest import skip
from functional_tests.base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        self.browser.get(self.live_server_url)
        # enter empty value
        self.get_item_input_box().send_keys(Keys.ENTER)
        # get error
        self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            'Can`t have an empty list item,'
        )

        to_do_items = ('not empty', 'not empty 2')
        # enter nonempty value
        input = self.browser.find_element_by_id('id_text')
        input.send_keys('not empty')
        input.send_keys(Keys.Enter)

        # enter empty value again
        self.browser.find_element_by_id('id_text').send_keys(Keys.ENTER)

        # get error
        self.assertEqual(
            self.client.find_element_by_css_selector('.has-error').text,
            'Can`t have an empty list item,'
        )

        # enter enother nonempty value
        input = self.browser.find_element_by_id('id_text')
        input.send_keys('not empty 2')
        input.send_keys(Keys.Enter)

        table = self.browser.find_element_by_tag_name('table')
        rows = table.find_elements_by_tag_name('tr')
        for item in to_do_items:
            self.assertTrue(
                any(item in row.text for row in rows),
                f"Item <{item}> did not appeare in a table: \n{table.text}"
            )
