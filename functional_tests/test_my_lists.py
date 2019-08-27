from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore

from functional_tests.base import FunctionalTest

import time

User = get_user_model()

class MyListsTest(FunctionalTest):
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

    def test_logged_in_users_list_saved_as_his(self):
        email = 'a@gmail.com'
        self.browser.get(self.live_server_url)
        self.assert_logged_out(email)

        self.create_pre_authenticated_session(email)
        self.browser.get(self.live_server_url)
        self.assert_logged_in(email)
