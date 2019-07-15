from django.test import TestCase
import accounts.views
from unittest.mock import patch, call

class SendLoginEmailViewTest(TestCase):
    def test_redirect_home_after_login(self):
        response = self.client.post('/accounts/send_login_email', data={
            'email' : 'a@gmail.com'
        })
        self.assertRedirects(response, '/')

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
        response = self.client.get('/accounts/login?token=1234567890')
        self.assertRedirects(response, '/')
