"""
Home Page Module

This module contains the page object for Rozetka home page.
"""

from selenium.webdriver.common.by import By
import logging

from pages.base_page import BasePage


logger = logging.getLogger(__name__)


class HomePage(BasePage):
    """Home page of Rozetka"""

    # Locators (updated with actual Rozetka selectors 2025)
    SEARCH_INPUT = (By.NAME, "search")  # ✓ Verified working
    SEARCH_BUTTON = (
        By.CSS_SELECTOR,
        "rz-search-suggest form button[type='submit']",
    )  # ✓ Nov 2025 - more specific
    LOGO = (By.CSS_SELECTOR, "a[class*='logo']")  # ✓ Updated from parser
    LANGUAGE_SWITCHER = (By.CSS_SELECTOR, "button[data-testid='lang_btn']")  # ✓ Nov 2025 - data-testid
    LANGUAGE_UK = (By.XPATH, "//button[contains(@class, 'lang')]//a[contains(text(), 'UA')]")
    LANGUAGE_RU = (By.XPATH, "//button[contains(@class, 'lang')]//a[contains(text(), 'RU')]")
    CATALOG_BUTTON = (By.CSS_SELECTOR, "button[data-testid='menu_button']")  # ✓ Nov 2025 - data-testid
    CART_ICON = (By.CSS_SELECTOR, "button[data-testid='header-cart-btn']")  # ✓ Nov 2025 - data-testid
    CART_COUNTER = (
        By.CSS_SELECTOR,
        "button[data-testid='header-cart-btn'] span[class*='counter']",
    )
    MAIN_CATEGORIES = (By.CSS_SELECTOR, "ul[class*='menu'] > li")
    PROMOTION_BANNER = (By.CSS_SELECTOR, "div[class*='promo']")

    def __init__(self, driver):
        """Initialize home page"""
        super().__init__(driver)
        logger.info("Initialized HomePage")

    def open_home_page(self):
        """Open Rozetka home page"""
        import time

        logger.info("Opening Rozetka home page")
        self.open("/")

        # Wait for page to fully load
        time.sleep(2)

        # Wait for search input to be present
        self.wait_for_element_visible(self.SEARCH_INPUT, timeout=20)
        logger.info("Home page loaded successfully")
        return self

    def search_product(self, query: str):
        """
        Search for product

        Args:
            query: Search query
        """
        logger.info(f"Searching for product: {query}")
        # Use Enter instead of clicking button (more reliable on Rozetka)
        self.search_product_with_enter(query)

    def search_product_with_enter(self, query: str):
        """
        Search for product using Enter key

        Args:
            query: Search query
        """
        import time

        logger.info(f"Searching for product with Enter: {query}")

        # Wait for search input
        search_input = self.wait_for_element_visible(self.SEARCH_INPUT, timeout=20)
        search_input.clear()
        time.sleep(0.3)

        # Type text quickly
        search_input.send_keys(query)

        time.sleep(0.5)  # Brief wait for autocomplete
        logger.info("Pressing Enter...")
        self.press_key(self.SEARCH_INPUT, "ENTER")
        time.sleep(1)  # Wait for navigation

    def open_catalog(self):
        """Open main catalog menu"""
        import time

        logger.info("Opening catalog")

        # Try clicking catalog button
        try:
            catalog_btn = self.find_element(self.CATALOG_BUTTON, timeout=10)
            logger.info(f"Catalog button found, clicking...")

            # Try regular click first
            catalog_btn.click()
            logger.info("Regular click executed")
        except Exception as e:
            logger.warning(f"Regular click failed: {e}, trying JavaScript")
            catalog_btn = self.find_element(self.CATALOG_BUTTON, timeout=10)
            self.execute_script("arguments[0].click();", catalog_btn)
            logger.info("JavaScript click executed")

        time.sleep(2)  # Increased wait for menu to open
        logger.info("Catalog opened")

    def is_catalog_opened(self) -> bool:
        """Check if catalog is opened"""
        import time

        time.sleep(1)  # Wait for menu animation

        # Try multiple selectors
        selectors = [
            (By.CSS_SELECTOR, "ul[class*='menu-categories']"),
            (By.CSS_SELECTOR, "div[class*='menu-wrapper']"),
            (By.CSS_SELECTOR, "rz-sidebar-fat-menu"),
            (By.CSS_SELECTOR, "[class*='fat-menu']"),
        ]

        for selector in selectors:
            if self.is_element_visible(selector, timeout=3):
                logger.info(f"Catalog opened (detected via {selector})")
                return True

        logger.warning("Catalog not detected with any selector")
        return False

    def get_main_categories(self) -> list:
        """
        Get list of main categories

        Returns:
            List of category names
        """
        logger.info("Getting main categories")
        self.open_catalog()
        categories = self.find_elements(self.MAIN_CATEGORIES)
        category_names = [cat.text for cat in categories if cat.text]
        logger.info(f"Found {len(category_names)} categories")
        return category_names

    def select_category(self, category_name: str):
        """
        Select category from catalog

        Args:
            category_name: Name of category to select
        """
        logger.info(f"Selecting category: {category_name}")
        self.open_catalog()
        category_locator = (By.XPATH, f"//ul[contains(@class, 'menu-categories')]//a[contains(text(), '{category_name}')]")
        self.click(category_locator)

    def change_language(self, language: str):
        """
        Change site language

        Args:
            language: Language code ('uk' or 'ru')
        """
        import time

        logger.info(f"Changing language to: {language}")

        # Click language switcher button
        self.click(self.LANGUAGE_SWITCHER, timeout=10)
        time.sleep(0.5)  # Wait for dropdown

        if language.lower() == "uk":
            self.click(self.LANGUAGE_UK, timeout=10)
        elif language.lower() == "ru":
            self.click(self.LANGUAGE_RU, timeout=10)
        else:
            raise ValueError(f"Unsupported language: {language}")

        time.sleep(1)  # Wait for page to reload

    def get_current_language(self) -> str:
        """
        Get current language

        Returns:
            Current language code
        """
        lang_button = self.find_element(self.LANGUAGE_SWITCHER)
        return lang_button.text.lower()

    def open_cart(self):
        """Open shopping cart"""
        import time

        logger.info("Opening cart")
        self.click(self.CART_ICON, timeout=10)
        time.sleep(1)  # Wait for cart modal/page

    def get_cart_items_count(self) -> int:
        """
        Get number of items in cart from counter badge

        Returns:
            Number of items
        """
        import time

        time.sleep(2)  # Increased wait for counter to update

        if self.is_element_visible(self.CART_COUNTER, timeout=5):
            count_text = self.get_text(self.CART_COUNTER)
            logger.info(f"Cart counter shows: {count_text}")
            try:
                return int(count_text)
            except ValueError:
                logger.warning(f"Could not parse cart counter: {count_text}")
                return 0
        else:
            logger.info("Cart counter not visible (likely 0 items)")
            return 0

    def click_logo(self):
        """Click on Rozetka logo to return to home page"""
        logger.info("Clicking logo")
        self.click(self.LOGO)

    def is_home_page_opened(self) -> bool:
        """
        Check if home page is opened

        Returns:
            True if on home page
        """
        return self.base_url in self.get_current_url()
