"""
Search Results Page Module

This module contains the page object for Rozetka search results page.
"""

from selenium.webdriver.common.by import By
import logging
from typing import List

from pages.base_page import BasePage


logger = logging.getLogger(__name__)


class SearchPage(BasePage):
    """Search results page of Rozetka"""

    # Locators - Updated for current Rozetka layout (2025)
    # Multiple fallback selectors for robustness
    SEARCH_RESULTS = (By.XPATH, "//*[contains(@class, 'tile') or contains(@class, 'product') or contains(@class, 'goods')]")
    PRODUCT_TILES = (By.XPATH, "//*[contains(@class, 'tile') or contains(@class, 'product-card')]")
    PRODUCT_TITLES = (By.XPATH, "//a[contains(@class, 'title') or contains(@class, 'heading')]")
    PRODUCT_PRICES = (By.XPATH, "//*[contains(@class, 'price') and not(contains(@class, 'old'))]")
    SORT_DROPDOWN = (By.ID, "sort")  # ✓ Updated from HTML - select#sort
    SORT_BY_PRICE_ASC = (By.XPATH, "//option[@value='cheap']")  # ✓ value='cheap'
    SORT_BY_PRICE_DESC = (By.XPATH, "//option[@value='expensive']")  # ✓ value='expensive'
    SORT_BY_POPULARITY = (By.XPATH, "//option[@value='popularity' or @value='popular']")
    SORT_BY_NOVELTY = (By.XPATH, "//option[@value='novelty']")  # ✓ value='novelty'
    SORT_BY_RATING = (By.XPATH, "//option[@value='rank']")  # ✓ value='rank'
    SORT_BY_ACTION = (By.XPATH, "//option[contains(text(), 'кці') or contains(text(), 'sale')]")
    NO_RESULTS_MESSAGE = (
        By.XPATH,
        "//*[contains(@class, 'empty') or contains(@class, 'nothing') or contains(@class, 'not-found')]",
    )  # ✓ From parser
    SEARCH_QUERY_TEXT = (By.XPATH, "//h1[contains(@class, 'heading') or contains(@class, 'title')]")
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, "rz-buy-button button")
    PAGINATION = (By.CSS_SELECTOR, "ul[class*='pagination'], div[class*='pagination']")
    NEXT_PAGE_BUTTON = (By.XPATH, "//a[contains(@class, 'next') or contains(@class, 'forward')]")
    FILTER_SIDEBAR = (By.XPATH, "//div[contains(@class, 'filter') or contains(@class, 'sidebar')]")  # ✓ From parser
    PRICE_MIN_INPUT = (By.XPATH, "//input[contains(@name, 'min') or contains(@placeholder, 'мін')]")
    PRICE_MAX_INPUT = (By.XPATH, "//input[contains(@name, 'max') or contains(@placeholder, 'макс')]")
    APPLY_FILTER_BUTTON = (
        By.XPATH,
        "//button[contains(text(), 'астосувати') or contains(text(), 'Apply') or contains(@class, 'apply')]",
    )

    def __init__(self, driver):
        """Initialize search page"""
        super().__init__(driver)
        logger.info("Initialized SearchPage")

    def wait_for_results(self, timeout: int = 10) -> bool:
        """
        Wait for search results to load

        Args:
            timeout: Wait timeout in seconds

        Returns:
            True if results loaded
        """
        import time

        logger.info("Waiting for search results to load...")

        # Wait for URL to change
        start_time = time.time()
        url_changed = False
        while (time.time() - start_time) < 5:
            current_url = self.driver.current_url
            if "search" in current_url or "catalog" in current_url:
                logger.info(f"✓ URL changed to results page: {current_url}")
                url_changed = True
                break
            time.sleep(0.3)

        if not url_changed:
            logger.warning("⚠ URL didn't change to search results page")
            return False

        # Wait briefly for page to stabilize
        time.sleep(1)

        # Try to find product elements
        try:
            if self.is_element_visible(self.PRODUCT_TILES, timeout=3):
                logger.info("✓ Product tiles found")
                return True

            if self.is_element_visible(self.PRODUCT_PRICES, timeout=3):
                logger.info("✓ Product prices found")
                return True

            logger.warning("No clear indication of search results")
            return False

        except Exception as e:
            logger.warning(f"Error waiting for results: {e}")
            return False

    def get_products_count(self) -> int:
        """
        Get number of products on current page (tries multiple selectors)

        Returns:
            Number of products
        """
        import time

        time.sleep(1)  # Let page stabilize

        # Try multiple ways to count products
        products = self.find_elements(self.PRODUCT_TILES)
        if products:
            count = len(products)
            logger.info(f"✓ Found {count} products via PRODUCT_TILES")
            return count

        # Try counting by prices
        prices = self.find_elements(self.PRODUCT_PRICES)
        if prices:
            count = len(prices)
            logger.info(f"✓ Found {count} products via PRODUCT_PRICES")
            return count

        logger.warning("No products found with any selector")
        return 0

    def get_product_titles(self) -> List[str]:
        """
        Get list of product titles

        Returns:
            List of product titles
        """
        logger.info("Getting product titles")
        titles = self.find_elements(self.PRODUCT_TITLES)
        return [title.text for title in titles if title.text]

    def get_product_prices(self) -> List[float]:
        """
        Get list of product prices

        Returns:
            List of prices as floats
        """
        logger.info("Getting product prices")
        price_elements = self.find_elements(self.PRODUCT_PRICES)
        prices = []

        for price_elem in price_elements:
            try:
                # Remove non-numeric characters and convert to float
                price_text = price_elem.text.replace(" ", "").replace("₴", "")
                prices.append(float(price_text))
            except ValueError:
                logger.warning(f"Could not parse price: {price_elem.text}")
                continue

        logger.info(f"Got {len(prices)} prices")
        return prices

    def sort_by(self, sort_option: str):
        """
        Sort products by specified option

        Args:
            sort_option: Sort option ('price_asc', 'price_desc', 'popularity', 'novelty', 'action', 'rating')
        """
        import time
        from selenium.webdriver.support.ui import Select

        logger.info(f"Sorting by: {sort_option}")

        time.sleep(1)  # Brief wait for dropdown

        # Map sort options to select values
        sort_values = {
            "price_asc": "cheap",
            "price_desc": "expensive",
            "popularity": "popularity",
            "novelty": "novelty",
            "rating": "rank",
        }

        if sort_option not in sort_values:
            raise ValueError(f"Unknown sort option: {sort_option}")

        try:
            # Find the select element
            select_element = self.find_element(self.SORT_DROPDOWN, timeout=10)

            # Use Selenium Select class
            select = Select(select_element)
            select.select_by_value(sort_values[sort_option])

            time.sleep(2)  # Wait for page to reload with sorted results
            logger.info(
                f"Successfully sorted by {sort_option} (value={sort_values[sort_option]})"
            )
        except Exception as e:
            logger.error(f"Failed to sort by {sort_option}: {e}")
            raise

    def is_sorted_by_price_ascending(self) -> bool:
        """
        Check if products are sorted by price in ascending order

        Returns:
            True if sorted correctly
        """
        prices = self.get_product_prices()
        is_sorted = all(prices[i] <= prices[i + 1] for i in range(len(prices) - 1))
        logger.info(f"Is sorted by price ascending: {is_sorted}")
        return is_sorted

    def is_sorted_by_price_descending(self) -> bool:
        """
        Check if products are sorted by price in descending order

        Returns:
            True if sorted correctly
        """
        prices = self.get_product_prices()
        is_sorted = all(prices[i] >= prices[i + 1] for i in range(len(prices) - 1))
        logger.info(f"Is sorted by price descending: {is_sorted}")
        return is_sorted

    def has_results(self) -> bool:
        """
        Check if search has results

        Returns:
            True if has results
        """
        has_products = self.get_products_count() > 0
        logger.info(f"Has search results: {has_products}")
        return has_products

    def has_no_results(self) -> bool:
        """
        Check if search has no results

        Returns:
            True if no results
        """
        return self.is_element_visible(self.NO_RESULTS_MESSAGE, timeout=5)

    def get_search_query_text(self) -> str:
        """
        Get search query text from page heading

        Returns:
            Search query text
        """
        return self.get_text(self.SEARCH_QUERY_TEXT)

    def click_product(self, index: int = 0):
        """
        Click on product by index

        Args:
            index: Product index (0-based)
        """
        logger.info(f"Clicking product at index {index}")
        products = self.find_elements(self.PRODUCT_TILES)
        if 0 <= index < len(products):
            products[index].click()
        else:
            raise IndexError(f"Product index {index} out of range")

    def add_product_to_cart(self, index: int = 0):
        """
        Add product to cart by index

        Args:
            index: Product index (0-based)
        """
        import time

        logger.info(f"Adding product at index {index} to cart")

        # Wait for add to cart buttons
        time.sleep(1)
        add_buttons = self.find_elements(self.ADD_TO_CART_BUTTONS, timeout=10)

        logger.info(f"Found {len(add_buttons)} add to cart buttons")

        if not add_buttons:
            logger.error("No add to cart buttons found")
            logger.error(f"Current URL: {self.driver.current_url}")
            raise Exception("No add to cart buttons found on page")

        if 0 <= index < len(add_buttons):
            # Scroll to button
            logger.info(f"Scrolling to button {index}")
            self.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                add_buttons[index],
            )
            time.sleep(0.5)

            # Click button
            try:
                logger.info(f"Clicking add to cart button {index}")
                self.execute_script("arguments[0].click();", add_buttons[index])
                logger.info("Button clicked, waiting for cart update...")
                time.sleep(2)  # Wait for cart counter to update

                # Check if modal appeared and close it
                modal_locator = (By.CSS_SELECTOR, "rz-modal rz-modal-layout")
                if self.is_element_visible(modal_locator, timeout=3):
                    logger.info("Modal appeared, closing...")
                    # Press Escape key to close modal
                    from selenium.webdriver.common.keys import Keys

                    self.driver.find_element(By.TAG_NAME, "body").send_keys(
                        Keys.ESCAPE
                    )
                    logger.info("Closed modal via Escape key")
                    time.sleep(0.5)

                logger.info(f"Successfully added product {index} to cart")
            except Exception as e:
                logger.error(f"Failed to add product to cart: {e}")
                raise
        else:
            raise IndexError(
                f"Product index {index} out of range (found {len(add_buttons)} buttons)"
            )

    def set_price_filter(self, min_price: int = None, max_price: int = None):
        """
        Set price filter

        Args:
            min_price: Minimum price
            max_price: Maximum price
        """
        logger.info(f"Setting price filter: min={min_price}, max={max_price}")

        if min_price is not None:
            self.input_text(self.PRICE_MIN_INPUT, str(min_price))

        if max_price is not None:
            self.input_text(self.PRICE_MAX_INPUT, str(max_price))

        self.click(self.APPLY_FILTER_BUTTON)

    def go_to_next_page(self):
        """Go to next page of results"""
        logger.info("Going to next page")
        if self.is_element_visible(self.NEXT_PAGE_BUTTON, timeout=5):
            self.click(self.NEXT_PAGE_BUTTON)
        else:
            logger.warning("Next page button not found")

    def has_pagination(self) -> bool:
        """
        Check if pagination exists

        Returns:
            True if pagination exists
        """
        return self.is_element_visible(self.PAGINATION, timeout=3)
