from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from lists.views import indexView
from lists.models import Item, List
# Create your tests here.

class IndexPageTest(TestCase):

    def test_index_view_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/index.html')


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_view_displays_appropriate_list_items(self):
        first_list_ = List.objects.create()
        Item.objects.create(text = 'item 1', list = first_list_)
        Item.objects.create(text = 'item 2', list = first_list_)

        second_list_ = List.objects.create()
        Item.objects.create(text = 'enother item 1', list = second_list_)
        Item.objects.create(text = 'enother item 2', list = second_list_)

        response = self.client.get(f'/lists/{first_list_.id}/')

        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 2')
        self.assertNotContains(response, 'enother item 1')
        self.assertNotContains(response, 'enother item 2')

    def test_passes_correct_list_to_template(self):
        right_list = List.objects.create()
        wrong_list = List.objects.create()

        response = self.client.get(f'/lists/{right_list.id}/')
        self.assertEqual(response.context['list'], right_list)

class NewListTest(TestCase):
    def test_post_can_save(self):
        test_item_text = 'New item'
        response = self.client.post('/lists/new', data={'item_text' : test_item_text, 'list_id' : List.objects.create().id})
        first_item = Item.objects.first()

        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(first_item.text, test_item_text)

    def test_redirect_after_post(self):
        response = self.client.post('/lists/new', data={'item_text' : 'test'})
        list_id = List.objects.first().id
        self.assertRedirects(response, f'/lists/{list_id}/')


class NewItemTest(TestCase):
    def test_can_save_to_existing_list(self):
        wrong_list = List.objects.create()
        right_list = List.objects.create()
        wrong_list2 = List.objects.create()

        self.client.post(
            f'/lists/{right_list.id}/add_item',
            {'item_text' : 'right test text 1'}
        )

        self.assertEquals(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEquals(new_item.text, 'right test text 1')
        self.assertEquals(new_item.list, right_list)

    def test_redirect_to_list_view(self):
        wrong_list = List.objects.create()
        right_list = List.objects.create()
        wrong_list2 = List.objects.create()

        response = self.client.post(
            f'/lists/{right_list.id}/add_item',
            {'item_text' : 'right test text'}
        )

        self.assertRedirects(response, f'/lists/{right_list.id}/')


class ListAndItemModelTest(TestCase):
    def test_saving_and_retriving(self):
        list_ = List()
        list_.save()

        to_dos = ("The first list item", "Item the second")
        for to_do in to_dos:
            item = Item()
            item.text = to_do
            item.list = list_
            item.save()

        saved_list = List.objects.first()
        self.assertEquals(saved_list, list_)
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), len(to_dos))

        for i in range(len(saved_items)):
            self.assertIn(saved_items[i].text, to_dos)
            self.assertEquals(saved_items[i].list, list_)
