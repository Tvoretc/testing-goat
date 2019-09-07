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

# not used
    def wait_email(self, test_email, subject):
        if not self.staging_server:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(email.subject, SUBJECT)
            return email.body

        email_id = None
        start = time.time()
        inbox = poplib.POP3_SSL('pop.mail.yahoo.com')
        try:
            inbox.user(test_email)
            inbox.pass_(os.environ['YAHOO_PASSWORD'])
            while time.time() - start < 60:
                count, _ = inbox.stat()
                for i in reversed(range(max(1,count - 10), count + 1)):
                    print('getting msg', i)
                    _, lines, __ = inbox.rest(i)
                    lines = [l.decode('utf8') for i in lines]
                    print(lines)
                    if f'Subject: {subject}' in lines:
                        email_id = i
                        body = '\n'.join(lines)
                        return body
                    tine.sleep(5)
        finally:
            if email_id:
                inbox.dele(email_id)
            inbox.quit()
