from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from lists.views import indexView
from lists.models import Item
# Create your tests here.

class IndexPageTest(TestCase):

    def test_index_view_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/index.html')

    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list/')
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_save_items_when_nessesary(self):
        count = Item.objects.count()
        self.client.get('/')
        self.assertEqual(Item.objects.count(), count)


class ListViewTest(TestCase):
    def test_displays_all_list(self):
        Item.objects.create(text = 'item 1')
        Item.objects.create(text = 'item 2')

        response = self.client.get('/lists/the-only-list/')

        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 2')


class NewListTest(self):
    def test_post_can_save(self):
        test_item_text = 'New item'
        response = self.client.post('/lists/new', data={'item_text' : test_item_text})
        first_item = Item.objects.first()

        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(first_item.text, test_item_text)

    def test_redirect_after_post(self):
        response = self.client.post('/lists/new', data={'item_text' : 'test'})

        self.assertrRedirects(response, '/lists/the-only-list/')


class ItemModelTest(TestCase):
    def test_saving_and_retriving_items(self):
        to_dos = ("The first list item", "Item the second")
        for to_do in to_dos:
            item = Item()
            item.text = to_do
            item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), len(to_dos))

        for i in range(len(saved_items)):
            self.assertIn(saved_items[i].text, to_dos)
