from django.urls import resolve
from django.test import TestCase
from lists.views import indexView

# Create your tests here.

class IndexPageTest(TestCase):

    def test_index_url_to_index_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, indexView)
