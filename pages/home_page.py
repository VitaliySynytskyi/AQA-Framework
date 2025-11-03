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

    # Locators
    SEARCH_INPUT = (By.NAME, "search")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[class*='search__button']")
    LOGO = (By.CSS_SELECTOR, "a[class*='header__logo']")
    LANGUAGE_SWITCHER = (By.CSS_SELECTOR, "button[class*='lang-toggle']")
    LANGUAGE_UK = (By.XPATH, "//button[contains(@class, 'lang-toggle')]//a[contains(text(), 'UA')]")
    LANGUAGE_RU = (By.XPATH, "//button[contains(@class, 'lang-toggle')]//a[contains(text(), 'RU')]")
    CATALOG_BUTTON = (By.CSS_SELECTOR, "button[class*='menu-toggler']")
    CART_ICON = (By.CSS_SELECTOR, "a[class*='header__button--cart']")
    CART_COUNTER = (By.CSS_SELECTOR, "span[class*='counter--green']")
    MAIN_CATEGORIES = (By.CSS_SELECTOR, "ul[class*='menu-categories'] > li")
    PROMOTION_BANNER = (By.CSS_SELECTOR, "div[class*='promo-banner']")

    def __init__(self, driver):
        """Initialize home page"""
        super().__init__(driver)
        logger.info("Initialized HomePage")

    def open_home_page(self):
        """Open Rozetka home page"""
        logger.info("Opening Rozetka home page")
        self.open("/")
        return self

    def search_product(self, query: str):
        """
        Search for product

        Args:
            query: Search query
        """
        logger.info(f"Searching for product: {query}")
        self.input_text(self.SEARCH_INPUT, query)
        self.click(self.SEARCH_BUTTON)

    def search_product_with_enter(self, query: str):
        """
        Search for product using Enter key

        Args:
            query: Search query
        """
        logger.info(f"Searching for product with Enter: {query}")
        self.input_text(self.SEARCH_INPUT, query)
        self.press_key(self.SEARCH_INPUT, "ENTER")

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
