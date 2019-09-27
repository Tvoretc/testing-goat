from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from lists.models import Item, List
# Create your tests here.
User = get_user_model()

class ItemModelTest(TestCase):
    def test_item_default_text(self):
        item = Item()
        self.assertEquals(item.text, '')

    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())
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


class ListModelTest(TestCase):

    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f"/lists/{list_.id}")

    def test_create_new_makes_list_and_item(self):
        List.create_new(first_item_text='new item text')
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'new item text')
        new_list = List.objects.first()
        self.assertEqual(new_list, new_item.list)

    def test_create_new_optionally_saves_owner(self):
        user = User.objects.create()
        List.create_new(first_item_text='new item text', owner=user)
        new_list = List.objects.first()
        self.assertEqual(new_list.owner, user)

    def test_list_can_have_owner(self):
        List(owner=User())

    def test_list_owner_is_optional(self):
        List().full_clean()

    def test_create_new_returns_new_list(self):
        returned = List.create_new(first_item_text = 'new item text')
        self.assertEqual(List.objects.first(), returned)

    def test_list_name_is_first_item_text(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='first item')
        Item.objects.create(list=list_, text='second item')
        self.assertEqual(list_.name, 'first item')

    #shared_with
    def test_shared_with_adds(self):
        list_ = List.objects.create()
        user = User.objects.create(email = 'b@gmail.com')
        list_.shared_with.add(user)
        self.assertIn(user, list_.shared_with.all())
