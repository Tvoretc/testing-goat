from selenium.webdriver.common.keys import Keys
from functional_tests.base import FunctionalTest

class LayoutAndStylingTest(FunctionalTest):
        def test_styling_and_layout(self):
            self.browser.get(self.live_server_url)
            self.browser.set_window_size(1024,768)

            inputbox = self.get_item_input_box()
            self.assertAlmostEqual(
                inputbox.location['x'] + inputbox.size['width'] / 2,
                512,
                delta = 10
            )

            inputbox.send_keys('test')
            inputbox.send_keys(Keys.ENTER)

            inputbox = self.get_item_input_box()
            self.assertAlmostEqual(
                inputbox.location['x'] + inputbox.size['width'] / 2,
                512,
                delta = 10
            )
