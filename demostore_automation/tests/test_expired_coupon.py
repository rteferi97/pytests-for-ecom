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
from demostore_automation.src.pages.CheckoutPage import CheckoutPage
from demostore_automation.src.pages.OrderReceivedPage import OrderReceivedPage
from demostore_automation.src.configs.MainConfigs import MainConfigs

url = 'http://localhost:8888/ecomtester/'


@pytest.mark.usefixtures("init_driver")
class TestExpiredCoupon:

    # @pytest.mark.tcid33
    # @pytest.mark.pioneertcid3
    def test_expired_coupon(self):
        # create objects
        home_page = HomePage(self.driver)

        cart_page = CartPage(self.driver)
        header = Header(self.driver)
        checkout_page = CheckoutPage(self.driver)
        order_received = OrderReceivedPage(self.driver)

        # Open browser & Go to homepage
        print("Opening Browser...")
        print("going to homepage...")
        home_page.go_to_home_page()
        # Add item to cart
        home_page.click_first_add_to_cart_button()

        # make sure the cart is updated before going to cart #start here!!!
        header.wait_until_cart_item_count(1)

        # Go to cart
        header.click_on_cart_on_right_header()

        # Apply the expired coupon code
        coupon_code = MainConfigs.get_coupon_code('FREE_COUPON')
        cart_page.apply_coupon(coupon_code)

        # Verify the error message
        # driver.implicitly_wait(10)

        error_box = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.woocommerce-error')))

        # proceed to checkout
        cart_page.click_on_proceed_to_checkout()

