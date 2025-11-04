"""
Category Page Module

This module contains the page object for Rozetka category pages.
"""

from selenium.webdriver.common.by import By
import logging
from typing import List

from pages.base_page import BasePage


logger = logging.getLogger(__name__)


class CategoryPage(BasePage):
    """Category page of Rozetka"""

    # Locators (parsed from live Rozetka - December 2025)
    CATEGORY_TITLE = (By.CSS_SELECTOR, "h1")  # ✓ Parsed: simple h1 selector
    PRODUCT_TILES = (By.CSS_SELECTOR, "li[class*='catalog-grid__cell']")
    PRODUCT_TITLES = (By.CSS_SELECTOR, "span[class*='goods-tile__title']")
    PRODUCT_PRICES = (By.CSS_SELECTOR, "span[class*='goods-tile__price-value']")
    SUBCATEGORIES = (By.CSS_SELECTOR, "div[class*='tiles-list'] a")
    BREADCRUMBS = (By.CSS_SELECTOR, "nav")  # ✓ Parsed: first nav is breadcrumbs
    BREADCRUMB_LINKS = (By.CSS_SELECTOR, "nav a")  # ✓ Links within breadcrumbs
    FILTERS_SIDEBAR = (By.CSS_SELECTOR, "aside[class*='sidebar']")
    SORT_DROPDOWN = (By.CSS_SELECTOR, "select[class*='select-css']")
    VIEW_GRID_BUTTON = (By.CSS_SELECTOR, "button[class*='catalog-view--grid']")
    VIEW_LIST_BUTTON = (By.CSS_SELECTOR, "button[class*='catalog-view--list']")
    PRODUCTS_COUNT_TEXT = (By.CSS_SELECTOR, "span[class*='goods-count']")
    LOAD_MORE_BUTTON = (By.CSS_SELECTOR, "button[class*='paginate__more']")

    def __init__(self, driver):
        """Initialize category page"""
        super().__init__(driver)
        logger.info("Initialized CategoryPage")

    def wait_for_category_load(self, timeout: int = 10) -> bool:
        """
        Wait for category page to load

        Args:
            timeout: Wait timeout in seconds

        Returns:
            True if loaded
        """
        logger.info("Waiting for category to load")
        return self.is_element_visible(self.CATEGORY_TITLE, timeout=timeout)

    def get_category_title(self) -> str:
        """
        Get category title

        Returns:
            Category title
        """
        title = self.get_text(self.CATEGORY_TITLE)
        logger.info(f"Category title: {title}")
        return title

    def get_products_count(self) -> int:
        """
        Get number of products visible on page

        Returns:
            Number of products
        """
        products = self.find_elements(self.PRODUCT_TILES)
        count = len(products)
        logger.info(f"Found {count} products on category page")
        return count

    def get_product_titles(self) -> List[str]:
        """
        Get list of product titles

        Returns:
            List of product titles
        """
        logger.info("Getting product titles from category")
        titles = self.find_elements(self.PRODUCT_TITLES)
        return [title.text for title in titles if title.text]

    def get_subcategories(self) -> List[str]:
        """
        Get list of subcategories

        Returns:
            List of subcategory names
        """
        logger.info("Getting subcategories")
        subcats = self.find_elements(self.SUBCATEGORIES)
        return [cat.text for cat in subcats if cat.text]

    def select_subcategory(self, subcategory_name: str):
        """
        Select subcategory

        Args:
            subcategory_name: Name of subcategory to select
        """
        logger.info(f"Selecting subcategory: {subcategory_name}")
        subcat_locator = (By.XPATH, f"//div[contains(@class, 'tiles-list')]//a[contains(text(), '{subcategory_name}')]")
        self.click(subcat_locator)

    def get_breadcrumbs(self) -> List[str]:
        """
        Get breadcrumb trail

        Returns:
            List of breadcrumb items
        """
        logger.info("Getting breadcrumbs")
        # Get breadcrumb links
        breadcrumb_links = self.find_elements(self.BREADCRUMB_LINKS)
        breadcrumbs = [bc.text.strip() for bc in breadcrumb_links if bc.text.strip()]
        logger.info(f"Breadcrumbs: {breadcrumbs}")
        return breadcrumbs

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

    def switch_to_grid_view(self):
        """Switch to grid view"""
        logger.info("Switching to grid view")
        if self.is_element_present(self.VIEW_GRID_BUTTON):
            self.click(self.VIEW_GRID_BUTTON)

    def switch_to_list_view(self):
        """Switch to list view"""
        logger.info("Switching to list view")
        if self.is_element_present(self.VIEW_LIST_BUTTON):
            self.click(self.VIEW_LIST_BUTTON)

    def load_more_products(self):
        """Load more products (if pagination button exists)"""
        logger.info("Loading more products")
        if self.is_element_visible(self.LOAD_MORE_BUTTON, timeout=3):
            self.click(self.LOAD_MORE_BUTTON)
        else:
            logger.info("Load more button not found")

    def sort_products(self, sort_option: str):
        """
        Sort products

        Args:
            sort_option: Sort option ('price_asc', 'price_desc', 'popularity', etc.)
        """
        logger.info(f"Sorting products by: {sort_option}")
        self.click(self.SORT_DROPDOWN)

        sort_locators = {
            "price_asc": (By.XPATH, "//option[contains(text(), 'Від дешевих до дорогих')]"),
            "price_desc": (By.XPATH, "//option[contains(text(), 'Від дорогих до дешевих')]"),
            "popularity": (By.XPATH, "//option[contains(text(), 'Популярні')]"),
            "novelty": (By.XPATH, "//option[contains(text(), 'Новинки')]"),
        }

        if sort_option in sort_locators:
            self.click(sort_locators[sort_option])
        else:
            raise ValueError(f"Unknown sort option: {sort_option}")

    def is_category_page(self) -> bool:
        """
        Check if on category page

        Returns:
            True if on category page
        """
        return self.is_element_visible(self.CATEGORY_TITLE, timeout=5)
