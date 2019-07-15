from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.models import Token

User = get_user_model()

class UserModelTest(TestCase):
    def test_user_creates_with_email_only(self):
        user = User(email='a@gmail.com')
        user.full_clean()

    def test_email_is_pk(self):
        user = User(email='a@gmail.com')
        self.assertEqual(user.pk, 'a@gmail.com')

class TokenModelTest(TestCase):
    def test_tokens_generate_different_uid(self):
        token1 = Token.objects.create(email = 'a@gmail.com')
        token2 = Token.objects.create(email = 'a@gmail.com')
        self.assertNotEqual(token1.uid, token2.uid)
