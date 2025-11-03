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
    
    # Locators
    SEARCH_RESULTS = (By.CSS_SELECTOR, "div[class*='catalog-grid__cell']")
    PRODUCT_TILES = (By.CSS_SELECTOR, "li[class*='catalog-grid__cell']")
    PRODUCT_TITLES = (By.CSS_SELECTOR, "span[class*='goods-tile__title']")
    PRODUCT_PRICES = (By.CSS_SELECTOR, "span[class*='goods-tile__price-value']")
    SORT_DROPDOWN = (By.CSS_SELECTOR, "select[class*='select-css']")
    SORT_BY_PRICE_ASC = (By.XPATH, "//option[contains(text(), 'Від дешевих до дорогих')]")
    SORT_BY_PRICE_DESC = (By.XPATH, "//option[contains(text(), 'Від дорогих до дешевих')]")
    SORT_BY_POPULARITY = (By.XPATH, "//option[contains(text(), 'Популярні')]")
    SORT_BY_NOVELTY = (By.XPATH, "//option[contains(text(), 'Новинки')]")
    SORT_BY_ACTION = (By.XPATH, "//option[contains(text(), 'Акційні')]")
    SORT_BY_RATING = (By.XPATH, "//option[contains(text(), 'Рейтинг')]")
    NO_RESULTS_MESSAGE = (By.CSS_SELECTOR, "div[class*='catalog-nothing-found']")
    SEARCH_QUERY_TEXT = (By.CSS_SELECTOR, "h1[class*='catalog-heading']")
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, "button[class*='buy-button']")
    PAGINATION = (By.CSS_SELECTOR, "ul[class*='pagination']")
    NEXT_PAGE_BUTTON = (By.CSS_SELECTOR, "a[class*='pagination__link--next']")
    FILTER_SIDEBAR = (By.CSS_SELECTOR, "aside[class*='sidebar']")
    PRICE_MIN_INPUT = (By.CSS_SELECTOR, "input[formcontrolname='min']")
    PRICE_MAX_INPUT = (By.CSS_SELECTOR, "input[formcontrolname='max']")
    APPLY_FILTER_BUTTON = (By.XPATH, "//button[contains(text(), 'Застосувати')]")
    
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
        logger.info("Waiting for search results")
        return self.is_element_visible(self.PRODUCT_TILES, timeout=timeout)
    
    def get_products_count(self) -> int:
        """
        Get number of products on current page
        
        Returns:
            Number of products
        """
        products = self.find_elements(self.PRODUCT_TILES)
        count = len(products)
        logger.info(f"Found {count} products on page")
        return count
    
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
                price_text = price_elem.text.replace(' ', '').replace('₴', '')
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
        logger.info(f"Sorting by: {sort_option}")
        self.click(self.SORT_DROPDOWN)
        
        sort_locators = {
            'price_asc': self.SORT_BY_PRICE_ASC,
            'price_desc': self.SORT_BY_PRICE_DESC,
            'popularity': self.SORT_BY_POPULARITY,
            'novelty': self.SORT_BY_NOVELTY,
            'action': self.SORT_BY_ACTION,
            'rating': self.SORT_BY_RATING
        }
        
        if sort_option in sort_locators:
            self.click(sort_locators[sort_option])
        else:
            raise ValueError(f"Unknown sort option: {sort_option}")
    
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
        logger.info(f"Adding product at index {index} to cart")
        add_buttons = self.find_elements(self.ADD_TO_CART_BUTTONS)
        if 0 <= index < len(add_buttons):
            self.scroll_to_element(self.ADD_TO_CART_BUTTONS)
            add_buttons[index].click()
        else:
            raise IndexError(f"Product index {index} out of range")
    
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
