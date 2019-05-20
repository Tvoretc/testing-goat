from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
import time

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome('C:\\webdrivers\\chromedriver.exe')

    def test_visit(self):
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
            inputbox = self.browser.find_element_by_id('id_new_item')
            self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Enter a to-do item'
            )

            #input the item
            inputbox.send_keys(to_do_items[i])
            inputbox.send_keys(Keys.ENTER)
            time.sleep(1)

            #check the table for items
            table = self.browser.find_element_by_tag_name('table')
            rows = table.find_elements_by_tag_name('tr')
            for item in to_do_items[:i+1]:
                self.assertTrue(
                    any(item in row.text for row in rows),
                    f"Item <{item}> did not appeare in a table: \n{table.text}"
                )

        #input second item
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys(to_do_items[1])
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        time.sleep(3)


    def tearDown(self):
        self.browser.quit()

#
# if __name__ == '__main__':
#     unittest.main(warnings='ignore')
