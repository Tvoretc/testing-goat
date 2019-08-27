from django.test import TestCase
import accounts.views
from accounts.models import Token
from unittest.mock import patch, call

class SendLoginEmailViewTest(TestCase):

    @patch('accounts.views.send_mail')
    def test_sends_mail_to_address_from_post(self, mock_send_mail):
        self.client.post('/accounts/send_login_email', data = {
            'email' : 'a@gmail.com'
        })

        self.assertTrue(mock_send_mail.called)
        (subject, body, from_email, to_email_list), kwargs = mock_send_mail.call_args
        self.assertEqual(subject, 'Your login link for Superlists')
        self.assertEqual(from_email, 'noreply@superlists')
        self.assertEqual(to_email_list, ['a@gmail.com'])

    def test_success_message_after_mail_sent(self):
        response = self.client.post('/accounts/send_login_email',
        data = {'email' : 'a@gmail.com'}, follow = True)

        message = list(response.context['messages'])[0]

        self.assertEqual(message.message,
            'Check your email, we`ve sent you a link to log in.'
        )
        self.assertEqual(message.tags, 'success')

    def test_redirects_to_home(self):
        response = self.client.get('/accounts/login')
        self.assertRedirects(response, '/')

    def test_creates_token_associated_with_email(self):
        response = self.client.post('/accounts/send_login_email', data = {'email':'a@gmail.com'})
        token = Token.objects.first()
        self.assertEquals(token.email, 'a@gmail.com')

    @patch('accounts.views.send_mail')
    def test_sends_link_to_login_using_token_uid(self, mock_send_mail):
        response = self.client.post('/accounts/send_login_email', data = {'email':'a@gmail.com'})
        token = Token.objects.first()

        expected_url = f'http://testserver/accounts/login?token={token.uid}'
        (subject, body, from_email, to_email_list), kwargs = mock_send_mail.call_args
        self.assertIn(expected_url, body)


@patch('accounts.views.auth')
class LoginViewTest(TestCase):
    def test_redirect_home_after_login(self, mock_auth):
        response = self.client.post('/accounts/send_login_email', data={
            'email' : 'a@gmail.com'
        })
        self.assertRedirects(response, '/')

    def test_calls_authenticate_with_uid_from_get_request(self, mock_auth):
        self.client.get('/accounts/login?token=123')
        self.assertEqual(
            mock_auth.authenticate.call_args,
            call('123')
        )

    def test_calls_auth_login_with_user(self, mock_auth):
        response = self.client.get('/accounts/login?token=123')
        self.assertEqual(
            mock_auth.login.call_args,
            call(response.wsgi_request, mock_auth.authenticate.return_value)
        )

    def test_does_not_login_when_not_authenticated(self, mock_auth):
        mock_auth.authenticate.return_value = None
        self.client.get('/accounts/login?token=123')
        self.assertEqual(mock_auth.login.called, False)
