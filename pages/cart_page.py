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

    # Locators - Updated for Rozetka (2025) - Verified working selectors
    CART_MODAL = (By.CSS_SELECTOR, "rz-modal")
    CART_MODAL_HEADER = (By.CSS_SELECTOR, "rz-modal-layout .header h2")
    CART_ITEMS = (By.CSS_SELECTOR, "rz-cart-product")
    CART_ITEM_BODY = (By.CSS_SELECTOR, ".cart-product__body")
    # Working selector from debug
    CART_ITEM_TITLES = (By.CSS_SELECTOR, ".cart-product__title")
    CART_ITEM_PRICES = (By.CSS_SELECTOR, "rz-cart-product span[class*='price']")
    # Working selector from debug  
    CART_ITEM_QUANTITIES = (
        By.CSS_SELECTOR,
        "rz-cart-product input[formcontrolname='quantity']",
    )
    # Menu buttons for actions (delete, etc)
    CART_ITEM_ACTION_MENU = (By.CSS_SELECTOR, "button[id^='cartProductActions']")
    # Remove button inside menu
    REMOVE_ITEM_BUTTON_IN_MENU = (By.CSS_SELECTOR, "rz-trash-icon > button")
    
    EMPTY_CART_MESSAGE = (By.CSS_SELECTOR, ".cart-dummy__content, .cart-dummy")
    TOTAL_PRICE = (By.CSS_SELECTOR, "div[class*='cart-receipt__sum-price']")
    CHECKOUT_BUTTON = (
        By.XPATH,
        "//button[contains(text(), 'Оформлення замовлення')]",
    )
    CONTINUE_SHOPPING_BUTTON = (By.CSS_SELECTOR, "a.cart-dummy__button, button.cart-dummy__button")
    # Quantity buttons - verified working selectors
    # Button 3rd child = increase, 1st child = decrease
    QUANTITY_INCREASE_BUTTONS = (
        By.CSS_SELECTOR,
        "rz-cart-counter > div > button:nth-child(3)",
    )
    QUANTITY_DECREASE_BUTTONS = (
        By.CSS_SELECTOR,
        "rz-cart-counter > div > button:nth-child(1)",
    )
    CART_HEADER = (
        By.CSS_SELECTOR,
        "h1[class*='cart-page__title'], rz-modal-layout h2",
    )

    def __init__(self, driver):
        """Initialize cart page"""
        super().__init__(driver)
        logger.info("Initialized CartPage")

    def wait_for_cart_load(self, timeout: int = 15) -> bool:
        """
        Wait for cart modal/page to load

        Args:
            timeout: Wait timeout in seconds

        Returns:
            True if loaded
        """
        import time

        logger.info("Waiting for cart to load")
        time.sleep(2)  # Initial wait for page to stabilize

        # Check if modal appeared
        if self.is_element_visible(self.CART_MODAL, timeout=3):
            logger.info("Cart modal appeared")
            time.sleep(1)  # Wait for modal content to load
            return True

        # Otherwise wait for page header
        cart_loaded = self.is_element_visible(self.CART_HEADER, timeout=timeout)
        if cart_loaded:
            logger.info("Cart page loaded")
            time.sleep(1)  # Wait for content to load
        return cart_loaded

    def is_cart_empty(self) -> bool:
        """
        Check if cart is empty

        Returns:
            True if empty
        """
        import time

        time.sleep(0.5)  # Brief wait for stability

        # Check for empty cart message
        if self.is_element_visible(self.EMPTY_CART_MESSAGE, timeout=3):
            logger.info("Cart is empty (empty message visible)")
            return True

        # Check if no cart items exist
        cart_items = self.find_elements(self.CART_ITEMS, timeout=2)
        if not cart_items:
            logger.info(f"Cart is empty (no items found)")
            return True

        logger.info(f"Cart is not empty ({len(cart_items)} items found)")
        return False

    def get_items_count(self) -> int:
        """
        Get number of items in cart

        Returns:
            Number of items
        """
        import time

        # Wait a bit for cart items to render
        time.sleep(1)

        if self.is_cart_empty():
            logger.info("Cart is empty (0 items)")
            return 0

        items = self.find_elements(self.CART_ITEMS, timeout=5)
        count = len(items)
        logger.info(f"Cart has {count} items")
        return count

    def get_item_titles(self) -> List[str]:
        """
        Get list of item titles in cart

        Returns:
            List of titles
        """
        import time

        logger.info("Getting cart item titles")
        if self.is_cart_empty():
            return []

        time.sleep(1)  # Wait for titles to load

        # Use verified working selector
        title_elements = self.find_elements(self.CART_ITEM_TITLES)
        titles = [title.text for title in title_elements if title.text]
        logger.info(f"Found {len(titles)} titles")
        return titles

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
        Remove item from cart by index (using action menu)

        Args:
            index: Item index (0-based)
        """
        import time

        logger.info(f"Removing item at index {index}")

        time.sleep(1)  # Wait for page to stabilize

        # Find all cart items to get the specific item
        cart_items = self.find_elements(self.CART_ITEMS)
        logger.info(f"Found {len(cart_items)} cart items")

        if 0 <= index < len(cart_items):
            cart_item = cart_items[index]
            
            # Scroll to item
            self.execute_script("arguments[0].scrollIntoView({block: 'center'});", cart_item)
            time.sleep(0.5)
            
            # Find action menu button within this cart item
            try:
                action_menu_button = cart_item.find_element(*self.CART_ITEM_ACTION_MENU)
                logger.info(f"Found action menu button for item {index}")
                
                # Click action menu
                self.execute_script("arguments[0].click();", action_menu_button)
                time.sleep(1)  # Wait for menu to appear
                
                # Find and click remove button in menu
                remove_button = cart_item.find_element(*self.REMOVE_ITEM_BUTTON_IN_MENU)
                logger.info(f"Found remove button in menu")
                self.execute_script("arguments[0].click();", remove_button)
                
                time.sleep(2)  # Wait for removal to complete
                logger.info(f"Item {index} removed successfully")
            except Exception as e:
                logger.error(f"Error removing item {index}: {e}")
                raise
        else:
            logger.error(f"Item index {index} out of range (found {len(cart_items)} items)")
            raise IndexError(f"Item index {index} out of range")

    def remove_all_items(self):
        """Remove all items from cart"""
        import time

        logger.info("Removing all items from cart")
        max_attempts = 20  # Prevent infinite loop
        attempts = 0

        while not self.is_cart_empty() and attempts < max_attempts:
            attempts += 1
            logger.info(f"Removal attempt {attempts}")
            
            try:
                self.remove_item(0)
                time.sleep(1)  # Wait for UI update
            except (IndexError, Exception) as e:
                logger.warning(f"Error removing item: {e}")
                # Check if cart is actually empty
                time.sleep(1)
                if self.is_cart_empty():
                    logger.info("Cart is now empty")
                    break
                else:
                    logger.error("Failed to remove item but cart not empty")
                    break

        if attempts >= max_attempts:
            logger.warning(f"Reached max attempts ({max_attempts}) removing items")
        else:
            logger.info("All items removed successfully")

    def increase_item_quantity(self, index: int = 0):
        """
        Increase item quantity using the + button

        Args:
            index: Item index (0-based)
        """
        import time

        logger.info(f"Increasing quantity for item at index {index}")

        # Wait for cart page to fully load
        time.sleep(2)

        # Find all increase buttons
        increase_buttons = self.find_elements(self.QUANTITY_INCREASE_BUTTONS, timeout=10)
        logger.info(f"Found {len(increase_buttons)} increase buttons")

        if not increase_buttons:
            logger.error("No increase buttons found on page")
            raise Exception("No increase buttons found on page")

        if 0 <= index < len(increase_buttons):
            # Scroll to button
            self.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                increase_buttons[index],
            )
            time.sleep(0.5)

            # Click button
            self.execute_script("arguments[0].click();", increase_buttons[index])
            time.sleep(2)  # Wait for quantity update
            logger.info(f"Increased quantity for item {index}")
        else:
            raise IndexError(f"Item index {index} out of range (found {len(increase_buttons)} buttons)")

    def decrease_item_quantity(self, index: int = 0):
        """
        Decrease item quantity using the - button

        Args:
            index: Item index (0-based)
        """
        import time

        logger.info(f"Decreasing quantity for item at index {index}")
        
        time.sleep(1)
        
        # Find all decrease buttons
        decrease_buttons = self.find_elements(self.QUANTITY_DECREASE_BUTTONS)
        logger.info(f"Found {len(decrease_buttons)} decrease buttons")
        
        if 0 <= index < len(decrease_buttons):
            # Scroll to button
            self.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                decrease_buttons[index],
            )
            time.sleep(0.5)
            
            # Click button
            self.execute_script("arguments[0].click();", decrease_buttons[index])
            time.sleep(2)  # Wait for quantity update
            logger.info(f"Decreased quantity for item {index}")
        else:
            raise IndexError(f"Item index {index} out of range")

    def set_item_quantity(self, index: int, quantity: int):
        """
        Set item quantity

        Args:
            index: Item index (0-based)
            quantity: Desired quantity
        """
        import time
        from selenium.webdriver.common.keys import Keys

        logger.info(f"Setting quantity to {quantity} for item at index {index}")
        quantity_inputs = self.find_elements(self.CART_ITEM_QUANTITIES)
        if 0 <= index < len(quantity_inputs):
            input_field = quantity_inputs[index]
            
            # Scroll to input
            self.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_field)
            time.sleep(0.5)
            
            # Clear and set new value
            input_field.click()
            time.sleep(0.3)
            input_field.clear()
            time.sleep(0.3)
            input_field.send_keys(str(quantity))
            time.sleep(0.3)
            input_field.send_keys(Keys.ENTER)  # Confirm the change
            time.sleep(1)
            logger.info(f"Set quantity to {quantity} for item {index}")
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
        import time

        time.sleep(1)  # Wait for page to stabilize

        # Try primary selector
        quantity_inputs = self.find_elements(self.CART_ITEM_QUANTITIES)
        
        if not quantity_inputs:
            # Try alternative selectors
            alternative_selectors = [
                (By.CSS_SELECTOR, "rz-cart-product input[type='text']"),
                (By.CSS_SELECTOR, "rz-cart-product input[class*='counter']"),
                (By.XPATH, "//rz-cart-product//input[@formcontrolname='quantity']"),
            ]

            for selector in alternative_selectors:
                logger.info(f"Trying alternative selector for quantity: {selector}")
                quantity_inputs = self.find_elements(selector)
                if quantity_inputs:
                    break

        if 0 <= index < len(quantity_inputs):
            value = quantity_inputs[index].get_attribute("value")
            logger.info(f"Quantity for item {index}: {value}")
            return int(value)
        
        logger.error(f"Item index {index} out of range (found {len(quantity_inputs)} inputs)")
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
        import time

        logger.info("Continuing shopping")
        
        # Try primary selector
        if self.is_element_visible(self.CONTINUE_SHOPPING_BUTTON, timeout=5):
            self.click(self.CONTINUE_SHOPPING_BUTTON)
            logger.info("Clicked continue shopping button")
            return

        # Try alternative approaches
        alternative_selectors = [
            (By.XPATH, "//button[contains(text(), 'Продовжити покупки')]"),
            (By.XPATH, "//a[contains(text(), 'Продовжити покупки')]"),
            (By.CSS_SELECTOR, "a.cart-dummy__button"),
            (By.CSS_SELECTOR, "button.cart-dummy__button"),
        ]

        for selector in alternative_selectors:
            logger.info(f"Trying alternative selector for continue shopping: {selector}")
            if self.is_element_visible(selector, timeout=3):
                self.click(selector)
                logger.info("Clicked continue shopping via alternative selector")
                return

        logger.warning("Continue shopping button not found - cart might not be empty")

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
