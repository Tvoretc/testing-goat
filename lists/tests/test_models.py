from django.test import TestCase
from django.core.exceptions import ValidationError

from lists.models import Item, List
# Create your tests here.

class ItemModelTest(TestCase):
    def test_item_default_text(self):
        item = Item()
        self.assertEquals(item.text, '')

    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_item_set.all())
    #
    # def test_saving_and_retriving(self):
    #     list_ = List()
    #     list_.save()
    #
    #     to_dos = ("The first list item", "Item the second")
    #     for to_do in to_dos:
    #         item = Item()
    #         item.text = to_do
    #         item.list = list_
    #         item.save()
    #
    #     saved_list = List.objects.first()
    #     self.assertEquals(saved_list, list_)
    #     saved_items = Item.objects.all()
    #     self.assertEqual(saved_items.count(), len(to_dos))
    #
    #     for i in range(len(saved_items)):
    #         self.assertIn(saved_items[i].text, to_dos)
    #         self.assertEquals(saved_items[i].list, list_)

    def test_cant_save_empty_list_item(self):
        list_ = List.objects.create()
        item = Item(list = list_, text = '')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_duplicates_in_same_list(self):
        text = 'text'
        list_ = List.objects.create()
        Item.objects.create(list = list_, text = text)
        with self.assertRaises(ValidationError):
            item = Item(list = list_, text = text)
            item.full_clean()

    def test_duplicates_in_separate_lists(self):
        text = 'text'
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1)
        Item.objects.create(list=list2) # must not raise

    def text_item_ordering(self):
        list_ = List.objects.create()
        item1 = Item.objects.create(list = list_, text = '1st')
        item2 = Item.objects.create(list = list_, text = 'second')
        item3 = Item.objects.create(list = list_, text = '3')
        self.assertEquals(Item.objects.all(), [item1, item2, item3])


class ItemModelTest(TestCase):
    def test_list_has_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f"/lists/{list_.id}/")
    
