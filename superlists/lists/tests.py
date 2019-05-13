from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from lists.views import indexView

# Create your tests here.

class IndexPageTest(TestCase):

    def test_index_url_resolves_to_index_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, indexView)

    def test_index_view_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/index.html')

    def test_post(self):
        response = self.client.post('/', data={'item_text' : 'New item'})
        self.assertIn('New item', response.content.decode())
        self.assertTemplateUsed(response, 'lists/index.html')
