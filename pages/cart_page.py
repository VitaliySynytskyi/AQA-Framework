"""
Cart Page Module

This module contains the page object for Rozetka shopping cart page.
"""

from selenium.webdriver.common.by import By
import logging
from typing import List, Dict

from pages.base_page import BasePage


logger = logging.getLogger(__name__)


class CartPage(BasePage):
    """Shopping cart page of Rozetka"""

    # Locators
    CART_ITEMS = (By.CSS_SELECTOR, "li[class*='cart-product']")
    CART_ITEM_TITLES = (By.CSS_SELECTOR, "a[class*='cart-product__title']")
    CART_ITEM_PRICES = (By.CSS_SELECTOR, "span[class*='cart-product__price']")
    CART_ITEM_QUANTITIES = (By.CSS_SELECTOR, "input[class*='cart-counter__input']")
    REMOVE_ITEM_BUTTONS = (By.CSS_SELECTOR, "button[class*='cart-product__remove']")
    EMPTY_CART_MESSAGE = (By.CSS_SELECTOR, "div[class*='cart-dummy']")
    TOTAL_PRICE = (By.CSS_SELECTOR, "div[class*='cart-receipt__sum-price']")
    CHECKOUT_BUTTON = (By.XPATH, "//button[contains(text(), 'Оформлення замовлення')]")
    CONTINUE_SHOPPING_BUTTON = (By.CSS_SELECTOR, "a[class*='cart-dummy__button']")
    QUANTITY_INCREASE_BUTTONS = (By.CSS_SELECTOR, "button[class*='cart-counter__button--plus']")
    QUANTITY_DECREASE_BUTTONS = (By.CSS_SELECTOR, "button[class*='cart-counter__button--minus']")
    CART_HEADER = (By.CSS_SELECTOR, "h1[class*='cart-page__title']")

    def __init__(self, driver):
        """Initialize cart page"""
        super().__init__(driver)
        logger.info("Initialized CartPage")

    def wait_for_cart_load(self, timeout: int = 10) -> bool:
        """
        Wait for cart page to load

        Args:
            timeout: Wait timeout in seconds

        Returns:
            True if loaded
        """
        logger.info("Waiting for cart to load")
        return self.is_element_visible(self.CART_HEADER, timeout=timeout)

    def is_cart_empty(self) -> bool:
        """
        Check if cart is empty

        Returns:
            True if empty
        """
        is_empty = self.is_element_visible(self.EMPTY_CART_MESSAGE, timeout=5)
        logger.info(f"Is cart empty: {is_empty}")
        return is_empty

    def get_items_count(self) -> int:
        """
        Get number of items in cart

        Returns:
            Number of items
        """
        if self.is_cart_empty():
            return 0

        items = self.find_elements(self.CART_ITEMS)
        count = len(items)
        logger.info(f"Cart has {count} items")
        return count

    def get_item_titles(self) -> List[str]:
        """
        Get list of item titles in cart

        Returns:
            List of titles
        """
        logger.info("Getting cart item titles")
        if self.is_cart_empty():
            return []

        title_elements = self.find_elements(self.CART_ITEM_TITLES)
        return [title.text for title in title_elements if title.text]

    def get_item_prices(self) -> List[float]:
        """
        Get list of item prices in cart

        Returns:
            List of prices
        """
        logger.info("Getting cart item prices")
        if self.is_cart_empty():
            return []

        price_elements = self.find_elements(self.CART_ITEM_PRICES)
        prices = []

        for price_elem in price_elements:
            try:
                price_text = price_elem.text.replace(" ", "").replace("₴", "")
                prices.append(float(price_text))
            except ValueError:
                logger.warning(f"Could not parse price: {price_elem.text}")
                continue

        return prices

    def get_total_price(self) -> float:
        """
        Get total cart price

        Returns:
            Total price
        """
        logger.info("Getting total cart price")
        if self.is_cart_empty():
            return 0.0

        total_text = self.get_text(self.TOTAL_PRICE)
        try:
            price_text = total_text.replace(" ", "").replace("₴", "")
            return float(price_text)
        except ValueError:
            logger.error(f"Could not parse total price: {total_text}")
            return 0.0

    def remove_item(self, index: int = 0):
        """
        Remove item from cart by index

        Args:
            index: Item index (0-based)
        """
        logger.info(f"Removing item at index {index}")
        remove_buttons = self.find_elements(self.REMOVE_ITEM_BUTTONS)
        if 0 <= index < len(remove_buttons):
            remove_buttons[index].click()
        else:
            raise IndexError(f"Item index {index} out of range")

    def remove_all_items(self):
        """Remove all items from cart"""
        logger.info("Removing all items from cart")
        while not self.is_cart_empty():
            self.remove_item(0)

    def increase_item_quantity(self, index: int = 0):
        """
        Increase item quantity

        Args:
            index: Item index (0-based)
        """
        logger.info(f"Increasing quantity for item at index {index}")
        increase_buttons = self.find_elements(self.QUANTITY_INCREASE_BUTTONS)
        if 0 <= index < len(increase_buttons):
            increase_buttons[index].click()
        else:
            raise IndexError(f"Item index {index} out of range")

    def decrease_item_quantity(self, index: int = 0):
        """
        Decrease item quantity

        Args:
            index: Item index (0-based)
        """
        logger.info(f"Decreasing quantity for item at index {index}")
        decrease_buttons = self.find_elements(self.QUANTITY_DECREASE_BUTTONS)
        if 0 <= index < len(decrease_buttons):
            decrease_buttons[index].click()
        else:
            raise IndexError(f"Item index {index} out of range")

    def set_item_quantity(self, index: int, quantity: int):
        """
        Set item quantity

        Args:
            index: Item index (0-based)
            quantity: Desired quantity
        """
        logger.info(f"Setting quantity to {quantity} for item at index {index}")
        quantity_inputs = self.find_elements(self.CART_ITEM_QUANTITIES)
        if 0 <= index < len(quantity_inputs):
            quantity_inputs[index].clear()
            quantity_inputs[index].send_keys(str(quantity))
        else:
            raise IndexError(f"Item index {index} out of range")

    def get_item_quantity(self, index: int) -> int:
        """
        Get item quantity

        Args:
            index: Item index (0-based)

        Returns:
            Item quantity
        """
        quantity_inputs = self.find_elements(self.CART_ITEM_QUANTITIES)
        if 0 <= index < len(quantity_inputs):
            return int(quantity_inputs[index].get_attribute("value"))
        raise IndexError(f"Item index {index} out of range")

    def is_item_in_cart(self, product_title: str) -> bool:
        """
        Check if specific product is in cart

        Args:
            product_title: Product title to check

        Returns:
            True if product in cart
        """
        logger.info(f"Checking if '{product_title}' is in cart")
        titles = self.get_item_titles()
        return any(product_title.lower() in title.lower() for title in titles)

    def proceed_to_checkout(self):
        """Proceed to checkout"""
        logger.info("Proceeding to checkout")
        if not self.is_cart_empty():
            self.click(self.CHECKOUT_BUTTON)
        else:
            logger.warning("Cannot checkout - cart is empty")

    def continue_shopping(self):
        """Continue shopping (when cart is empty)"""
        logger.info("Continuing shopping")
        if self.is_cart_empty():
            self.click(self.CONTINUE_SHOPPING_BUTTON)

    def get_cart_summary(self) -> Dict:
        """
        Get cart summary with all details

        Returns:
            Dictionary with cart details
        """
        logger.info("Getting cart summary")
        return {
            "is_empty": self.is_cart_empty(),
            "items_count": self.get_items_count(),
            "titles": self.get_item_titles(),
            "prices": self.get_item_prices(),
            "total_price": self.get_total_price(),
        }
