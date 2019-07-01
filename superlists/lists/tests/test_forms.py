from django.test import TestCase

from lists.models import Item, List
from lists.forms import ItemForm, EMPTY_ITEM_ERROR


class ItemFormTest(TestCase):
    def test_form_renders_text_input(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-controll input-lg"', form.as_p())

    def test_form_validation_for_empty_items(self):
        form = ItemForm(data={'text':''})
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['text'], [EMPTY_ITEM_ERROR])

    def test_form_save(self):
        list_ = List.objects.create()
        form = ItemForm(data={'text':'to-do item'})
        new_item = form.save(list_ = list_)
        self.assertEqual(Item.objects.first(), new_item)
        self.assertEqual(new_item.list, list_)
        self.assertEqual(new_item.text, 'to-do item')
