from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from unittest import skip
from functional_tests.base import FunctionalTest
from lists.models import Item
from lists.forms import EMPTY_ITEM_ERROR
import time


class ItemValidationTest(FunctionalTest):

    def assertItemInList(self, item):
        table = self.browser.find_element_by_tag_name('table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(item in row.text for row in rows),
            f"Item <{item}> did not appeare in a table: \n{table.text}"
        )

    def test_cannot_add_empty_list_items(self):
        self.browser.get(self.live_server_url)
        # enter empty value
        input = self.get_item_input_box()
        input.send_keys(Keys.ENTER)
        # get error
        self.browser.find_elements_by_css_selector('#id_text:invalid')

        # input valid text
        input.send_keys('buy milk')
        # see it is valid
        self.browser.find_elements_by_css_selector('#id_text:valid')
        input.send_keys(Keys.ENTER)

        # check if item appeared in list
        self.assertItemInList('buy milk')

        # empty input again
        input = self.get_item_input_box()
        # input doesnt contain old data (write unittest?)
        self.assertEquals(input.text, '')
        input.send_keys(Keys.ENTER)

        self.browser.find_elements_by_css_selector('#id_text:invalid')
        self.assertItemInList('buy milk')

        # enter enother nonempty value
        input = self.get_item_input_box()
        input.send_keys('make a tea')
        input.send_keys(Keys.ENTER)

        # check if item appeared in list
        self.assertItemInList('buy milk')
        self.assertItemInList('make a tea')

    def test_cant_have_duplicates(self):
        self.browser.get(self.live_server_url)
        input = self.get_item_input_box()
        input.send_keys('to-do item')
        input.send_keys(Keys.ENTER)

        input = self.get_item_input_box()
        input.send_keys('to-do item')
        input.send_keys(Keys.ENTER)

        self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            'You`ve already entered this item. Can`t have duplicates.'
        )
        self.assertEquals(Item.objects.count(), 1)
