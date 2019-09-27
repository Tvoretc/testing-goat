from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model

import os
import time
from datetime import datetime

User = get_user_model()

SCREEN_DUMP_LOCATION = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'screendumps'
)

class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        if os.name == 'nt':
            self.chrome_dir = '../webdrivers/chromedriver.exe'
        else:
            self.chrome_dir = '/usr/bin/chromedriver'
        self.browser = webdriver.Chrome(self.chrome_dir)
        self.staging_server = os.environ.get('STAGING_SERVER')
        if self.staging_server:
            self.live_server_url = 'http://' + staging_server

    def get_table_rows(self):
        return self.browser.find_elements_by_css_selector('#id_list_table tr')

    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')

    def wait(fn):
        def modified_fn(*args, **kwargs):
            start_time = time.time()
            while True:
                try:
                    return fn(*args, **kwargs)
                except (AssertionError, WebDriverException) as e:
                    if time.time() - start_time > 5:
                        raise e
                    time.sleep(0.5)
        return modified_fn

    def assert_item_in_list(self, item):
        rows = self.get_table_rows()
        self.assertTrue(
            any(item in row.text for row in rows),
            f"Item <{item}> did not appeare in a table"
        )

    def assert_items_in_list(self, items):
        rows = self.get_table_rows()
        for item in items:
            self.assertTrue(
                any(item in row.text for row in rows),
                f"Item <{item}> did not appeare in a table"
            )

    @wait
    def assert_logged_in(self, email):
        self.browser.find_element_by_link_text('Log out')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(email, navbar.text)

    @wait
    def assert_logged_out(self, email):
        self.browser.find_element_by_name('email')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(email, navbar.text)

    @wait
    def wait_for_row_in_list_table(self, row_text):
        rows = self.get_table_rows()
        self.assertIn(row_text, [row.text for row in rows])

    @wait
    def wait_for(self, fn):
        return fn()

    def add_list_item(self, item_text):
        self.get_item_input_box().send_keys(item_text)
        self.get_item_input_box().send_keys(Keys.ENTER)
        item_number = len(self.browser.find_elements_by_css_selector('#id_list_table tr')) - 1
        self.wait_for_row_in_list_table(f'{item_number} {item_text}')

    def create_pre_authenticated_session(self, email):
        user = User.objects.create(email=email)
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()

        self.browser.get(self.live_server_url + '/non-existing-url/')
        self.browser.add_cookie(dict(
            name = settings.SESSION_COOKIE_NAME,
            value= session.session_key,
            path = '/',
        ))

###
### tearDown part
###

    def _test_has_failed(self):
        # wut
        return any(error for (method, error) in self._outcome.errors)

    def take_screenshot(self):
        filename = self._get_filename()+'.png'
        print('screenshotting to ', filename)
        self.browser.get_screenshot_as_file(filename)

    def dump_html(self):
        filename = self._get_filename()+'.html'
        print('dumping html page to ', filename)
        with open(filename, 'w') as f:
            f.write(self.browser.page_source)

    def _get_filename(self):
        timestamp = datetime.now().isoformat().replace(':', '.')[:19]
        return '{folder}/{classname}.{method}-window{windowid}-{timestamp}'.format(
            folder = SCREEN_DUMP_LOCATION,
            classname = self.__class__.__name__,
            method = self._testMethodName,
            windowid = self._windowid,
            timestamp = timestamp
        )

    def tearDown(self):
        if self._test_has_failed():
            if not os.path.exists(SCREEN_DUMP_LOCATION):
                os.makedirs(SCREEN_DUMP_LOCATION)
            for ix, handle in enumerate(self.browser.window_handles):
                self._windowid = ix
                self.browser.switch_to_window(handle)
                self.take_screenshot()
                self.dump_html()
        self.browser.quit()
        super().tearDown()
