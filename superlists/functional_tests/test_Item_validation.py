from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from unittest import skip
from functional_tests.base import FunctionalTest

@skip
class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_items(self):
        self.fail("write a test")
