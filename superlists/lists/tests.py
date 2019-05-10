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
        request = HttpRequest()
        response = indexView(request)
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>To-Do lists</title>', html)
        self.assertTrue(html.endswith('</html>'))
