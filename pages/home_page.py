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
    LANGUAGE_SWITCHER = (By.CSS_SELECTOR, "button[class*='lang']")
    LANGUAGE_UK = (By.XPATH, "//button[contains(@class, 'lang')]//a[contains(text(), 'UA')]")
    LANGUAGE_RU = (By.XPATH, "//button[contains(@class, 'lang')]//a[contains(text(), 'RU')]")
    CATALOG_BUTTON = (By.CSS_SELECTOR, "button[class*='menu']")  # ✓ Updated from parser
    CART_ICON = (By.CSS_SELECTOR, "a[href*='cart']")
    CART_COUNTER = (By.CSS_SELECTOR, "span[class*='counter']")
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
        
        # Wait for page to fully load (important for headless mode)
        time.sleep(3)
        
        # Wait for search input to be present (ensures page is loaded)
        self.wait_for_element_visible(self.SEARCH_INPUT, timeout=30)
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

        # Wait for search input to be visible and interactable (increased timeout for CI/CD)
        search_input = self.wait_for_element_visible(self.SEARCH_INPUT, timeout=30)
        search_input.clear()
        time.sleep(0.5)

        # Type text slowly to let autocomplete work
        for char in query:
            search_input.send_keys(char)
            time.sleep(0.1)  # Small delay between characters

        time.sleep(1)  # Wait for autocomplete suggestions
        logger.info("Pressing Enter...")
        self.press_key(self.SEARCH_INPUT, "ENTER")
        time.sleep(2)  # Wait for navigation to complete

    def open_catalog(self):
        """Open main catalog menu"""
        logger.info("Opening catalog")
        self.click(self.CATALOG_BUTTON)

    def is_catalog_opened(self) -> bool:
        """Check if catalog is opened"""
        return self.is_element_visible((By.CSS_SELECTOR, "ul[class*='menu-categories']"), timeout=5)

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
        logger.info(f"Changing language to: {language}")
        self.click(self.LANGUAGE_SWITCHER)

        if language.lower() == "uk":
            self.click(self.LANGUAGE_UK)
        elif language.lower() == "ru":
            self.click(self.LANGUAGE_RU)
        else:
            raise ValueError(f"Unsupported language: {language}")

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
        logger.info("Opening cart")
        self.click(self.CART_ICON)

    def get_cart_items_count(self) -> int:
        """
        Get number of items in cart

        Returns:
            Number of items
        """
        if self.is_element_visible(self.CART_COUNTER, timeout=2):
            count_text = self.get_text(self.CART_COUNTER)
            return int(count_text)
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
