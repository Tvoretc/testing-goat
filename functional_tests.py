from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome('C:\\webdrivers\\chromedriver.exe')

    def test(self):
        self.browser.get('http://localhost:8000/')

        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')
        #, "Title was " + browser.title

    def tearDown(self):
        self.browser.quit()

if __name__ == '__main__':
    unittest.main(warnings='ignore')
