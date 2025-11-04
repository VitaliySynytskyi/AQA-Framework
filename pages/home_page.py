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

    # Locators (parsed from live Rozetka site - December 2025)
    SEARCH_INPUT = (By.NAME, "search")  # ✓ Verified: input[name='search']
    SEARCH_BUTTON = (
        By.CSS_SELECTOR,
        "rz-search-suggest form button[type='submit']",
    )
    LOGO = (By.CSS_SELECTOR, "a[class*='logo']")
    # Language switching via URL (NO dropdown UI exists)
    UK_URL = "https://rozetka.com.ua/ua/"
    RU_URL = "https://rozetka.com.ua/ru/"
    CATALOG_BUTTON = (By.CSS_SELECTOR, "button[data-testid='fat_menu_btn']")  # ✓ Parsed: fat_menu_btn
    CART_ICON = (By.CSS_SELECTOR, "button[data-testid='header-cart-btn']")  # ✓ Verified
    CART_COUNTER = (
        By.CSS_SELECTOR,
        "button[data-testid='header-cart-btn'] .badge",
    )  # ✓ Parsed
    MAIN_CATEGORIES = (By.CSS_SELECTOR, "a.menu-link")  # ✓ Parsed: category links in menu
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

        # Check for menu container with category links
        if self.is_element_visible((By.CSS_SELECTOR, "div[class*='menu']"), timeout=3):
            # Verify that category links are visible
            if self.is_element_visible((By.CSS_SELECTOR, "a.menu-link"), timeout=3):
                logger.info("Catalog opened (detected via menu links)")
                return True

        logger.warning("Catalog not detected")
        return False

    def get_main_categories(self) -> list:
        """
        Get list of main categories

        Returns:
            List of category names
        """
        import time

        logger.info("Getting main categories")

        # Ensure catalog is open
        if not self.is_catalog_opened():
            self.open_catalog()
            time.sleep(2)  # Wait for menu to fully expand

        # Find category links
        categories = self.find_elements(self.MAIN_CATEGORIES)
        category_names = [cat.text.strip() for cat in categories if cat.text.strip()]
        logger.info(f"Found {len(category_names)} categories")
        return category_names

    def select_category(self, category_name: str):
        """
        Select category from catalog

        Args:
            category_name: Name of category to select
        """
        import time

        logger.info(f"Selecting category: {category_name}")

        # Ensure catalog is open
        if not self.is_catalog_opened():
            self.open_catalog()
            time.sleep(2)  # Wait for menu to fully expand

        # Escape single quotes in XPath by using concat
        if "'" in category_name:
            # Split by ' and use concat
            parts = category_name.split("'")
            xpath_text = f"concat('{parts[0]}', \"'\", '{parts[1]}')"
            category_locator = (
                By.XPATH,
                f"//a[contains(@class, 'menu-link') and contains(text(), {xpath_text})]",
            )
        else:
            category_locator = (
                By.XPATH,
                f"//a[contains(@class, 'menu-link') and contains(text(), '{category_name}')]",
            )

        self.click(category_locator, timeout=20)  # Increased timeout for slow navigation
        time.sleep(2)  # Wait for category page to start loading

    def change_language(self, language: str):
        """
        Change site language via URL (Rozetka uses URL-based language switching)

        Args:
            language: Language code ('uk' or 'ru')
        """
        import time

        logger.info(f"Changing language to: {language}")

        if language.lower() == "uk":
            logger.info(f"Navigating to Ukrainian version: {self.UK_URL}")
            self.driver.get(self.UK_URL)
        elif language.lower() == "ru":
            logger.info(f"Navigating to Russian version: {self.RU_URL}")
            self.driver.get(self.RU_URL)
        else:
            raise ValueError(f"Unsupported language: {language}")

        time.sleep(2)  # Wait for page to load

    def get_current_language(self) -> str:
        """
        Get current language from URL

        Returns:
            Current language code ('uk' or 'ru')
        """
        current_url = self.get_current_url()
        if "/ua/" in current_url:
            return "uk"
        elif "/ru/" in current_url:
            return "ru"
        else:
            # Default language is Ukrainian
            return "uk"

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

        # Wait longer for counter to update after adding to cart
        time.sleep(3)

        try:
            # Try to find the counter element
            counter_element = self.driver.find_element(*self.CART_COUNTER)
            count_text = counter_element.text.strip()

            if count_text:
                logger.info(f"Cart counter shows: '{count_text}'")
                try:
                    return int(count_text)
                except ValueError:
                    logger.warning(f"Could not parse cart counter: '{count_text}'")
                    return 0
            else:
                logger.info("Cart counter element found but empty (0 items)")
                return 0
        except Exception as e:
            logger.info(f"Cart counter not found or not visible (0 items): {e}")
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
