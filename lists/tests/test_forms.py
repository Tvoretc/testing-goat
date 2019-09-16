from django.test import TestCase

import unittest
from unittest.mock import patch, Mock

from lists.models import Item, List
from lists.forms import ItemForm, EMPTY_ITEM_ERROR, NewListForm, \
                        ExistingListItemForm, DUPLICATE_ITEM_ERROR


class ItemFormTest(TestCase):
    def test_form_renders_text_input(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-controll input-lg"', form.as_p())

    def test_form_validation_for_empty_items(self):
        form = ItemForm(data={'text':''})
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['text'], [EMPTY_ITEM_ERROR])


class ExistingListItemFormTest(TestCase):
    def test_form_renders_text_input(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(list_ = list_)
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        # self.assertIn('class="form-controll input-lg"', form.as_p())

    def test_form_validation_for_empty_items(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(list_ = list_, data={'text':''})
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['text'], [EMPTY_ITEM_ERROR])

    def test_form_invalid_for_duplicate_items(self):
        list_ = List.objects.create()
        item = Item.objects.create(list = list_, text = 'to-do item')
        form = ExistingListItemForm(list_ = list_, data={'text':'to-do item'})

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR])

    def test_ex_list_form_save(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(list_ = list_, data = {'text' : '123'})
        item = form.save()
        self.assertEqual(item, Item.objects.first())


class NewListFormTest(unittest.TestCase):

    @patch('lists.models.List.create_new')
    def test_save_creates_new_list_form_post_data_if_user_not_authenticted(
        self, mock_List_create_new
    ):
        user - Mock(is_authenticated = False)
        listForm = NewListForm(data = {'text' : 'new item text'})
        # form.is_valid()
        listForm.save(owner = user)
        mock_List_create_new.assert_called_once_with(
            first_item_text = 'new item text'
        )

    @patch('lists.forms.List.create_new')
    def test_save_creates_new_list_form_post_data_if_user_not_authenticted(
        self, mock_List_create_new
    ):
        user = Mock(is_authenticated = True)
        listForm = NewListForm(data = {'text' : 'new item text'})
        # form.is_valid()
        listForm.save(owner = user)
        mock_List_create_new.assert_called_once_with(
            first_item_text = 'new item text', owner = user
        )

    @patch('lists.views.List.create_new')
    def test_save_returns_new_list(self, mock_List_create_new):
        user = Mock(is_authenticated=True)
        form = NewListForm(data={'text':'new list text'})
        returned = form.save(owner=user)
        self.assertEqual(returned, mock_List_create_new())
