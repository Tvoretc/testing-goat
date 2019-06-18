from django.test import TestCase
from django.core.exceptions import ValidationError

from lists.models import Item, List
# Create your tests here.

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

    def test_cant_save_empty_list_item(self):
        list_ = List.objects.create()
        item = Item(list = list_, text = '')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_list_has_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f"/lists/{list_.id}/")
