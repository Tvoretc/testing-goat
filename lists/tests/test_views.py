from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest, HttpResponse
from django.utils.html import escape
from django.contrib.auth import get_user_model
from django.shortcuts import redirect

User = get_user_model()

from unittest.mock import patch
import unittest

from lists.views import indexView, newListView
from lists.models import Item, List
from lists.forms import ItemForm, EMPTY_ITEM_ERROR, ExistingListItemForm, DUPLICATE_ITEM_ERROR
# Create your tests here.

class IndexPageTest(TestCase):

    def test_index_view_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/index.html')

    def test_use_right_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}')
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_view_displays_appropriate_list_items(self):
        first_list_ = List.objects.create()
        Item.objects.create(text = 'item 1', list = first_list_)
        Item.objects.create(text = 'item 2', list = first_list_)

        second_list_ = List.objects.create()
        Item.objects.create(text = 'enother item 1', list = second_list_)
        Item.objects.create(text = 'enother item 2', list = second_list_)

        response = self.client.get(f'/lists/{first_list_.id}')

        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 2')
        self.assertNotContains(response, 'enother item 1')
        self.assertNotContains(response, 'enother item 2')

    def test_passes_correct_list_to_template(self):
        right_list = List.objects.create()
        wrong_list = List.objects.create()

        response = self.client.get(f'/lists/{right_list.id}')
        self.assertEqual(response.context['list'], right_list)

    def test_can_save_to_existing_list(self):
        wrong_list = List.objects.create()
        right_list = List.objects.create()
        wrong_list2 = List.objects.create()

        self.client.post(
            f'/lists/{right_list.id}',
            {'text' : 'right test text 1'}
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
            f'/lists/{right_list.id}',
            {'item_text' : 'right test text'}
        )

        self.assertTemplateUsed(response, 'lists/list.html')

    def test_displays_item_form(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}')
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertContains(response, 'name="text"')

    def test_displays_shared_users(self):
        user = User.objects.create(email='b@gmail.com')
        list_ = List.objects.create()
        list_.shared_with.add(user)
        response = self.client.get(f'/lists/{list_.id}')
        self.assertContains(response, user)

    def test_displays_owner(self):
        user = User.objects.create(email='b@gmail.com')
        list_ = List.objects.create()
        list_.owner = user
        list_.save()
        response = self.client.get(f'/lists/{list_.id}')
        self.assertContains(response, f'Owner: {user}')

#ListViewTest end

class NewListViewIntegratedTest(TestCase):

    def test_post_can_save(self):
        test_item_text = 'New item'
        response = self.client.post(
            '/lists/new',
            data={'text' : test_item_text, 'list_id' : List.objects.create().id}
        )
        first_item = Item.objects.first()

        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(first_item.text, test_item_text)

    def test_redirect_after_post(self):
        response = self.client.post(
            '/lists/new',
            data={'text' : 'test'}
        )
        list_id = List.objects.first().id
        self.assertRedirects(response, f'/lists/{list_id}')

    def test_list_owner_saved_if_authenticated(self): #, mockListClass, mockItemFormClass, mock_redirect):
        user = User.objects.create(email='a@gmail.com')
        self.client.force_login(user)

        self.client.post('/lists/new', data={'text':'new item'})
        # mocked_list = mockListClass.return_value
        list_ = List.objects.first()

        # mocked_list.save.assert_called_once_with()
        self.assertEqual(list_.owner, user)


