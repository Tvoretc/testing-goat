from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore

from functional_tests.base import FunctionalTest
from functional_tests.my_lists_page import MyListsPage

import time

User = get_user_model()

class MyListsTest(FunctionalTest):

    def test_logged_in_users_list_saved_as_his(self):
        email = 'a@gmail.com'
        self.browser.get(self.live_server_url)
        self.assert_logged_out(email)

        self.create_pre_authenticated_session(email)
        self.browser.get(self.live_server_url)
        self.assert_logged_in(email)

    def test_logged_in_users_lists_are_saves_as_my_lists(self):
        # logs in
        self.create_pre_authenticated_session('a@gmail.com')

        # goes to home page and starts new list
        self.browser.get(self.live_server_url)
        self.add_list_item('Nice list')
        self.add_list_item('second item')
        first_list_url = self.browser.current_url

        # goes to "My lists"
        my_lists_page = MyListsPage(self)
        my_lists_page.get_my_list_link().click()

        # sees new list
        self.browser.find_element_by_link_text('Nice list').click()
        self.assertEqual(self.browser.current_url, first_list_url)

        # starts another list
        self.browser.get(self.live_server_url)
        self.add_list_item('Another list')
        second_list_url = self.browser.current_url

        # new list appears
        self.browser.find_element_by_link_text('My lists').click()
        self.browser.find_element_by_link_text('Another list').click()
        self.assertEqual(self.browser.current_url, second_list_url)

        # logs out, "My lists" disappear
        self.browser.find_element_by_link_text('Log out').click()
        self.assertEquals(self.browser.find_elements_by_link_text('My lists'), [])
