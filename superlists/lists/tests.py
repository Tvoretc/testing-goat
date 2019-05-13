from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from lists.views import indexView
from lists.models import Item
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


class ItemModelTest(TestCase):
    def test_saying_and_retriving_items(self):
        to_dos = ("The first list item", "Item the second")
        for to_do in to_dos:
            item = Item()
            item.text = to_do
            item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), len(to_dos))

        for i in range(len(saved_items)):
            self.assertIn(saved_items[i].text, to_dos)
