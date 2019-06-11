from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import os

class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome('C:\\webdrivers\\chromedriver.exe')
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        self.browser.quit()
