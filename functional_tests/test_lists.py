from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from functional_tests.base import FunctionalTest

class NewVisitorTest(FunctionalTest):
    def test_new_visitor_creating_list(self):
        #visit site
        self.browser.get(self.live_server_url)

        #see the title and header
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)


        #items to add
        to_do_items = ('Write a test.', 'Run the test.')

        for i in range(len(to_do_items)):
            #find inputbox
            inputbox = self.get_item_input_box()
            self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Enter a to-do item'
            )

            #input the item
            inputbox.send_keys(to_do_items[i])
            inputbox.send_keys(Keys.ENTER)

            #check the table for items
            self.assert_items_in_list(to_do_items[:i+1])


    def test_different_visitors_have_different_lists(self):
        self.browser.get(self.live_server_url)

        # table = self.browser.find_element_by_tag_name('table')
        # self.assertNotIn('1:', table.text)

        inputbox = self.get_item_input_box()
        inputbox.send_keys('my unique to-do item.')
        inputbox.send_keys(Keys.ENTER)
        table = self.browser.find_element_by_tag_name('table')

        self.assertIn('my unique to-do item.', table.text)
        first_url = self.browser.current_url
        self.assertRegex(first_url, '/lists/.+')

        self.browser.quit()
        self.browser = webdriver.Chrome(self.chrome_dir)

        self.browser.get(self.live_server_url)

        # table = self.browser.find_element_by_tag_name('table')
        # self.assertNotIn('1:', table.text)

        inputbox = self.get_item_input_box()
        inputbox.send_keys('other user`s item.')
        inputbox.send_keys(Keys.ENTER)
        table = self.browser.find_element_by_tag_name('table')

        self.assertIn('other user`s item.', table.text)

        second_url = self.browser.current_url
        self.assertRegex(second_url, '/lists/.+')
        self.assertNotEqual(first_url, second_url)

        self.assertNotIn('my unique to-do item.', table.text)
