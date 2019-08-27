from django.test import TestCase
from django.contrib import auth

from accounts.models import Token

User = auth.get_user_model()

class UserModelTest(TestCase):
    def test_user_creates_with_email_only(self):
        user = User(email='a@gmail.com')
        user.full_clean()

    def test_email_is_pk(self):
        user = User(email='a@gmail.com')
        self.assertEqual(user.pk, 'a@gmail.com')

    def test_no_problem_with_auth_login(self):
        user = User.objects.create(email='a@gmail.com')
        user.backend = ''
        request = self.client.request().wsgi_request
        auth.login(request, user)
        self.assertTrue(request.user.is_authenticated)
        # self.assertEqual(request.user.email, 'a@gmail.com')
        # self.assertEqual(user.pk, int(self.client.session['_auth_user_id']))


class TokenModelTest(TestCase):
    def test_tokens_generate_different_uid(self):
        token1 = Token.objects.create(email = 'a@gmail.com')
        token2 = Token.objects.create(email = 'a@gmail.com')
        self.assertNotEqual(token1.uid, token2.uid)
