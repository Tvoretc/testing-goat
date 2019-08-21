from django.core import mail
from selenium.webdriver.common.keys import Keys
import re
import time

from .base import FunctionalTest

TEST_EMAIL = 'test@mail.com'
SUBJECT = 'Your login link for Superlists'

class LoginTest(FunctionalTest):

    def test_can_get_email_link_to_login(self):
        #comes to site and enteres email
        self.browser.get(self.live_server_url)
        input = self.browser.find_element_by_name('email')
        input.send_keys(TEST_EMAIL)
        input.send_keys(Keys.ENTER)

        #checks email
        self.assertIn('Check your email', self.browser.find_element_by_tag_name('body').text)
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)
        self.assertIn('Use this link to log in', email.body)

        #finds url
        url_search = re.search(r'http://.+/.+$', email.body)
        if not url_search:
            self.fail('Could not find url in email body')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        #goes to url - logs in
        self.browser.get(url)
        self.assert_logged_in(TEST_EMAIL)

        #logs out
        self.browser.find_element_by_link_text('Log out').click()
        self.assert_logged_out(TEST_EMAIL)
