from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pytest
from demostore_automation.src.pages.HomePage import HomePage
from demostore_automation.src.pages.CartPage import CartPage
from demostore_automation.src.pages.Header import Header
from demostore_automation.src.configs.MainConfigs import MainConfigs
import logging as logger

@pytest.mark.usefixtures("init_driver")
class TestExpiredCoupon:

    # @pytest.mark.tcid33
    # @pytest.mark.pioneertcid3
    def test_expired_coupon(self):
        # create objects
        home_page = HomePage(self.driver)
        cart_page = CartPage(self.driver)
        header = Header(self.driver)

        # Go to homepage

        logger.info("Going to homepage...")
        home_page.go_to_home_page()

        # Add item to cart
        home_page.click_first_add_to_cart_button()

        # make sure the cart is updated before going to cart
        header.wait_until_cart_item_count(1)

        # Go to cart
        header.click_on_cart_on_right_header()

        # Apply the expired coupon code
        coupon_code = MainConfigs.get_coupon_code('FREE_COUPON')
        cart_page.apply_coupon(coupon_code)
        # it won't work if i write...
        # elif filter.upper() == 'EXPIRED_COUPON':
        # return "LB100"
        # Verify the error message
        error_message = cart_page.get_displayed_error_message()
        if error_message == 'This coupon has expired.':
            assert "Success"# should i use 'assert' instead of 'return'?
        else:
            assert "failure"# should i use 'assert' instead of 'return'?

