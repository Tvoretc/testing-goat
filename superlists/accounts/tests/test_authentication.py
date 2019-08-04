from django.test import TestCase

from accounts.models import Token, User
from accounts.authentication import PasswordlessAuthenticationBackend


class AuthenticationTest(TestCase):
    def test_returns_none_if_no_token(self):
        result = PasswordlessAuthenticationBackend().authenticate('no-such-token')
        self.assertIsNone(result)

    def test_returns_new_user_with_corect_email_if_token_exists(self):
        email = 'a@gmail.com'
        token = Token.objects.create(email = email)
        user = PasswordlessAuthenticationBackend().authenticate(token.uid)
        new_user = User.objects.get(email = email)
        self.assertEqual(user, new_user)

    def test_returns_existing_user_with_correct_email_if_token_exists(self):
        email = 'a@gmail.com'
        existing_user = User.objects.create(email = email)
        token = Token.objects.create(email = email)

        user = PasswordlessAuthenticationBackend().authenticate(token.uid)
        self.assertEqual(user, existing_user)

    def test_logins_user(self):
        Token.objects.create(uid='123', email='a@gmail.com')
        User.objects.create(email='a@gmail.com')
        response = self.client.get('/accounts/login?token=123', follow=True)


class GetUserTest(TestCase):
    def test_returns_none_if_user_doesnt_exist(self):
        self.assertIsNone(
            PasswordlessAuthenticationBackend().get_user('a@gmail.com')
        )

    def test_returns_correct_user(self):
        email = 'a@gmail.com'
        actual_user = User.objects.create(email = email)
        wrong_user = User.objects.create(email = 'b@gmail.com')
        returned_user = PasswordlessAuthenticationBackend().get_user(email)
        self.assertEqual(actual_user, returned_user)
        self.assertNotEqual(wrong_user, returned_user)
