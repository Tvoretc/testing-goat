from selenium import webdriver
from functional_tests.base import FunctionalTest
from functional_tests.list_page import ListPage
from functional_tests.my_lists_page import MyListsPage


def quit_if_possible(browser):
    try: browser.quit()
    except: pass


class SharingTest(FunctionalTest):

    def test_can_share_a_list_with_another_user(self):
        # user A logs in
        self.create_pre_authenticated_session('a@gmail.com')
        a_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(a_browser))

        # user B also logs in
        b_browser = webdriver.Chrome(self.chrome_dir)
        self.addCleanup(lambda: quit_if_possible(b_browser))
        self.browser = b_browser
        self.create_pre_authenticated_session('b@gmail.com')

        # A starts list
        self.browser = a_browser
        self.browser.get(self.live_server_url)
        self.add_list_item('Shared list')
        list_page = ListPage(self)

        # A shares list
        list_page.share_list_with('b@gmail.com')
        list_page.assert_email_in_share_list('b@gmail.com')

        # B goes to my lists page
        self.browser = b_browser
        my_list_page = MyListPage(self)
        my_list_page.go_to_my_lists_page()
        self.browser.find_element_by_link_text('Shared list').click()

        # B can see list`s owner
        self.wait_for(lambda: self.assertEqual(
            list_page.get_list_owner(),
            'a@gmail.com'
        ))

        # B adds an item to the list
        list_page.add_list_item('Item from B')

        # A sees new item
        self.browser = a_browser
        self.browser.refresh()
        list_page.wait_for_row_in_list_table('Item from B', 2)