@patch('lists.views.NewListForm')
class NewListUnitTest(unittest.TestCase):

    def setUp(self):
        self.request = HttpRequest()
        self.request.POST['text'] = 'new list item'
        self.request.user = User()

    @patch('lists.views.redirect')
    def test_passes_POST_data_to_NewListForm(
        self, mock_redirect, mockNewListForm
    ):
        newListView(self.request)
        mockNewListForm.assert_called_once_with(data=self.request.POST)

    @patch('lists.views.redirect')
    def test_saves_owner_if_form_valid(
        self, mock_redirect, mockNewListForm
    ):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = True
        newListView(self.request)
        mock_form.save.assert_called_once_with(owner=self.request.user)

    def test_doesnt_save_owner_if_form_invalid(
        self, mockNewListForm
    ):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = False
        newListView(self.request)
        self.assertFalse(mock_form.save.called)

    @patch('lists.views.redirect')
    def test_redirects_to_form_returned_object_if_form_valid(
        self, mock_redirect, mockNewListForm
    ):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = True

        response = newListView(self.request)

        self.assertEqual(response, mock_redirect.return_value)
        mock_redirect.assert_called_once_with(mock_form.save.return_value)

    @patch('lists.views.render')
    def test_redirects_home_if_form_invalid(self, mock_render, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = False

        response = newListView(self.request)

        self.assertEqual(response, mock_render.return_value)
        mock_render.assert_called_once_with(self.request, 'lists/index.html', {'form': mock_form})


class NewItemTest(TestCase):

    def post_invalid_item(self):
        list_ = List.objects.create()
        return self.client.post(
            f'/lists/{list_.id}',
            data={'text' : ''},
        )

    def test_invalid_input_doesnt_save_item(self):
        self.post_invalid_item()
        self.assertEquals(Item.objects.count(), 0)

    def test_invalid_input_returns_list_template(self):
        response = self.post_invalid_item()
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_invalid_input_returns_form(self):
        response = self.post_invalid_item()
        # print(response)
        self.assertIsInstance(response.context.get('form', None), ExistingListItemForm)

    def test_invalid_input_returns_error(self):
        response = self.post_invalid_item()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_validation_error_shown_on_page(self):
        response = self.client.post(
            '/lists/new',
            data={'text' : ''}
        )
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_after_invalid_input_passes_form(self):
        response = self.client.post(
            '/lists/new',
            data={'text' : ''}
        )
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_empty_items_are_not_saved(self):
        response = self.client.post(
            '/lists/new',
            data={'text' : ''}
        )
        self.assertEquals(Item.objects.count(), 0)
        self.assertEquals(List.objects.count(), 0)

    def test_duplicates_validate_error_and_endupon_listpage(self):
        list_ = List.objects.create()
        item = Item.objects.create(list = list_, text = '123456')
        response = self.client.post(f'/lists/{list_.id}', data={'text':'123456'})

        self.assertContains(response, DUPLICATE_ITEM_ERROR)
        self.assertTemplateUsed('lists/list.html')
        self.assertEquals(Item.objects.count(), 1)


# all lists of one user
class MyListsViewTest(TestCase):

    def test_renders_right_template(self):
        User.objects.create(email='a@gmail.com')
        response = self.client.get('/lists/users/a@gmail.com')
        self.assertTemplateUsed(response, 'lists/my_lists.html')

    def test_passes_correct_owner(self):
        User.objects.create(email='wrong@gmail.com')
        correct_user = User.objects.create(email='right@gmail.com')
        response = self.client.get('/lists/users/right@gmail.com')
        self.assertEqual(response.context['owner'], correct_user)

    def test_displays_shared_lists(self):
        user = User.objects.create(email = 'a@gmail.com')
        list_ = List.objects.create()
        list_.shared_with.add(user)
        response = self.client.get('/lists/users/a@gmail.com')
        self.assertContains(response, list_)

#MyListsViewTest end

class ListShareViewTest(TestCase):

    def test_post_redirects_to_list_page(self):
        # print('\n=====\ntest started\n=====\n')
        user = User.objects.create(email='a@gmail.com')
        list_ = List.objects.create()
        response = self.client.post(
            f"/lists/{list_.id}/share",
            data={'share_email':user.email}
        )
        # print(f'\n==\ngot {response}\n==\n')
        self.assertRedirects(response, f'/lists/{list_.id}')
        # print('\n=====\ntest ended\n=====\n')

    def test_user_added_to_shared(self):
        user = User.objects.create(email='a@gmail.com')
        list_ = List.objects.create()
        response = self.client.post(
            f"/lists/{list_.id}/share",
            data={'share_email' : user.email}
        )
        self.assertIn(user, list_.shared_with.all())
